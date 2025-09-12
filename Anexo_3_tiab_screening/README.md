# Anexo 3: Screening de títulos y abstracts (`Anexo_3_tiab_screening`)

Notebooks, datos y resultados del proceso de **screening de títulos y abstracts** para la revisión PRISMA-ScR sobre biomarcadores en ADPKD.

## Estructura de la carpeta

- `anexo_3_udfs.py`: funciones principales para el screening interactivo y recuperación de abstracts.
- `tabla_3.3_screening_con_abstract_progress.csv`: archivo de progreso y resultados del screening (se genera automáticamente).
- Otros scripts y archivos auxiliares.

## ¿Qué contiene?

- **Scripts de screening** para facilitar la inclusión/exclusión de artículos basada en su título, autores y abstract.
- Utilidades para resaltar palabras clave, registrar motivos de exclusión y guardar el progreso.
- Ejemplo de uso interactivo en terminal.

## Requisitos y dependencias

- Python ≥ 3.8
- Paquetes recomendados:
  - `numpy`
  - `pandas`
  - `requests`
  - `tqdm`
  - `semanticscholar` (opcional, para recuperar abstracts desde Semantic Scholar)

Instala las dependencias con:
```bash
pip install -r requirements.txt
```
o manualmente:
```bash
pip install numpy pandas requests tqdm semanticscholar
```

## Uso básico

1. **Preparar el archivo de entrada:**  
   Asegúrate de tener un archivo CSV con los artículos a revisar. Debe contener, al menos: `Title`, `Author`, `DOI`, `Manual Tags`, `Abstract Note`.
2. **Ejecutar el script principal:**
   ```bash
   python screening_functions.py
   ```
   Sigue las instrucciones en pantalla para clasificar los artículos.

3. El progreso se guarda automáticamente en `table_3.3_screening_con_abstract_progress.csv` y puede retomarse en futuras sesiones.

## Personalización

- Puedes modificar la lista de palabras clave que se resaltan en los abstracts.
- El screening permite registrar motivos personalizados de exclusión o duda.

## Resultados

- El archivo CSV final contiene, para cada artículo:
  - Decisión (`include`, `exclude`, `dudoso`)
  - Motivo (si aplica)
  - Progreso y estadísticas automáticas
