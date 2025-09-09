# Revisión PRISMA-ScR sobre Biomarcadores en ADPKD

Este repositorio contiene la estructura completa para realizar una revisión sistemática siguiendo las guías PRISMA-ScR (Preferred Reporting Items for Systematic Reviews and Meta-Analyses extension for Scoping Reviews) sobre biomarcadores en enfermedad poliquística renal autosómica dominante (ADPKD).

## Estructura del Proyecto

El proyecto está organizado en 5 fases principales, cada una con su propia carpeta y herramientas específicas:

### 1. 📝 Construcción de Queries (`construir_queries/`)
- **Objetivo**: Diseñar y generar queries de búsqueda para diferentes bases de datos
- **Componentes**:
  - `constructos/` - Constructos y términos de búsqueda
  - `PubMed_queries/` - Queries específicas para PubMed
  - `WOS_queries/` - Queries para Web of Science
  - `notebook1_generar_queries.ipynb` - Notebook para generación de queries
  - `udfs.py` - Funciones auxiliares

### 2. 🔍 Búsqueda en Bases de Datos (`busqueda_bbdd/`)
- **Objetivo**: Gestionar resultados de búsqueda y eliminar duplicados
- **Componentes**:
  - `historiales_busqueda/` - Registros de búsquedas realizadas
  - `resultados/` - Resultados procesados
  - `inputs/` - Archivos de entrada desde bases de datos
  - `notebook1_revisar_duplicados.ipynb` - Identificación y eliminación de duplicados

### 3. 📋 Screening de Títulos y Abstracts (`tiab_screening/`)
- **Objetivo**: Evaluar relevancia basada en títulos y abstracts
- **Componentes**:
  - `resultados/` - Resultados del screening
  - `notebook1_recuperar_abstracts.ipynb` - Recuperación automática de abstracts
  - `notebook2_tiab_screening.ipynb` - Proceso de screening TIAB
  - `udfs_1.py` - Funciones para recuperación de abstracts
  - `udfs_2.py` - Funciones para screening

### 4. 📄 Screening de Texto Completo (`full_text_screening/`)
- **Objetivo**: Evaluación detallada de artículos completos
- **Componentes**:
  - `inputs/` - Archivos PDF de artículos
  - `resultados/` - Decisiones finales de inclusión/exclusión
  - `notebook1_full_text_screening.ipynb` - Proceso de screening completo
  - `udfs.py` - Funciones para procesamiento de PDFs y screening

### 5. 📊 Análisis de Resultados (`resultados/`)
- **Objetivo**: Generar tablas, figuras y análisis finales
- **Componentes**:
  - `resultados/` - Archivos de salida finales
  - `notebook1_tablas.ipynb` - Generación de tablas
  - `notebook2_figuras.ipynb` - Creación de visualizaciones
  - `tables_udfs.py` - Funciones para tablas
  - `plotting_udfs.py` - Funciones para gráficos

## Flujo de Trabajo

1. **Definir Constructos** → Establecer términos de búsqueda y estrategias
2. **Generar Queries** → Crear queries específicas para cada base de datos
3. **Búsqueda** → Ejecutar búsquedas y descargar resultados
4. **Deduplicación** → Identificar y eliminar registros duplicados
5. **Screening TIAB** → Evaluar relevancia por título/abstract
6. **Screening Completo** → Evaluación detallada de textos completos
7. **Extracción de Datos** → Extraer información relevante
8. **Análisis y Síntesis** → Generar tablas, figuras y conclusiones

## Tecnologías Utilizadas

- **Python 3.8+** - Lenguaje principal
- **Jupyter Notebooks** - Análisis interactivo
- **Pandas** - Manipulación de datos
- **Matplotlib/Seaborn** - Visualizaciones estáticas
- **Plotly** - Visualizaciones interactivas
- **Scikit-learn** - Análisis de concordancia
- **PyPDF2/textract** - Procesamiento de PDFs

## Instalación y Uso

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/pedrofortesgonzalez/Revision_PRISMAScR_sobre_biomarcadores_en_ADPKD.git
   cd Revision_PRISMAScR_sobre_biomarcadores_en_ADPKD
   ```

2. **Instalar dependencias**:
   ```bash
   pip install pandas numpy matplotlib seaborn plotly scikit-learn jupyter
   pip install PyPDF2 textract requests
   ```

3. **Ejecutar notebooks en orden**:
   - Comenzar con `construir_queries/notebook1_generar_queries.ipynb`
   - Continuar secuencialmente a través de cada fase

## Archivos de Entrada Esperados

- **Búsquedas**: Archivos CSV o Excel con resultados de bases de datos
- **PDFs**: Artículos en texto completo para screening final
- **Metadatos**: Información bibliográfica completa

## Salidas Generadas

- **Tablas**: Características de estudios, biomarcadores, calidad metodológica
- **Figuras**: Diagrama PRISMA, distribuciones, mapas de evidencia
- **Reportes**: Documentación completa del proceso
- **Dashboard**: Visualización interactiva de resultados

## Guías Seguidas

Este proyecto sigue las recomendaciones de:
- **PRISMA-ScR**: Para reporting de scoping reviews
- **Cochrane Handbook**: Para métodos de revisión sistemática
- **JBI Manual**: Para scoping reviews

## Contribuciones

Para contribuir al proyecto:
1. Fork el repositorio
2. Crear una rama feature
3. Hacer commit de cambios
4. Enviar pull request

## Licencia

[Especificar licencia del proyecto]

## Contacto

[Información de contacto del equipo de investigación]