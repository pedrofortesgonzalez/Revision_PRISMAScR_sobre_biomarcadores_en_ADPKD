# Anexo 2: Búsqueda en Bases de Datos

Resultados y preprocesamiento de las búsquedas sistemáticas realizadas en PubMed y WOS.

## Estructura del Directorio

```
Anexo_3_tiab_screening/
│
├── README.md
│
├── Anexo_2_notebook1_revisar_duplicados.ipynb    # notebook para procesar resultados de búsqueda bibliográficas
│
├── Anexo_2_carpeta_1_historiales_busqueda/
│   ├── tabla_2.1_PubMed_Search_History.csv       # estrategia de búsqueda utilizada en PubMed
│   ├── tabla_2.2_WOS_Search_History.csv          # estrategia de búsqueda utilizada en WOS
│   └── tabla_2.3_deduplication.csv               # archivos de entrada para deduplicado de resultados de búsquedas
│
└── Anexo_2_carpeta_2_resultados/                 # archivo de estadísticas de la búsqueda
    └── tabla_2.4_search_stats.csv
```

## Metodología

La búsqueda sistemática se realizó siguiendo las directrices PRISMA-ScR (*Preferred Reporting Items for Systematic Reviews and Meta-Analyses extension for Scoping Reviews*) para garantizar:
- Búsquedas realizadas en: MEDLINE (vía PubMed) y Web of Science
- Reproducibilidad de la metodología
- Documentación completa de los resultados

## Dependencias

```python
import os, sys, session_info, re
```

---
*Este README forma parte de la documentación del proyecto de revisión sistemática sobre biomarcadores en ADPKD.*
