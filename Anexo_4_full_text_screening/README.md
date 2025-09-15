# Anexo 4: Screening de textos completos (`Anexo_4_full_text_screening`)

Notebooks, datos y resultados del proceso de **screening de textos completos** para la revisión PRISMA-ScR sobre biomarcadores en ADPKD.

## Estructura y contenido del directorio

```
Anexo_4_full_text_screening/
│
├── README.md
│
├── Anexo_4_notebook1_recuperar_abstracts.ipynb   # notebook para pre-procesado del screening, incluyendo recuperación de abstacts
│
├── Anexo_4_udfs.py                               # funciones auxiliares para los notebooks
│
└── Anexo_4_carpeta_1_resultados/                 # archivos de salida y auto-guardado del screening
    ├── tabla_4.1_include.csv
    ├── tabla_4.2_exclude.csv
    ├── tabla_4.3_reviewed.csv
    ├── tabla_4.4_studies_extraction.csv
    ├── tabla_4.5_biomarkers_extraction.csv
    └── tabla_4.6_stats.csv
```

## Metodología

El cribado de textos completos se realizó siguiendo estos pasos:

1. Evaluación de los textos completos de los estudios incluidos tras el *tiab screening* en la búsqueda sistemática aplicando los criterios de inclusión y exclusión previamente definidos.
2. Resolución de discrepancias mediante repaso de referencias cuya inclusión fuese dudosa.
3. Registro detallado de decisiones y razones de exclusión.

## Requisitos y dependencias

```python
import os, pandas, numpy, re
```
---
*Este README forma parte de la documentación del proyecto de revisión sistemática sobre biomarcadores en ADPKD.*


---
*Este README forma parte de la documentación del proyecto de revisión sistemática sobre biomarcadores en ADPKD.*
