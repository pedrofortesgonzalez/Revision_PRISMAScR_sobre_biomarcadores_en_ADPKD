# Anexo 5: Resultados Finales de la Revisión

Resultados finales derivados del análisis de los estudios incluidos en la revisión sistemática sobre biomarcadores en ADPKD.

## Estructura y contenido del directorio

```
Anexo_5_full_text_screening/
│
├── README.md
│
├── Anexo_5_notebook1_tablas.ipynb          # notebook para crear tablas con resultados del full text screening
│
├── Anexo_5_notebook2_figuras.ipynb         # notebook para crear figuras con resultados del full text screening
|
├── Anexo_5_tables_udfs.py                  # funciones auxiliares para crear figuras del notebook 1
|
├── Anexo_5_plotting_udfs.py                # funciones auxiliares para crear figuras del notebook 2
|
└── Anexo_5_carpeta_1_resultados/           # archivos de salida que sirven para construir figuras y tablas
    |
    ├── tabla_1_constructs.csv              # sirve para construir tabla 1 del TFM
    ├── tabla_2_search_results.csv          # sirve para construir tabla 2 del TFM
    ├── tabla_3_articles.csv                # sirve para construir tabla 3 del TFM
    ├── tabla_4_biomarkers.csv              # sirve para construir tabla 4 del TFM
    ├── tabla_5_stats.csv                   # sirve para construir la figura 1 del TFM
    |
    ├── fig1_flowchart.png                  # diagrama de flujo PRISMA
    ├── fig2_techniques_barplot.png         # diagrama de barras de técnicas y campos de estudio
    └── fig3_biomarkers_barplot.png         # diagrama de barras con tipos de biomarcadores y muestras
```


## Dependencias

```python
import re, os, pandas, numpy, matplotlib, seaborn, collections
```

---

*Este README forma parte de la documentación del proyecto de revisión sistemática sobre biomarcadores en ADPKD.*
