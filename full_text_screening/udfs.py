"""
User Defined Functions para full text screening
PRISMA-ScR Revisión sobre biomarcadores en ADPKD
"""

import pandas as pd
import numpy as np
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import PyPDF2
import textract
from sklearn.metrics import cohen_kappa_score


def identify_missing_fulltext(df: pd.DataFrame, available_pdfs: List[Path]) -> pd.DataFrame:
    """
    Identifica artículos sin texto completo disponible.
    
    Args:
        df (pd.DataFrame): DataFrame con artículos incluidos en TIAB
        available_pdfs (List[Path]): Lista de PDFs disponibles
        
    Returns:
        pd.DataFrame: Artículos sin texto completo
    """
    # Extraer identificadores de PDFs disponibles
    available_ids = []
    for pdf_path in available_pdfs:
        # Asumiendo que el nombre del archivo contiene DOI o PMID
        filename = pdf_path.stem
        available_ids.append(filename)
    
    # Identificar artículos sin PDF
    missing_mask = ~df['DOI'].str.replace('/', '_').isin(available_ids)
    missing_mask = missing_mask & ~df['PMID'].astype(str).isin(available_ids)
    
    return df[missing_mask].copy()


def extract_text_from_pdfs(pdf_paths: List[Path]) -> Dict[str, str]:
    """
    Extrae texto de archivos PDF.
    
    Args:
        pdf_paths (List[Path]): Lista de rutas a archivos PDF
        
    Returns:
        Dict[str, str]: Diccionario con ID del artículo y texto extraído
    """
    extracted_texts = {}
    
    for pdf_path in pdf_paths:
        try:
            # Intentar con PyPDF2
            text = extract_with_pypdf2(pdf_path)
            
            if not text or len(text.strip()) < 100:
                # Intentar con textract como fallback
                text = extract_with_textract(pdf_path)
            
            if text and len(text.strip()) >= 100:
                article_id = pdf_path.stem
                extracted_texts[article_id] = text
                
        except Exception as e:
            print(f"Error extrayendo texto de {pdf_path.name}: {e}")
            
    return extracted_texts


