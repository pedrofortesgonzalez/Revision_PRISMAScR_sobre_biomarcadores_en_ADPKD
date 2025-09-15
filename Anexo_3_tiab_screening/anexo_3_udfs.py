#!/usr/bin/env python
# coding: utf-8

# screening_functions.py
import os, pandas as pd
import requests, json
from tqdm import tqdm
from semanticscholar import SemanticScholar


def viz():
    """
    Ampliar la visualización de outputs por defecto de pandas.
    """
    pd.set_option('display.max_rows', None)       # show all rows
    pd.set_option('display.max_columns', None)    # show all cols
    pd.set_option('display.width', None)          # not restricting width
    pd.set_option('display.max_colwidth', None)   # show all content in every cell


# Intentar importar SemanticScholar solo si se usa
try:
    from semanticscholar import SemanticScholar
    SEMANTIC_SCHOLAR_AVAILABLE = True
except ImportError:
    SEMANTIC_SCHOLAR_AVAILABLE = False

def fetch_abstract_by_doi(doi, mail):
    """
    Recupera el abstract de un artículo dado su DOI usando varias APIs.
    Args:
        doi (str): DOI del artículo.
        mail (str): Email para Unpaywall y CrossRef.
    Returns:
        str: Abstract o cadena vacía si no se encuentra.
    """
    # Método 1: CrossRef
    try:
        url = f"https://api.crossref.org/works/{doi}"
        headers = {"User-Agent": "AbstractRecovery/1.0 (mailto:'pedro.fortes.gonzalez@sergas.es')"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'abstract' in data.get('message', {}):
                return data['message']['abstract']
    except Exception as e:
        print(f"Error en CrossRef para DOI {doi}: {e}")
    
    # Método 2: Unpaywall
    try:
        url = f"https://api.unpaywall.org/v2/{doi}?email={mail}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('abstract'):
                return data['abstract']
    except Exception as e:
        print(f"Error en Unpaywall para DOI {doi}: {e}")
    
    # Método 3: Semantic Scholar (requiere instalación de paquete)
    # pip install semanticscholar
    try:
        from semanticscholar import SemanticScholar
        sch = SemanticScholar()
        paper = sch.get_paper(f"DOI:{doi}")
        if paper:
            return paper['abstract']
    except Exception as e:
        print(f"Error en Semantic Scholar para DOI {doi}: {e}")
    
    return ''



def highlight_keywords(text, keywords):
    """
    Resalta palabras clave en el texto usando ANSI escape codes.
    Args:
        text (str): Texto original.
        keywords (list): Lista de palabras clave.
        highlight_style (str): Formato para resaltar (por defecto rojo).
    Returns:
        str: Texto con palabras clave resaltadas.
    """
    if not text or not isinstance(text, str):
        return ""
    for keyword in keywords:
        text = text.replace(keyword, f"\033[1;31;40m{keyword}\033[0m")
    return text



def interactive_screening(df, keywords, output_file='Anexo_3_carpeta_2_resultados/table_3.4_screening_wip.csv'):
    """
    Screening para artículos con clasificación detallada de biomarcadores y aplicaciones traslacionales
    
    Args:
        df (DataFrame): DataFrame con los artículos a clasificar
        keywords (list): Lista de palabras clave para resaltar
        output_file (str): Nombre del archivo CSV donde se guarda el progreso
        
    Returns:
        DataFrame: DataFrame con todas las clasificaciones y criterios
    """
    # Separamos criterios booleanos y de texto
    bool_criteria = ['ADPKD?', 'OMICS?', 'BIOINFO?', 'HUMAN DATA?']
    text_criteria = ['BIOMARKER?', 'TRASLATIONAL?']
    
    # Hacer una copia para evitar warnings de SettingWithCopyWarning
    df = df.copy()
    
    # Asegurarse de que existan las columnas necesarias con los tipos correctos
    if 'COMMENT' not in df.columns:
        df['COMMENT'] = None
    else:
        df['COMMENT'] = df['COMMENT'].astype('object')  # Convertir a tipo string/object
    
    if 'DECISION' not in df.columns:
        df['DECISION'] = None
    else:
        df['DECISION'] = df['DECISION'].astype('object')  # Convertir a tipo string/object
    
    # Asegurarse de que existan las columnas de criterios con valores por defecto apropiados
    for criterion in bool_criteria:
        if criterion not in df.columns:
            df[criterion] = False
        else:
            df[criterion] = df[criterion].astype('bool')  # Asegurar tipo booleano
            
    for criterion in text_criteria:
        if criterion not in df.columns:
            df[criterion] = None
        else:
            df[criterion] = df[criterion].astype('object')  # Convertir a tipo string/object
    
    # Verificar si existe un archivo de progreso previo
    if os.path.exists(output_file):
        print(f"Se encontró un archivo de progreso previo: {output_file}")
        try: 
            prev_progress = pd.read_csv(output_file, sep=";")
        except:
            prev_progress = pd.read_csv(output_file, sep=",")
        
        # Asegurar que las columnas necesarias existan
        if 'COMMENT' not in prev_progress.columns:
            prev_progress['COMMENT'] = None
        if 'DECISION' not in prev_progress.columns:
            prev_progress['DECISION'] = None
        
        # Asegurarse de que las columnas de criterios existen
        for criterion in bool_criteria:
            if criterion not in prev_progress.columns:
                prev_progress[criterion] = False
                
        for criterion in text_criteria:
            if criterion not in prev_progress.columns:
                prev_progress[criterion] = None
        
        # Identificar artículos ya clasificados (aquellos con decisión no nula)
        classified_articles = prev_progress[~prev_progress['DECISION'].isna()]
        pending_articles = df[~df.index.isin(classified_articles.index)]
        
        # Informar al usuario
        print(f"Artículos ya clasificados: {len(classified_articles)}")
        print(f"Artículos pendientes: {len(pending_articles)}")
        
        # Confirmar si quiere continuar donde lo dejó
        continue_choice = input("¿Deseas continuar donde lo dejaste? [y/n]: ").lower()
        
        if continue_choice == 'y':
            # Trabajar solo con los artículos pendientes
            working_df = pending_articles.copy()
            # Conservar las decisiones, comentarios y criterios previos
            decision_dict = dict(zip(classified_articles.index, classified_articles['DECISION']))
            comment_dict = dict(zip(classified_articles.index, classified_articles['COMMENT'].fillna('')))
            
            # Diccionario para almacenar los criterios marcados
            bool_criteria_dict = {criterion: {} for criterion in bool_criteria}
            text_criteria_dict = {criterion: {} for criterion in text_criteria}
            
            for criterion in bool_criteria:
                for idx in classified_articles.index:
                    if idx in classified_articles.index:
                        bool_criteria_dict[criterion][idx] = classified_articles.at[idx, criterion]
            
            for criterion in text_criteria:
                for idx in classified_articles.index:
                    if idx in classified_articles.index:
                        text_criteria_dict[criterion][idx] = classified_articles.at[idx, criterion]
        else:
            # Reiniciar desde el principio
            working_df = df.copy()
            decision_dict = {}
            comment_dict = {}
            bool_criteria_dict = {criterion: {} for criterion in bool_criteria}
            text_criteria_dict = {criterion: {} for criterion in text_criteria}
    else:
        # No hay progreso previo, trabajar con todo el DataFrame
        working_df = df.copy()
        decision_dict = {}
        comment_dict = {}
        bool_criteria_dict = {criterion: {} for criterion in bool_criteria}
        text_criteria_dict = {criterion: {} for criterion in text_criteria}
    
    # Si no hay artículos pendientes
    if len(working_df) == 0:
        print("No hay artículos pendientes de clasificar. ¡Screening completo!")
        return df
    
    # Proceder con el screening solo para artículos pendientes
    count = 0
    for idx, row in tqdm(working_df.iterrows(), total=len(working_df)):
        title = row['Title']
        authors = row['Author']
        doi = row['DOI'] if pd.notnull(row['DOI']) else "No disponible"
        kwds = row['Manual Tags'] if pd.notnull(row['Manual Tags']) else "No disponible"
        count += 1
        
        print(f"\n--- Artículo nº {count} de {len(working_df)} (pendientes) ---")
        print(f"--- AUTHORS:\n{authors[:31]}..." if len(str(authors)) > 30 else f"\nAUTHORS:\n{authors}")
        print(f"--- KEYWORDS:\n{kwds}")
        print(f"--- TITLE:\n{title}")
        
        highlighted_abstract = highlight_keywords(row['Abstract Note'], keywords)
        print(f"--- ABSTRACT:\n{highlighted_abstract}")
        
        # Diccionarios para almacenar las respuestas actuales
        current_bool_criteria = {}
        current_text_criteria = {}
        
        # Solicitar respuestas para criterios booleanos
        print("\n=== CRITERIOS DE INCLUSIÓN BOOLEANOS ===")
        for criterion in bool_criteria:
            criterion_choice = input(f"{criterion} [y/n]: ").lower()
            is_true = True if criterion_choice == 'y' else False
            bool_criteria_dict[criterion][idx] = is_true
            current_bool_criteria[criterion] = is_true
        
        # Solicitar respuestas para criterios de texto
        print("\n=== CRITERIOS DE CLASIFICACIÓN DETALLADA ===")
        print("(Deja en blanco si no aplica, o describe el tipo/categoría)")
        
        for criterion in text_criteria:
            if criterion == "BIOMARKER?":
                print("\nTipos de biomarcadores posibles: genético, proteómico, metabolómico,")
                print("imagen, funcional, clínico, otro (especificar)")
            elif criterion == "TRASLATIONAL?":
                print("\nAspectos traslacionales: diagnóstico, pronóstico, terapéutico,")
                print("estratificación, monitorización, otro (especificar)")
                
            text_value = input(f"{criterion}: ")
            if text_value.strip():
                text_criteria_dict[criterion][idx] = text_value
                current_text_criteria[criterion] = text_value
            else:
                text_criteria_dict[criterion][idx] = None
                current_text_criteria[criterion] = None
        
        # Mostrar resumen de criterios marcados
        print("\n=== RESUMEN DE CRITERIOS MARCADOS ===")
        print("╔════════════════╦═══════════════════════════════╗")
        print("║    CRITERIO    ║            VALOR              ║")
        print("╠════════════════╬═══════════════════════════════╣")
        
        # Mostrar criterios booleanos
        for criterion, value in current_bool_criteria.items():
            value_str = "✅ SÍ" if value else "❌ NO"
            print(f"║ {criterion:<14} ║ {value_str:<29} ║")
        
        # Mostrar criterios de texto
        for criterion, value in current_text_criteria.items():
            value_str = value if value else "(No especificado)"
            # Truncar si es muy largo
            if len(value_str) > 27:
                value_str = value_str[:24] + "..."
            print(f"║ {criterion:<14} ║ {value_str:<29} ║")
        
        print("╚════════════════╩═══════════════════════════════╝")
        
        # Solicitar decisión
        choice = input("\nDECISIÓN (basada en criterios anteriores): [i]ncluir, [e]xcluir, [d]udoso, [s]alir: ").lower()

        # Si decisión es s: salir y guardar progreso
        if choice == 's':
            break

        # Registrar decisión
        decision_dict[idx] = 'dudoso' if choice == 'd' else ('include' if choice == 'i' else 'exclude')
        
        # Solicitar comentario para todas las decisiones
        comment = input("\nComentario (opcional): ")
        if comment:
            comment_dict[idx] = comment
        
        # Actualizar DataFrame completo con todas las decisiones, comentarios y criterios
        result_df = df.copy()
        for i, decision in decision_dict.items():
            result_df.at[i, 'DECISION'] = decision
            if i in comment_dict and comment_dict[i]:
                result_df.at[i, 'COMMENT'] = comment_dict[i]
                
            # Actualizar criterios booleanos
            for criterion in bool_criteria:
                if i in bool_criteria_dict[criterion]:
                    result_df.at[i, criterion] = bool_criteria_dict[criterion][i]
                    
            # Actualizar criterios de texto
            for criterion in text_criteria:
                if i in text_criteria_dict[criterion]:
                    result_df.at[i, criterion] = text_criteria_dict[criterion][i]
        
        # Guardar progreso después de cada decisión
        result_df.to_csv(output_file, index=False, sep=";")
        
        # Guardar progreso adicional cada 10 artículos
        if count % 10 == 0:
            print(f"\n--- Progreso guardado: {count} artículos revisados en esta sesión ---")
    
    # Actualizar el DataFrame completo con todas las decisiones, comentarios y criterios finales
    result_df = df.copy()
    for i, decision in decision_dict.items():
        result_df.at[i, 'DECISION'] = decision
        if i in comment_dict and comment_dict[i]:
            result_df.at[i, 'COMMENT'] = comment_dict[i]
            
        # Actualizar criterios booleanos
        for criterion in bool_criteria:
            if i in bool_criteria_dict[criterion]:
                result_df.at[i, criterion] = bool_criteria_dict[criterion][i]
                
        # Actualizar criterios de texto
        for criterion in text_criteria:
            if i in text_criteria_dict[criterion]:
                result_df.at[i, criterion] = text_criteria_dict[criterion][i]
    
    # Guardar progreso final
    result_df.to_csv(output_file, index=False, sep=";")
    
    # Mostrar estadísticas
    stats = {
        'total': len(result_df),
        'clasificados': sum(~result_df['DECISION'].isna()),
        'pendientes': sum(result_df['DECISION'].isna()),
        'incluidos': sum(result_df['DECISION'] == 'include'),
        'excluidos': sum(result_df['DECISION'] == 'exclude'),
        'dudosos': sum(result_df['DECISION'] == 'dudoso')
    }
    
    # Estadísticas por criterio booleano
    bool_criteria_stats = {}
    for criterion in bool_criteria:
        bool_criteria_stats[criterion] = sum(result_df[criterion] == True)
    
    # Estadísticas de criterios de texto (categorías más frecuentes)
    text_criteria_stats = {}
    for criterion in text_criteria:
        values = result_df[criterion].dropna().value_counts().head(5)
        text_criteria_stats[criterion] = values
    
    print("\n=== ESTADÍSTICAS DE SCREENING ===")
    print(f"Total artículos: {stats['total']}")
    print(f"Artículos clasificados: {stats['clasificados']} ({stats['clasificados']/stats['total']*100:.1f}%)")
    print(f"Artículos incluidos: {stats['incluidos']}")
    print(f"Artículos excluidos: {stats['excluidos']}")
    print(f"Artículos dudosos: {stats['dudosos']}")
    print(f"Artículos pendientes: {stats['pendientes']}")
    
    print("\n=== ESTADÍSTICAS DE CRITERIOS BOOLEANOS ===")
    for criterion, count in bool_criteria_stats.items():
        print(f"{criterion}: {count} artículos")
        
    print("\n=== CATEGORÍAS MÁS FRECUENTES EN CRITERIOS DE TEXTO ===")
    for criterion, counts in text_criteria_stats.items():
        print(f"\n{criterion}:")
        if len(counts) > 0:
            for category, count in counts.items():
                print(f"  - {category}: {count}")
        else:
            print("  (Sin datos)")
    
    return result_df
