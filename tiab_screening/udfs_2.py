"""
User Defined Functions para screening de títulos y abstracts
PRISMA-ScR Revisión sobre biomarcadores en ADPKD
"""

import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
import re
from typing import Dict, List, Tuple, Optional


def automated_prescreening(df: pd.DataFrame, inclusion_criteria: Dict, exclusion_criteria: Dict) -> pd.DataFrame:
    """
    Aplica pre-screening automatizado basado en palabras clave.
    
    Args:
        df (pd.DataFrame): DataFrame con registros
        inclusion_criteria (Dict): Criterios de inclusión
        exclusion_criteria (Dict): Criterios de exclusión
        
    Returns:
        pd.DataFrame: Registros que pasan el pre-screening
    """
    # Implementar pre-screening automatizado
    prescreened_df = df.copy()
    
    # Aplicar filtros de inclusión
    inclusion_mask = apply_inclusion_filters(prescreened_df, inclusion_criteria)
    
    # Aplicar filtros de exclusión
    exclusion_mask = apply_exclusion_filters(prescreened_df, exclusion_criteria)
    
    # Combinar máscaras
    final_mask = inclusion_mask & ~exclusion_mask
    
    prescreened_df['prescreening_decision'] = 'exclude'
    prescreened_df.loc[final_mask, 'prescreening_decision'] = 'include'
    
    return prescreened_df[final_mask].copy()


def apply_inclusion_filters(df: pd.DataFrame, criteria: Dict) -> pd.Series:
    """
    Aplica filtros de inclusión basados en palabras clave.
    
    Args:
        df (pd.DataFrame): DataFrame con registros
        criteria (Dict): Criterios de inclusión
        
    Returns:
        pd.Series: Máscara booleana de registros incluidos
    """
    # Palabras clave para ADPKD
    adpkd_keywords = [
        'adpkd', 'autosomal dominant polycystic kidney',
        'polycystic kidney disease', 'pkd1', 'pkd2',
        'polycystin'
    ]
    
    # Palabras clave para biomarcadores
    biomarker_keywords = [
        'biomarker', 'marker', 'indicator', 'predictor',
        'creatinine', 'gfr', 'proteinuria', 'albumin',
        'httkv', 'total kidney volume'
    ]
    
    # Combinar título y abstract para búsqueda
    text_columns = ['Title', 'Abstract']
    combined_text = df[text_columns].fillna('').apply(lambda x: ' '.join(x), axis=1).str.lower()
    
    # Buscar palabras clave de ADPKD
    adpkd_mask = combined_text.str.contains('|'.join(adpkd_keywords), case=False, na=False)
    
    # Buscar palabras clave de biomarcadores
    biomarker_mask = combined_text.str.contains('|'.join(biomarker_keywords), case=False, na=False)
    
    return adpkd_mask & biomarker_mask


def apply_exclusion_filters(df: pd.DataFrame, criteria: Dict) -> pd.Series:
    """
    Aplica filtros de exclusión basados en palabras clave.
    
    Args:
        df (pd.DataFrame): DataFrame con registros
        criteria (Dict): Criterios de exclusión
        
    Returns:
        pd.Series: Máscara booleana de registros a excluir
    """
    # Tipos de estudio a excluir
    exclude_study_types = [
        'review', 'editorial', 'letter', 'comment',
        'case report', 'conference abstract'
    ]
    
    # Poblaciones a excluir
    exclude_populations = [
        'animal', 'mouse', 'rat', 'in vitro',
        'cell culture', 'pediatric only'
    ]
    
    # Combinar título y abstract para búsqueda
    text_columns = ['Title', 'Abstract']
    combined_text = df[text_columns].fillna('').apply(lambda x: ' '.join(x), axis=1).str.lower()
    
    # Buscar términos de exclusión
    study_type_mask = combined_text.str.contains('|'.join(exclude_study_types), case=False, na=False)
    population_mask = combined_text.str.contains('|'.join(exclude_populations), case=False, na=False)
    
    return study_type_mask | population_mask


def prepare_screening_data(df: pd.DataFrame) -> Dict:
    """
    Prepara datos para screening manual por revisores.
    
    Args:
        df (pd.DataFrame): DataFrame con registros pre-screening
        
    Returns:
        Dict: Datos preparados para screening
    """
    screening_data = {
        'total_records': len(df),
        'screening_fields': ['Title', 'Abstract', 'Authors', 'Journal', 'Year'],
        'decision_options': ['include', 'exclude', 'uncertain'],
        'exclusion_reasons': [
            'not_adpkd', 'not_biomarker', 'wrong_study_type',
            'animal_study', 'no_relevant_outcome', 'other'
        ]
    }
    
    return screening_data


def load_screening_results(filename: str) -> pd.DataFrame:
    """
    Carga resultados de screening desde archivo CSV.
    
    Args:
        filename (str): Nombre del archivo con resultados
        
    Returns:
        pd.DataFrame: Resultados de screening
    """
    try:
        results = pd.read_csv(filename)
        return results
    except FileNotFoundError:
        print(f"Archivo {filename} no encontrado")
        return pd.DataFrame()


