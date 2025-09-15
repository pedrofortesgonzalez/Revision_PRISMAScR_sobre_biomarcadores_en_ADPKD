#!/usr/bin/env python
# coding: utf-8

# imports
import pandas as pd
import re


# Crear tabla de extracción para biomarcadores
def create_biomarker_extraction_table():
    """
    Crea un DataFrame vacío de pandas para la extracción de biomarcadores.

    Returns:
        pandas.DataFrame: DataFrame con las columnas relevantes para extraer información sobre biomarcadores, 
        como nombre, tipo, muestra, técnica de detección, estadio de la enfermedad, ventajas, limitaciones y aplicación clínica.
    """
    
    columns = [
        'article_id',          # ID único del artículo
        'journal'
        'biomarker_name',      # Nombre del biomarcador
        'biomarker_type',      # Genético, Proteómico, Metabolómico, Imagen, etc.
        'sample_type',         # Sangre, Orina, Tejido, etc.
        'detection_technique', # Técnica utilizada para medirlo
        'disease_stage',       # Fase de la enfermedad donde es útil
        'advantages',          # Ventajas del biomarcador
        'limitations',         # Limitaciones
        'clinical_application' # Aplicación clínica/traslacional
    ]
    
    biomarkers_df = pd.DataFrame(columns=columns)
    return biomarkers_df



# Crear tabla de extracción para estudios
def create_study_extraction_table():
    """
    Crea un DataFrame vacío de pandas para la extracción de información sobre estudios.

    Returns:
        pandas.DataFrame: DataFrame con las columnas relevantes para extraer información de artículos científicos, 
        como autor, año, título, diseño, tamaños muestrales, criterios de inclusión, técnicas ómicas, hallazgos y aplicaciones traslacionales.
    """
    
    columns = [
        'article_id',           # ID único del artículo
        'author',               # Primer autor
        'year',                 # Año de publicación
        'title',                # Título completo
        'journal',              # Revista
        'doi',                  # DOI
        'study_design',         # Diseño del estudio
        'sample_size_adpkd',    # n en grupo ADPKD
        'sample_size_control',  # n en grupo control
        'inclusion_criteria',   # Criterios de inclusión
        'omics_technique',      # Técnica ómica/bioinformática
        'main_findings',        # Hallazgos principales
        'translational_apps',   # Aplicaciones traslacionales
        'notes'                 # Notas adicionales
    ]
    
    studies_df = pd.DataFrame(columns=columns)
    return studies_df



def choose_study(autor, year, df):
    """
    Selecciona un estudio en el DataFrame que coincide con el autor y año indicados.

    Args:
        autor (str): Nombre del primer autor del estudio.
        year (int): Año de publicación del estudio.
        df (pandas.DataFrame): DataFrame con los estudios.

    Returns:
        pandas.DataFrame: Subconjunto del DataFrame correspondiente al estudio seleccionado.
    """
    c1 = df["Author"].str.startswith(autor)
    c2 = df["Publication Year"]== year
    study = df.loc[c1 & c2]
    return study



