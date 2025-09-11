# Anexo 1: Construcción de Queries

Generación y procesamiento de queries de búsqueda bibliográfica para PubMed y Web of Science.

## Estructura del Directorio

```
Anexo_1_construir_queries/
├── README.md
├── fase_1_s1_generar_queries.ipynb
├── fase_1_carpeta_1_constructos/
│   ├── constructo_1_mesh_kidney_diseases.txt
│   ├── constructo_2_adpkd.txt
│   ├── constructo_3_genes.txt
│   ├── constructo_4_omicas_bio_computacional.txt
│   └── constructo_5_biomarcadores.txt
├── fase_1_carpeta_2_PubMed_queries/
│   ├── PM_query_1.txt
│   ├── PM_query_2.txt
│   ├── PM_query_3.txt
│   ├── PM_query_4.txt
│   └── PM_query_5.txt
└── fase_1_carpeta_3_WOS_queries/
    ├── WOS_query_1.txt
    ├── WOS_query_2.txt
    ├── WOS_query_3.txt
    ├── WOS_query_4.txt
    └── WOS_query_5.txt
```

## Archivos Principales

### fase_1_s1_generar_queries.ipynb
Notebook Jupyter que implementa el flujo de trabajo para:
- Generación de queries para diferentes bases de datos
- Procesamiento y conversión de formatos
- Exportación de queries a archivos de texto

## Uso

1. El proceso completo se ejecuta a través del notebook `fase_1_s1_generar_queries.ipynb`
2. Las queries generadas se guardan en archivos de texto separados en el directorio correspondiente

## Dependencias

```python
import os, sys, session_info, re
```