def calculate_inter_rater_agreement(reviewer1: pd.DataFrame, reviewer2: pd.DataFrame) -> float:
    """
    Calcula la concordancia entre revisores usando Kappa de Cohen.
    
    Args:
        reviewer1 (pd.DataFrame): Decisiones del revisor 1
        reviewer2 (pd.DataFrame): Decisiones del revisor 2
        
    Returns:
        float: Coeficiente Kappa de Cohen
    """
    if len(reviewer1) == 0 or len(reviewer2) == 0:
        return 0.0
    
    # Alinear dataframes por ID de registro
    merged = reviewer1.merge(reviewer2, on='record_id', suffixes=('_r1', '_r2'))
    
    if len(merged) == 0:
        return 0.0
    
    # Calcular Kappa
    kappa = cohen_kappa_score(merged['decision_r1'], merged['decision_r2'])
    return kappa


def identify_discrepancies(reviewer1: pd.DataFrame, reviewer2: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica discrepancias entre decisiones de revisores.
    
    Args:
        reviewer1 (pd.DataFrame): Decisiones del revisor 1
        reviewer2 (pd.DataFrame): Decisiones del revisor 2
        
    Returns:
        pd.DataFrame: Registros con discrepancias
    """
    # Alinear dataframes por ID de registro
    merged = reviewer1.merge(reviewer2, on='record_id', suffixes=('_r1', '_r2'))
    
    # Identificar discrepancias
    discrepancies = merged[merged['decision_r1'] != merged['decision_r2']]
    
    return discrepancies


def resolve_discrepancies(discrepancies: pd.DataFrame) -> pd.DataFrame:
    """
    Resuelve discrepancias entre revisores (placeholder para proceso manual).
    
    Args:
        discrepancies (pd.DataFrame): Registros con discrepancias
        
    Returns:
        pd.DataFrame: Discrepancias resueltas
    """
    # En una implementación real, esto requeriría intervención manual
    # o un tercer revisor
    resolved = discrepancies.copy()
    resolved['final_decision'] = 'needs_resolution'
    
    return resolved


def combine_screening_results(reviewer1: pd.DataFrame, reviewer2: pd.DataFrame, 
                            resolved: pd.DataFrame) -> pd.DataFrame:
    """
    Combina resultados finales de screening incluyendo resolución de discrepancias.
    
    Args:
        reviewer1 (pd.DataFrame): Decisiones del revisor 1
        reviewer2 (pd.DataFrame): Decisiones del revisor 2
        resolved (pd.DataFrame): Discrepancias resueltas
        
    Returns:
        pd.DataFrame: Resultados finales combinados
    """
    # Alinear dataframes
    merged = reviewer1.merge(reviewer2, on='record_id', suffixes=('_r1', '_r2'))
    
    # Identificar acuerdos
    agreements = merged[merged['decision_r1'] == merged['decision_r2']]
    agreements['decision'] = agreements['decision_r1']
    
    # Combinar con discrepancias resueltas
    final_results = pd.concat([
        agreements[['record_id', 'decision']],
        resolved[['record_id', 'final_decision']].rename(columns={'final_decision': 'decision'})
    ], ignore_index=True)
    
    return final_results


def generate_tiab_screening_report(original_df: pd.DataFrame, prescreened_df: pd.DataFrame,
                                 final_results: pd.DataFrame, kappa: float) -> str:
    """
    Genera reporte detallado del proceso de TIAB screening.
    
    Args:
        original_df (pd.DataFrame): DataFrame original
        prescreened_df (pd.DataFrame): DataFrame después de pre-screening
        final_results (pd.DataFrame): Resultados finales
        kappa (float): Coeficiente Kappa de Cohen
        
    Returns:
        str: Reporte detallado
    """
    included = final_results[final_results['decision'] == 'include']
    excluded = final_results[final_results['decision'] == 'exclude']
    
    report = f"""
    REPORTE DE TITLE/ABSTRACT SCREENING
    ===================================
    
    Registros iniciales: {len(original_df)}
    Registros después de pre-screening: {len(prescreened_df)}
    Excluidos en pre-screening: {len(original_df) - len(prescreened_df)}
    
    RESULTADOS FINALES:
    Incluidos para full-text: {len(included)}
    Excluidos en TIAB: {len(excluded)}
    
    CONCORDANCIA ENTRE REVISORES:
    Kappa de Cohen: {kappa:.3f}
    Interpretación: {interpret_kappa(kappa)}
    
    TASAS:
    Tasa de inclusión: {len(included)/len(final_results)*100:.1f}%
    Tasa de exclusión: {len(excluded)/len(final_results)*100:.1f}%
    """
    
    return report


def interpret_kappa(kappa: float) -> str:
    """
    Interpreta el valor del coeficiente Kappa de Cohen.
    
    Args:
        kappa (float): Valor de Kappa
        
    Returns:
        str: Interpretación del valor
    """
    if kappa < 0:
        return "Peor que el azar"
    elif kappa < 0.20:
        return "Concordancia muy pobre"
    elif kappa < 0.40:
        return "Concordancia pobre"
    elif kappa < 0.60:
        return "Concordancia moderada"
    elif kappa < 0.80:
        return "Concordancia buena"
    else:
        return "Concordancia muy buena"


def extract_keywords_from_text(text: str) -> List[str]:
    """
    Extrae palabras clave relevantes del texto.
    
    Args:
        text (str): Texto a analizar
        
    Returns:
        List[str]: Lista de palabras clave
    """
    # Implementar extracción de palabras clave
    # Esta es una implementación básica
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filtrar palabras comunes
    stopwords = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
    keywords = [word for word in words if word not in stopwords and len(word) > 3]
    
    return list(set(keywords))