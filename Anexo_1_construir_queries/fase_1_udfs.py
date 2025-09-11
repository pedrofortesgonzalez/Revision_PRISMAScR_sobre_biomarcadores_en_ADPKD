#!/usr/bin/env python
# coding: utf-8

"""
Módulo con funciones para el procesamiento y conversión de consultas bibliográficas.
Incluye funciones para limpiar encabezados, convertir formato de términos y traducir
entre sintaxis de diferentes bases de datos.
"""

import re
   

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