def extract_with_pypdf2(pdf_path: Path) -> str:
    """
    Extrae texto usando PyPDF2.
    
    Args:
        pdf_path (Path): Ruta al archivo PDF
        
    Returns:
        str: Texto extraído
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error con PyPDF2 en {pdf_path.name}: {e}")
        
    return text


def extract_with_textract(pdf_path: Path) -> str:
    """
    Extrae texto usando textract.
    
    Args:
        pdf_path (Path): Ruta al archivo PDF
        
    Returns:
        str: Texto extraído
    """
    try:
        text = textract.process(str(pdf_path)).decode('utf-8')
        return text
    except Exception as e:
        print(f"Error con textract en {pdf_path.name}: {e}")
        return ""


def automated_fulltext_screening(texts: Dict[str, str], criteria: Dict) -> Dict[str, Dict]:
    """
    Aplica screening automatizado a textos completos.
    
    Args:
        texts (Dict[str, str]): Textos extraídos por artículo
        criteria (Dict): Criterios de inclusión/exclusión
        
    Returns:
        Dict[str, Dict]: Resultados del screening automatizado
    """
    results = {}
    
    for article_id, text in texts.items():
        screening_result = {
            'article_id': article_id,
            'auto_decision': 'uncertain',
            'inclusion_score': 0,
            'exclusion_score': 0,
            'flags': []
        }
        
        # Aplicar análisis automatizado
        inclusion_score = calculate_inclusion_score(text, criteria['inclusion'])
        exclusion_score = calculate_exclusion_score(text, criteria['exclusion'])
        
        screening_result['inclusion_score'] = inclusion_score
        screening_result['exclusion_score'] = exclusion_score
        
        # Determinar decisión automática preliminar
        if exclusion_score > 3:
            screening_result['auto_decision'] = 'likely_exclude'
        elif inclusion_score > 5:
            screening_result['auto_decision'] = 'likely_include'
        
        results[article_id] = screening_result
    
    return results


def calculate_inclusion_score(text: str, inclusion_criteria: Dict) -> float:
    """
    Calcula puntuación de inclusión basada en criterios.
    
    Args:
        text (str): Texto del artículo
        inclusion_criteria (Dict): Criterios de inclusión
        
    Returns:
        float: Puntuación de inclusión
    """
    score = 0
    text_lower = text.lower()
    
    # Población (ADPKD)
    adpkd_terms = ['adpkd', 'autosomal dominant polycystic kidney', 'polycystic kidney disease']
    if any(term in text_lower for term in adpkd_terms):
        score += 2
    
    # Biomarcadores
    biomarker_terms = ['biomarker', 'marker', 'creatinine', 'gfr', 'proteinuria', 'httkv']
    biomarker_count = sum(1 for term in biomarker_terms if term in text_lower)
    score += min(biomarker_count, 3)
    
    # Diseño de estudio
    study_terms = ['cohort', 'longitudinal', 'prospective', 'clinical trial']
    if any(term in text_lower for term in study_terms):
        score += 1
    
    # Outcomes relevantes
    outcome_terms = ['progression', 'prognosis', 'diagnosis', 'monitoring']
    if any(term in text_lower for term in outcome_terms):
        score += 1
    
    return score


def calculate_exclusion_score(text: str, exclusion_criteria: Dict) -> float:
    """
    Calcula puntuación de exclusión basada en criterios.
    
    Args:
        text (str): Texto del artículo
        exclusion_criteria (Dict): Criterios de exclusión
        
    Returns:
        float: Puntuación de exclusión
    """
    score = 0
    text_lower = text.lower()
    
    # Tipos de estudio a excluir
    exclude_study = ['review', 'editorial', 'case report', 'letter']
    if any(term in text_lower for term in exclude_study):
        score += 2
    
    # Poblaciones a excluir
    exclude_pop = ['animal', 'mouse', 'rat', 'in vitro', 'cell culture']
    if any(term in text_lower for term in exclude_pop):
        score += 3
    
    # Solo genética
    genetic_only = ['genetic testing only', 'mutation analysis', 'genotype only']
    if any(term in text_lower for term in genetic_only):
        score += 1
    
    return score


def prepare_fulltext_screening_forms(df: pd.DataFrame, criteria: Dict) -> Dict:
    """
    Prepara formularios estructurados para screening manual.
    
    Args:
        df (pd.DataFrame): Artículos para screening
        criteria (Dict): Criterios detallados
        
    Returns:
        Dict: Formularios preparados
    """
    forms = {
        'screening_template': {
            'article_id': '',
            'reviewer': '',
            'decision': '',  # include/exclude/uncertain
            'inclusion_checklist': {
                'adpkd_population': False,
                'biomarker_data': False,
                'appropriate_study_design': False,
                'relevant_outcomes': False,
                'appropriate_language': False
            },
            'exclusion_checklist': {
                'animal_study': False,
                'in_vitro_only': False,
                'review_editorial': False,
                'no_biomarker_data': False,
                'pediatric_only': False,
                'no_full_text': False
            },
            'exclusion_reason': '',
            'notes': '',
            'confidence': ''  # high/medium/low
        },
        'total_articles': len(df),
        'criteria_summary': criteria
    }
    
    return forms


def load_fulltext_screening(filename: str) -> pd.DataFrame:
    """
    Carga resultados de screening de texto completo.
    
    Args:
        filename (str): Nombre del archivo
        
    Returns:
        pd.DataFrame: Resultados de screening
    """
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Archivo {filename} no encontrado")
        return pd.DataFrame()


def calculate_fulltext_agreement(reviewer1: pd.DataFrame, reviewer2: pd.DataFrame) -> float:
    """
    Calcula concordancia entre revisores en full text screening.
    
    Args:
        reviewer1 (pd.DataFrame): Decisiones del revisor 1
        reviewer2 (pd.DataFrame): Decisiones del revisor 2
        
    Returns:
        float: Coeficiente Kappa de Cohen
    """
    if len(reviewer1) == 0 or len(reviewer2) == 0:
        return 0.0
    
    merged = reviewer1.merge(reviewer2, on='article_id', suffixes=('_r1', '_r2'))
    
    if len(merged) == 0:
        return 0.0
    
    return cohen_kappa_score(merged['decision_r1'], merged['decision_r2'])


def identify_fulltext_discrepancies(reviewer1: pd.DataFrame, reviewer2: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica discrepancias en screening de texto completo.
    
    Args:
        reviewer1 (pd.DataFrame): Decisiones del revisor 1
        reviewer2 (pd.DataFrame): Decisiones del revisor 2
        
    Returns:
        pd.DataFrame: Artículos con discrepancias
    """
    merged = reviewer1.merge(reviewer2, on='article_id', suffixes=('_r1', '_r2'))
    discrepancies = merged[merged['decision_r1'] != merged['decision_r2']]
    
    return discrepancies


def resolve_fulltext_discrepancies(discrepancies: pd.DataFrame) -> pd.DataFrame:
    """
    Resuelve discrepancias en screening de texto completo.
    
    Args:
        discrepancies (pd.DataFrame): Artículos con discrepancias
        
    Returns:
        pd.DataFrame: Discrepancias resueltas
    """
    # Placeholder para resolución manual o tercer revisor
    resolved = discrepancies.copy()
    resolved['final_decision'] = 'needs_resolution'
    
    return resolved