def add_study(article_id, author, year, title, journal, doi, study_design, 
              sample_adpkd, sample_control, inclusion_criteria, omics_technique, 
              findings, applications, notes=""):
    """
    Añade un nuevo estudio a la tabla de extracción de estudios y lo guarda en CSV.

    Args:
        article_id (str): Identificador único del artículo.
        author (str): Nombre del primer autor.
        year (int): Año de publicación.
        title (str): Título del estudio.
        journal (str): Revista donde se publicó.
        doi (str): DOI del estudio.
        study_design (str): Tipo de diseño del estudio.
        sample_adpkd (str/int): Número de pacientes ADPKD.
        sample_control (str/int): Número de controles.
        inclusion_criteria (str): Criterios de inclusión.
        omics_technique (str/list): Técnicas ómicas/bioinformáticas empleadas.
        findings (str): Hallazgos principales.
        applications (str): Aplicaciones traslacionales.
        notes (str, opcional): Notas adicionales.

    Returns:
        pandas.DataFrame: DataFrame actualizado con el estudio añadido.
    """
    
    # Cargar tabla actual
    try:
        studies_df = pd.read_csv('Anexo_4_carpeta_1_resultados/tabla_4.4_studies_extraction.csv')
    except:
        studies_df = create_study_extraction_table()
    
    # Crear nueva fila con los datos del estudio
    new_row = {
        'article_id': article_id,
        'author': author,
        'year': year,
        'title': title,
        'journal': journal,
        'doi': doi,
        'study_design': study_design,
        'sample_size_adpkd': sample_adpkd,
        'sample_size_control': sample_control,
        'inclusion_criteria': inclusion_criteria,
        'omics_technique': omics_technique,
        'main_findings': findings,
        'translational_apps': applications,
        'notes': notes
    }
    
    # Añadir la nueva fila
    studies_df = pd.concat([studies_df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Guardar la tabla actualizada
    studies_df.to_csv('Anexo_4_carpeta_1_resultados/tabla_4.4_studies_extraction.csv', index=False)
    
    print(f"Estudio '{author}, {year}' añadido correctamente (ID: {article_id}).")
    return studies_df


    
def review(autor, year, include, exclude, reviewed, studies_df):
    """
    Permite revisar un estudio para decidir su inclusión/exclusión en el screening y registrar el motivo.

    Args:
        autor (str): Nombre del primer autor.
        year (int): Año de publicación.
        include (pandas.DataFrame): Tabla de estudios candidatos a incluir.
        exclude (pandas.DataFrame): Tabla de estudios excluidos.
        reviewed (pandas.DataFrame): Tabla de estudios ya revisados.
        studies_df (pandas.DataFrame): Tabla de extracción de estudios.

    Returns:
        tuple: Las tablas actualizadas (include, exclude, reviewed, study seleccionado, studies_df actualizado).
    """
    
    # Seleccionar estudio
    study = choose_study(autor, year, include)

    # Checkear resultado
    if len(study)==0:
        raise ValueError("Error: repasa los datos introducidos")
    else:
        print(f"\nTítulo: {study['Title'].iloc[0]}")
        print(f"\nAutor: {study['Author'].iloc[0]}")
        print(f"\nAño: {study['Publication Year'].iloc[0]}")

    # Decidir si incluir o excluir
    incluir = input("\nDeseas incluir el paper para revisión del texto completo? (y/n)")
    affirmative = ["y", "yes", "sí", "si"]

    # Excluir
    if incluir.casefold() not in affirmative:
        # Guardar los DOIs antes de modificar
        study_doi = study["DOI"].iloc[0] if len(study) > 0 and "DOI" in study.columns else None
        
        # Definir condición de filtrado y quitar de include
        c = include["DOI"].isin(study["DOI"])
        preinclude = include.shape[0]
        include = include.loc[~c]
        print(f"Include: {preinclude} --> {include.shape[0]}")
        
        ## Añadir a exclude
        preexclude = exclude.shape[0]
        exclude = pd.concat([exclude, study])
        print(f"Exclude: {preexclude} --> {exclude.shape[0]}")

        ## Reasignar sus valores de motivo de exclusión
        c = exclude["DOI"].isin(study["DOI"])
        exclude.loc[c, "DECISION"] = "exclude"
        current_vals = exclude["MOTIVO"].dropna().unique().tolist()
        
        # Mostrar opciones disponibles
        print("\nMotivos de exclusión disponibles:")
        for i, motivo in enumerate(current_vals, 1):
            print(f"{i}. {motivo}")
        print(f"{len(current_vals)+1}. Otro (personalizado)")
        
        # Pedir selección
        seleccion = input(
            "\nElige un motivo de exclusión (número) o escribe 'nuevo' para añadir uno personalizado: ")
        motivo_exclusion = None
        if seleccion.lower() == 'nuevo' or seleccion == str(len(current_vals)+1):
            # Añadir motivo personalizado
            motivo_exclusion = input("Introduce el nuevo motivo de exclusión: ")
            current_vals.append(motivo_exclusion)
        else:
            try:
                indice = int(seleccion) - 1
                if 0 <= indice < len(current_vals):
                    motivo_exclusion = current_vals[indice]
                else:
                    print("Selección no válida, usando 'Otros' como motivo.")
                    motivo_exclusion = "Otros"
            except ValueError:
                print("Entrada no válida, usando 'Otros' como motivo.")
                motivo_exclusion = "Otros"
        
        # Asignar el motivo al estudio recién excluido
        if study_doi and "DOI" in exclude.columns:
            exclude.loc[exclude["DOI"] == study_doi, "MOTIVO"] = motivo_exclusion
            exclude.loc[exclude["DOI"] == study_doi, "DECISION"] = "exclude"
        else:
            # Si no hay DOI, asumimos que es el último registro añadido
            exclude.iloc[-1, exclude.columns.get_loc("MOTIVO")] = motivo_exclusion
            if "DECISION" in exclude.columns:
                exclude.iloc[-1, exclude.columns.get_loc("DECISION")] = "exclude"
            else:
                exclude["DECISION"] = ""
                exclude.iloc[-1, exclude.columns.get_loc("DECISION")] = "exclude"

        # Guardar include y exclude como CSV
        include.to_csv('Anexo_4_carpeta_1_resultados/tabla_4.1_include.csv', index=False)
        exclude.to_csv('Anexo_4_carpeta_1_resultados/tabla_4.2_exclude.csv', index=False)
        
        return include, exclude, reviewed, study, studies_df
    
    # Incluir
    else:
        ## Introducir datos
        study_design=input("\nDiseño del estudio: ")
        sample_adpkd=input("\nn pacientes ADPKD: ")
        sample_control=input("\nn controles: ")
        inclusion_criteria=input("\nCriterios de inclusión: ")
        omics_technique=input("\nTécnicas / ómicas: ").split(", ")
        findings=input("\nHallazgos: ")
        applications=input("\nAplicaciones: ")

        ## Añadir estudio a la tabla studies_df (add_study ya devuelve esta función)
        regex = r"\b(\w+\s?\w*),.*\b"
        autor_surname = re.match(regex, autor).group(1)
        studies_df = add_study(
            article_id=autor+str(year), author=autor, year=year,
            title=study["Title"].iloc[0] if "Title" in study.columns and not study["Title"].empty else "",
            journal=study["Publication Title"].iloc[0] if "Publication Title" in study.columns and not study["Publication Title"].empty else "",
            doi=study["DOI"].iloc[0] if "DOI" in study.columns and not study["DOI"].empty else "",
            study_design=study_design, sample_adpkd=sample_adpkd, sample_control=sample_control, 
            inclusion_criteria=inclusion_criteria,
            omics_technique=omics_technique, findings=findings, applications=applications)

        # Quitar estudio de include y pasarlo a reviewed
        c = include["DOI"].isin(study["DOI"])
        preinclude = include.shape[0]
        include = include.loc[~c]
        print(f"Include: {preinclude} --> {include.shape[0]}")
        
        ## Añadir a reviewed
        prerev = reviewed.shape[0]
        reviewed = pd.concat([reviewed, study])
        print(f"Reviewed: {prerev} --> {reviewed.shape[0]}")
        
        # Guardar dfs
        include.to_csv('Anexo_4_carpeta_1_resultados/tabla_4.1_include.csv', index=False)
        reviewed.to_csv('Anexo_4_carpeta_1_resultados/tabla_4.3_reviewed.csv', index=False)
        studies_df.to_csv('Anexo_4_carpeta_1_resultados/tabla_4.4_studies_extraction.csv', index=False)
        
        return include, exclude, reviewed, study, studies_df



def reload():
    """
    Recarga las tablas de inclusión, exclusión, revisados, estudios y biomarcadores desde los archivos CSV correspondientes.

    Returns:
        tuple: Las tablas pandas.DataFrame recargadas en el siguiente orden:
            include, exclude, reviewed, studies_df, biomarkers_df
    """
    
    try:
        include = pd.read_csv('Anexo_4_carpeta_1_resultados/tabla_4.1_include.csv', sep=",")
    except:
        include = pd.read_csv('Anexo_4_carpeta_1_resultados/tabla_4.1_include.csv', sep=";")

    try:
        exclude = pd.read_csv('Anexo_4_carpeta_1_resultados/tabla_4.2_exclude.csv', sep=",")
    except:
        exclude = pd.read_csv('Anexo_4_carpeta_1_resultados/tabla_4.2_exclude.csv', sep=";")

    try:
        reviewed = pd.read_csv('Anexo_4_carpeta_1_resultados/tabla_4.3_reviewed.csv', sep=",")
    except:
        reviewed = pd.read_csv('Anexo_4_carpeta_1_resultados/tabla_4.3_reviewed.csv', sep=";")
    
    try:
        studies_df = pd.read_csv("Anexo_4_carpeta_1_resultados/tabla_4.4_studies_extraction.csv", sep=",")
    except:
        studies_df = pd.read_csv("Anexo_4_carpeta_1_resultados/tabla_4.4_studies_extraction.csv", sep=";")
    
    try:
        biomarkers_df = pd.read_csv("Anexo_4_carpeta_1_resultados/tabla_4.5_biomarkers_extraction.csv", sep=",")
    except:
        biomarkers_df = pd.read_csv("Anexo_4_carpeta_1_resultados/tabla_4.5_biomarkers_extraction.csv", sep=";")

    return include, exclude, reviewed, studies_df, biomarkers_df

    

def add_biomarker(article_id, name, biomarker_type, sample_type, technique, 
                 disease_stage, advantages, limitations, validation, application):
    """
    Añade un nuevo biomarcador a la tabla de biomarcadores y guarda el resultado en CSV.

    Args:
        article_id (str): Identificador del artículo asociado.
        name (str): Nombre del biomarcador.
        biomarker_type (str): Tipo de biomarcador (genético, proteico, etc).
        sample_type (str): Tipo de muestra utilizada.
        technique (str): Técnica de detección utilizada.
        disease_stage (str): Etapa de la enfermedad en la que se aplica.
        advantages (str): Ventajas del biomarcador.
        limitations (str): Limitaciones del biomarcador.
        validation (str): Estado de validación.
        application (str): Aplicación clínica o traslacional.

    Returns:
        pandas.DataFrame: DataFrame de biomarcadores actualizado.
    """
    
    # Cargar tabla actual
    try:
        biomarkers_df = pd.read_csv('Anexo_4_carpeta_1_resultados/tabla_4.5_biomarkers_extraction.csv')
    except:
        biomarkers_df = create_biomarker_extraction_table()
    
    # Crear nueva fila con los datos del biomarcador
    new_row = {
        'article_id': article_id,
        'biomarker_name': name,
        'biomarker_type': biomarker_type,
        'sample_type': sample_type,
        'detection_technique': technique,
        'disease_stage': disease_stage,
        'advantages': advantages,
        'limitations': limitations,
        'validation_status': validation,
        'clinical_application': application
    }
    
    # Añadir la nueva fila
    biomarkers_df = pd.concat([biomarkers_df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Guardar la tabla actualizada
    biomarkers_df.to_csv('Anexo_4_carpeta_1_resultados/tabla_4.5_biomarkers_extraction.csv', index=False)
    
    print(f"Biomarcador '{name}' añadido correctamente (asociado al artículo ID: {article_id}).")
    return biomarkers_df



def generate_summary_tables():
    """
    Genera tablas resumen de estudios y biomarcadores a partir de los datos extraídos y las guarda en CSV.

    Returns:
        tuple: DataFrames resumen de estudios y biomarcadores respectivamente.
    """
    
    try:
        # Cargar los datos
        studies_df = pd.read_csv('Anexo_4_carpeta_1_resultados/tabla_4.4_studies_extraction.csv')
        biomarkers_df = pd.read_csv('Anexo_4_carpeta_1_resultados/tabla_4.5_biomarkers_extraction.csv')
        
        # 1. Tabla resumen de estudios
        study_summary = studies_df[['author', 'year', 'study_design', 
                                   'sample_size_adpkd', 'sample_size_control',
                                   'omics_technique']]
        
        study_summary['sample'] = study_summary.apply(
            lambda x: f"{x['sample_size_adpkd']}/{x['sample_size_control']}", axis=1)
        
        study_summary = study_summary[['author', 'year', 'study_design', 
                                      'sample', 'omics_technique']]
        
        study_summary.columns = ['Autor', 'Año', 'Diseño', 'n (ADPKD/Control)', 
                               'Técnica principal', 'Calidad metodológica']
        
        # 2. Tabla resumen de biomarcadores
        # Contar en cuántos estudios aparece cada biomarcador
        biomarker_counts = biomarkers_df['biomarker_name'].value_counts().reset_index()
        biomarker_counts.columns = ['biomarker_name', 'count']
        
        # Agrupar por biomarcador
        biomarker_summary = biomarkers_df.groupby('biomarker_name').agg({
            'biomarker_type': 'first',
            'sample_type': lambda x: ', '.join(x.unique()),
            'clinical_application': lambda x: ', '.join(x.unique())
        }).reset_index()
        
        # Combinar con conteo
        biomarker_summary = biomarker_summary.merge(biomarker_counts, on='biomarker_name')
        
        biomarker_summary = biomarker_summary[[
            'biomarker_name', 'biomarker_type', 'sample_type', 'count', 'clinical_application'
        ]]
        
        biomarker_summary.columns = [
            'Biomarcador', 'Tipo', 'Muestra', 'Estudios (n)', 'Aplicaciones clínicas'
        ]
        
        # Guardar tablas resumen
        study_summary.to_csv('Anexo_4_carpeta_1_resultados/tabla_4.4_studies_extraction.csv', index=False)
        biomarker_summary.to_csv('Anexo_4_carpeta_1_resultados/tabla_4.5_biomarkers_extraction.csv', index=False)
        
        print("Tablas resumen generadas correctamente.")
        
        # Mostrar las primeras filas
        print("\nResumen de Estudios:")
        print(study_summary.head())
        
        print("\nResumen de Biomarcadores:")
        print(biomarker_summary.head())
        
    except Exception as e:
        print(f"Error al generar tablas resumen: {e}")
        
    return study_summary, biomarker_summary
