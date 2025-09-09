#!/usr/bin/env python
# coding: utf-8

# screening_functions.py
import os, numpy as np, pandas as pd
import requests, json
from tqdm import tqdm
from semanticscholar import SemanticScholar

def fetch_abstract_by_doi(doi, mail):
    """Intenta recuperar abstract usando DOI a través de múltiples APIs"""
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
    """Resalta palabras clave en el texto"""
    if not text or not isinstance(text, str):
        return ""
    for keyword in keywords:
        text = text.replace(keyword, f"\033[1;31;40m{keyword}\033[0m")
    return text


def interactive_screening_abstract(df, keywords, output_file='table_3.3_screening_con_abstract_progress.csv'):
    """
    Screening para artículos CON abstract con capacidad para retomar progreso previo
    y registro de motivos de exclusión/duda
    
    Args:
        df (DataFrame): DataFrame con los artículos a clasificar
        keywords (list): Lista de palabras clave para resaltar
        output_file (str): Nombre del archivo CSV donde se guarda el progreso
        
    Returns:
        DataFrame: DataFrame con todas las clasificaciones y motivos
    """
    # Asegurarse de que exista la columna 'Motivo'
    if 'Motivo' not in df.columns:
        df['Motivo'] = np.nan
    
    # Verificar si existe un archivo de progreso previo
    if os.path.exists(output_file):
        print(f"Se encontró un archivo de progreso previo: {output_file}")
        try: 
            prev_progress = pd.read_csv(output_file, sep=";")
        except:
            prev_progress = pd.read_csv(output_file, sep=",")
        
        # Asegurar que la columna Motivo existe en el archivo de progreso
        if 'Motivo' not in prev_progress.columns:
            prev_progress['Motivo'] = np.nan
        
        # Identificar artículos ya clasificados (aquellos con decisión no nula)
        classified_articles = prev_progress[~prev_progress['decision'].isna()]
        pending_articles = df[~df.index.isin(classified_articles.index)]
        
        # Informar al usuario
        print(f"Artículos ya clasificados: {len(classified_articles)}")
        print(f"Artículos pendientes: {len(pending_articles)}")
        
        # Confirmar si quiere continuar donde lo dejó
        continue_choice = input("¿Deseas continuar donde lo dejaste? [y/n]: ").lower()
        
        if continue_choice == 'y':
            # Trabajar solo con los artículos pendientes
            working_df = pending_articles.copy()
            # Conservar las decisiones y motivos previos
            decision_dict = dict(zip(classified_articles.index, classified_articles['decision']))
            motivo_dict = dict(zip(classified_articles.index, 
                                  classified_articles['Motivo'].fillna('')))
        else:
            # Reiniciar desde el principio
            working_df = df.copy()
            decision_dict = {}
            motivo_dict = {}
    else:
        # No hay progreso previo, trabajar con todo el DataFrame
        working_df = df.copy()
        decision_dict = {}
        motivo_dict = {}
    
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
        print(f"--- ID del artículo: {idx} ---")
        print(f"\nTITLE:\n{title}")
        print(f"\nAUTHORS:\n{authors[:31]}..." if len(str(authors)) > 30 else f"\nAUTHORS:\n{authors}")
        print(f"\nDOI:\n{doi}")
        print(f"\nKeywords:\n{kwds}")
        
        highlighted_abstract = highlight_keywords(row['Abstract Note'], keywords)
        print(f"\nABSTRACT (palabras clave resaltadas):\n{highlighted_abstract}")
        
        choice = input("\nOpciones: [i]ncluir, [e]xcluir, [d]udoso, [s]alir: ").lower()

        # Si decisión es s: salir y guardar progreso
        if choice == 's':
            break

        # Registrar decisión
        decision_dict[idx] = 'dudoso' if choice == 'd' else ('include' if choice == 'i' else 'exclude')
        
        # Solicitar motivo para exclusiones y dudosos
        motivo = ""
        if choice in ['e', 'd']:
            motivo_prompt = "Excluido por: " if choice == 'e' else "Dudoso porque: "
            motivo = input(f"\n{motivo_prompt}")
            motivo_dict[idx] = motivo
        
        # Actualizar DataFrame completo con todas las decisiones y motivos
        result_df = df.copy()
        for i, decision in decision_dict.items():
            result_df.at[i, 'decision'] = decision
            if i in motivo_dict and motivo_dict[i]:  # Solo si hay motivo registrado
                result_df.at[i, 'Motivo'] = motivo_dict[i]
        
        # Guardar progreso después de cada decisión
        result_df.to_csv(output_file, index=False, sep=";")
        
        # Guardar progreso adicional cada 10 artículos
        if count % 10 == 0:
            print(f"\n--- Progreso guardado: {count} artículos revisados en esta sesión ---")
    
    # Actualizar el DataFrame completo con todas las decisiones y motivos finales
    result_df = df.copy()
    for i, decision in decision_dict.items():
        result_df.at[i, 'decision'] = decision
        if i in motivo_dict and motivo_dict[i]:
            result_df.at[i, 'Motivo'] = motivo_dict[i]
    
    # Guardar progreso final
    result_df.to_csv(output_file, index=False, sep=";")
    
    # Mostrar estadísticas
    stats = {
        'total': len(result_df),
        'clasificados': sum(~result_df['decision'].isna()),
        'pendientes': sum(result_df['decision'].isna()),
        'incluidos': sum(result_df['decision'] == 'include'),
        'excluidos': sum(result_df['decision'] == 'exclude'),
        'dudosos': sum(result_df['decision'] == 'dudoso')
    }
    
    print("\n=== ESTADÍSTICAS DE SCREENING ===")
    print(f"Total artículos: {stats['total']}")
    print(f"Artículos clasificados: {stats['clasificados']} ({stats['clasificados']/stats['total']*100:.1f}%)")
    print(f"Artículos incluidos: {stats['incluidos']}")
    print(f"Artículos excluidos: {stats['excluidos']}")
    print(f"Artículos dudosos: {stats['dudosos']}")
    print(f"Artículos pendientes: {stats['pendientes']}")
    
    return result_df
