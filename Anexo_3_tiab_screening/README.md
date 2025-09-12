# Anexo 3: Screening de títulos y abstracts (`Anexo_3_tiab_screening`)

Notebooks, datos y resultados del proceso de **screening de títulos y abstracts** para la revisión PRISMA-ScR sobre biomarcadores en ADPKD.

## Estructura de la carpeta

```
Anexo_3_tiab_screening/
│
├── README.md
│
├── Anexo_3_notebook1_recuperar_abstracts.ipynb   # notebook para pre-procesado del screening, incluyendo recuperación de abstacts
│
├── Anexo_3_notebook2_tiab_screening.ipynb        # notebook de screening interactivo
│
├── Anexo_3_udfs.py                               # funciones auxiliares para los notebooks
│
├── Anexo_3_dicts_resultados.ipynb                # diccionario para análisis de resultados del screening
│
├── Anexo_3_carpeta_1_inputs/                     # archivos de entrada y para tiab screening
│   ├── tabla_3.0_articulos_pre_revision.csv
│   ├── tabla_3.1_articulos_con_abstract.csv
│   ├── tabla_3.2_articulos_sin_abstract.csv
│   ├── tabla_3.2.2_abs_rec_wos.csv
│   ├── tabla_3.3.1_articulos_para_screening.csv
│   └── tabla_3.3.2.stats.csv
│
└── Anexo_3_carpeta_2_resultados/                 # archivos de salida y auto-guardado del tiab screening
    ├── tabla_3.4_screening_wip.csv
    ├── tabla_3.5.1_include.csv
    ├── tabla_3.5.2_exclude.csv
    └── tabla_3.5.3_stats_2.csv
```

## Requisitos y dependencias
```
import numpy, pandas, requests, tqdm, semanticscholar
```