def combine_fulltext_results(reviewer1: pd.DataFrame, reviewer2: pd.DataFrame, 
                           resolved: pd.DataFrame) -> pd.DataFrame:
    """
    Combina resultados finales de full text screening.
    
    Args:
        reviewer1 (pd.DataFrame): Decisiones del revisor 1
        reviewer2 (pd.DataFrame): Decisiones del revisor 2
        resolved (pd.DataFrame): Discrepancias resueltas
        
    Returns:
        pd.DataFrame: Resultados finales combinados
    """
    merged = reviewer1.merge(reviewer2, on='article_id', suffixes=('_r1', '_r2'))
    
    # Acuerdos
    agreements = merged[merged['decision_r1'] == merged['decision_r2']]
    agreements['decision'] = agreements['decision_r1']
    
    # Combinar con resueltos
    final_results = pd.concat([
        agreements[['article_id', 'decision']],
        resolved[['article_id', 'final_decision']].rename(columns={'final_decision': 'decision'})
    ], ignore_index=True)
    
    return final_results


def analyze_exclusion_reasons(results: pd.DataFrame) -> Dict:
    """
    Analiza las razones de exclusión en full text screening.
    
    Args:
        results (pd.DataFrame): Resultados completos de screening
        
    Returns:
        Dict: Análisis de razones de exclusión
    """
    excluded = results[results['decision'] == 'exclude']
    
    exclusion_analysis = {
        'total_excluded': len(excluded),
        'reasons': {},
        'most_common': '',
        'percentage_breakdown': {}
    }
    
    if 'exclusion_reason' in excluded.columns:
        reason_counts = excluded['exclusion_reason'].value_counts()
        exclusion_analysis['reasons'] = reason_counts.to_dict()
        
        if len(reason_counts) > 0:
            exclusion_analysis['most_common'] = reason_counts.index[0]
            exclusion_analysis['percentage_breakdown'] = (reason_counts / len(excluded) * 100).to_dict()
    
    return exclusion_analysis


def generate_final_screening_report(tiab_df: pd.DataFrame, fulltext_df: pd.DataFrame,
                                  kappa: float, exclusion_analysis: Dict) -> str:
    """
    Genera reporte final del proceso completo de screening.
    
    Args:
        tiab_df (pd.DataFrame): Resultados de TIAB screening
        fulltext_df (pd.DataFrame): Resultados de full text screening
        kappa (float): Concordancia en full text
        exclusion_analysis (Dict): Análisis de exclusiones
        
    Returns:
        str: Reporte final completo
    """
    included_final = fulltext_df[fulltext_df['decision'] == 'include']
    excluded_fulltext = fulltext_df[fulltext_df['decision'] == 'exclude']
    
    report = f"""
    REPORTE FINAL DE SCREENING - PRISMA-ScR
    =======================================
    
    ARTÍCULOS EN CADA FASE:
    - Incluidos después de TIAB: {len(tiab_df)}
    - Evaluados en full text: {len(fulltext_df)}
    - Incluidos finalmente: {len(included_final)}
    - Excluidos en full text: {len(excluded_fulltext)}
    
    CONCORDANCIA EN FULL TEXT:
    Kappa de Cohen: {kappa:.3f}
    
    RAZONES DE EXCLUSIÓN MÁS COMUNES:
    """
    
    for reason, count in list(exclusion_analysis.get('reasons', {}).items())[:5]:
        percentage = exclusion_analysis.get('percentage_breakdown', {}).get(reason, 0)
        report += f"    - {reason}: {count} ({percentage:.1f}%)\n"
    
    report += f"""
    
    FLUJO FINAL:
    Artículos identificados → TIAB screening → {len(tiab_df)} incluidos
    → Full text screening → {len(included_final)} estudios finales
    
    Tasa de inclusión final: {len(included_final)/len(tiab_df)*100:.1f}%
    """
    
    return report


def validate_pdf_quality(pdf_path: Path) -> Dict:
    """
    Valida la calidad del PDF para extracción de texto.
    
    Args:
        pdf_path (Path): Ruta al archivo PDF
        
    Returns:
        Dict: Métricas de calidad del PDF
    """
    quality_metrics = {
        'readable': False,
        'text_length': 0,
        'page_count': 0,
        'has_images_only': False,
        'extraction_method': None
    }
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            quality_metrics['page_count'] = len(pdf_reader.pages)
            
            # Extraer texto de primera página para validar
            if len(pdf_reader.pages) > 0:
                sample_text = pdf_reader.pages[0].extract_text()
                quality_metrics['text_length'] = len(sample_text)
                quality_metrics['readable'] = len(sample_text.strip()) > 50
                quality_metrics['extraction_method'] = 'pypdf2'
                
                if len(sample_text.strip()) < 50:
                    quality_metrics['has_images_only'] = True
                    
    except Exception as e:
        print(f"Error validando PDF {pdf_path.name}: {e}")
    
    return quality_metrics