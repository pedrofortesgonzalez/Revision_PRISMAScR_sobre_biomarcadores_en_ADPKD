#!/usr/bin/env python
# coding: utf-8

# importar librerías
import re
import sys

################################################################################################################################################
# UDFs
def rm_head(string):
    """Quita encabezados de .txt que comiencen por #"""
    
    # definir regex para reconocer headers (partes a eliminar de los .txt de los constructos)
    header = r'^#.*$'
    # sustituir por '' con re.sub
    string = re.sub(pattern=header, repl = '', string = string, flags = re.MULTILINE)
    # limpiar espacios en blanco al inicio y al final
    string = string.strip()
    # devolver resultado
    return string

################################################################################################################################################
# sustituir "" por {} con UDFs
## función ppal
def convertir(query):
    ## función secundaria
    def rep_comillas(match):
        # guardamos en variable el grupo 1 (texto entrecomillado)
        term = match.group(1)
        ## si acaba en asterisco, lo dejamos entrecomillado
        if term.endswith('*'):
            return f'"{term}"'
        ## si no, sustituimos llaves por comillas
        else:
            return f'{{{term}}}'
    ## una vez definida, aplicamos función secundaria en la ppal
    return re.sub(r'"([^"]+)"', rep_comillas, query)

################################################################################################################################################
# defino UDF con opearciones para traducir de scopus a wos
def sp2wos(spq):
    wosq = spq.replace('{', '"')
    wosq = wosq.replace('}', '"')
    wosq = wosq.replace('TITLE-ABS-KEY', 'TS=')
    return wosq
