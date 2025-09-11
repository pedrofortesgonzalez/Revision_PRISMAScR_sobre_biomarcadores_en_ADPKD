#!/usr/bin/env python
# coding: utf-8

"""
Módulo con funciones para el procesamiento y conversión de consultas bibliográficas.
Incluye funciones para limpiar encabezados, convertir formato de términos y traducir
entre sintaxis de diferentes bases de datos.
"""

import re, pandas as pd
from typing import Optional

def viz():
    """
    Amplía las visualizaciones por defecto de pandas para mejorar la consulta de DataFrames directamente en el notebook, sin resultados acortados.
    """
    pd.set_option('display.max_rows', None)       # show all rows
    pd.set_option('display.max_columns', None)    # show all cols
    pd.set_option('display.width', None)          # not restricting width
    pd.set_option('display.max_colwidth', None)   # show all content in every cell
    

def rm_head(string: str) -> str:
    """
    Elimina encabezados que comienzan con # de un texto.
    
    Args:
        string (str): Texto de entrada que puede contener encabezados
        
    Returns:
        str: Texto sin los encabezados que comenzaban con #
        
    Example:
        >>> text = "#Header\\nContent\\n#Another header\\nMore content"
        >>> rm_head(text)
        'Content\\nMore content'
    """
    header = r'^#.*$'
    string = re.sub(pattern=header, repl='', string=string, flags=re.MULTILINE)
    return string.strip()

def convertir(query: str) -> str:
    """
    Convierte términos entrecomillados a formato con llaves, excepto si terminan en asterisco.
    
    Args:
        query (str): Consulta con términos entrecomillados
        
    Returns:
        str: Consulta con términos convertidos a formato de llaves
        
    Example:
        >>> query = 'TITLE-ABS-KEY("biomarker" OR "protein*")'
        >>> convertir(query)
        'TITLE-ABS-KEY({biomarker} OR "protein*")'
    """
    def rep_comillas(match: re.Match) -> str:
        """Función auxiliar para procesar cada coincidencia."""
        term = match.group(1)
        return f'"{term}"' if term.endswith('*') else f'{{{term}}}'
    
    return re.sub(r'"([^"]+)"', rep_comillas, query)

def sp2wos(scopus_query: str) -> str:
    """
    Traduce una consulta de formato Scopus a formato Web of Science.
    
    Args:
        scopus_query (str): Consulta en formato Scopus
        
    Returns:
        str: Consulta traducida a formato Web of Science
        
    Example:
        >>> sp2wos('TITLE-ABS-KEY({biomarker})')
        'TS="biomarker"'
    """
    wos_query = scopus_query.replace('{', '"')
    wos_query = wos_query.replace('}', '"')
    wos_query = wos_query.replace('TITLE-ABS-KEY', 'TS=')
    return wos_query