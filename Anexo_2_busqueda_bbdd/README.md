# Anexo 2: Búsqueda en Bases de Datos

Ejecución de búsquedas bibliográficas en bases de datos científicas y procesamiento de resultados para la revisión PRISMA ScR sobre biomarcadores en ADPKD (Enfermedad Renal Poliquística Autosómica Dominante).

## Estructura del Directorio

```
Anexo_2_busqueda_bbdd/
│
├── README.md
│
├── fase_2_s1_revisar_duplicados.ipynb
│
├── Anexo_2_carpeta_1_historiales_busqueda/
│   ├── tabla_2.1_PubMed_Search_History.csv
│   ├── tabla_2.2_WOS_Search_History.csv
│   └── tabla_2.3_deduplication.csv
│
└── Anexo_2_carpeta_2_resultados/
    └── tabla_2.4_search_stats.csv
```

## Descripción del Proceso

Este anexo contiene el proceso de búsqueda bibliográfica sistemática para identificar estudios sobre biomarcadores en ADPKD. El flujo de trabajo incluye:

1. **Ejecución de búsquedas** en las principales bases de datos biomédicas (PubMed y Web of Science)
2. **Procesamiento de resultados** y extracción de estadísticas de búsqueda
3. **Deduplicación** de registros para eliminar artículos duplicados entre bases de datos
4. **Generación de estadísticas** finales para el reporte PRISMA

## Archivos Principales

### fase_2_s1_revisar_duplicados.ipynb
Notebook Jupyter que implementa el flujo de trabajo completo para:
- Importar y procesar historiales de búsqueda de PubMed y Web of Science
- Generar estadísticas descriptivas de los resultados de búsqueda
- Realizar deduplicación de registros basada en DOI
- Exportar tablas de estadísticas finales

### Anexo_2_carpeta_1_historiales_busqueda/
Contiene los archivos CSV con los historiales de búsqueda exportados directamente de las bases de datos:
- **tabla_2.1_PubMed_Search_History.csv**: Historial completo de búsquedas en PubMed
- **tabla_2.2_WOS_Search_History.csv**: Historial completo de búsquedas en Web of Science
- **tabla_2.3_deduplication.csv**: Conjunto de registros combinado para deduplicación

### Anexo_2_carpeta_2_resultados/
Contiene los resultados procesados:
- **tabla_2.4_search_stats.csv**: Estadísticas finales de búsqueda incluyendo totales por base de datos y después de deduplicación

## Bases de Datos Utilizadas

- **PubMed**: Base de datos principal de literatura biomédica (MEDLINE)
- **Web of Science (WOS)**: Base de datos multidisciplinaria de citaciones científicas

## Estrategia de Búsqueda

La estrategia de búsqueda se basa en cinco constructos principales desarrollados en el Anexo 1:
1. Enfermedades renales genéticas/congénitas (términos MeSH)
2. ADPKD y enfermedades quísticas renales
3. Genes implicados (PKD1, PKD2)
4. Ómicas y biología computacional
5. Biomarcadores y endofenotipos

## Uso

1. Ejecutar las búsquedas en PubMed y Web of Science utilizando las queries del Anexo 1
2. Exportar los historiales de búsqueda y guardarlos en `Anexo_2_carpeta_1_historiales_busqueda/`
3. Ejecutar el notebook `fase_2_s1_revisar_duplicados.ipynb` para procesar los resultados
4. Los resultados finales se generan automáticamente en `Anexo_2_carpeta_2_resultados/`

## Dependencias

```python
import os, sys, pandas as pd
```

## Contexto de la Revisión

Esta búsqueda forma parte de una revisión sistemática tipo PRISMA ScR (Scoping Review) que tiene como objetivo mapear la evidencia disponible sobre biomarcadores en la Enfermedad Renal Poliquística Autosómica Dominante (ADPKD). La ADPKD es la enfermedad renal hereditaria más común y la búsqueda sistemática de biomarcadores es crucial para identificar herramientas diagnósticas, pronósticas y de seguimiento de la enfermedad.