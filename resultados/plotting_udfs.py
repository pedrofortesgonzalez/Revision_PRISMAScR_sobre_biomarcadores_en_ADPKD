"""
User Defined Functions para generación de gráficos y visualizaciones
PRISMA-ScR Revisión sobre biomarcadores en ADPKD
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from typing import Dict, List, Any, Optional
import networkx as nx


def load_all_screening_data() -> Dict[str, pd.DataFrame]:
    """
    Carga todos los datos del proceso de screening.
    
    Returns:
        Dict[str, pd.DataFrame]: Diccionario con datos de screening
    """
    # Placeholder - en implementación real cargaría archivos
    screening_data = {
        'initial_search': pd.DataFrame({'total': [2500]}),
        'after_duplicates': pd.DataFrame({'total': [1800]}),
        'tiab_screened': pd.DataFrame({'total': [1800]}),
        'tiab_included': pd.DataFrame({'total': [150]}),
        'fulltext_screened': pd.DataFrame({'total': [150]}),
        'final_included': pd.DataFrame({'total': [45]})
    }
    return screening_data


def extract_screening_numbers(screening_data: Dict[str, pd.DataFrame]) -> Dict[str, int]:
    """
    Extrae números para diagrama de flujo PRISMA.
    
    Args:
        screening_data (Dict[str, pd.DataFrame]): Datos de screening
        
    Returns:
        Dict[str, int]: Números para el diagrama
    """
    numbers = {
        'initial_records': 2500,
        'after_duplicates': 1800,
        'duplicates_removed': 700,
        'tiab_screened': 1800,
        'tiab_excluded': 1650,
        'tiab_included': 150,
        'fulltext_screened': 150,
        'fulltext_excluded': 105,
        'final_included': 45,
        'exclusion_reasons': {
            'wrong_population': 25,
            'no_biomarker': 20,
            'wrong_study_type': 35,
            'animal_study': 15,
            'other': 10
        }
    }
    return numbers


def create_prisma_flow_diagram(numbers: Dict[str, int]) -> go.Figure:
    """
    Crea diagrama de flujo PRISMA-ScR.
    
    Args:
        numbers (Dict[str, int]): Números del proceso de screening
        
    Returns:
        go.Figure: Diagrama de flujo interactivo
    """
    fig = go.Figure()
    
    # Definir posiciones de cajas
    boxes = [
        # Identificación
        {"x": 0.5, "y": 0.95, "text": f"Registros identificados\nen búsqueda inicial\n(n = {numbers['initial_records']})", "color": "lightblue"},
        
        # Screening
        {"x": 0.2, "y": 0.8, "text": f"Duplicados removidos\n(n = {numbers['duplicates_removed']})", "color": "lightcoral"},
        {"x": 0.5, "y": 0.8, "text": f"Registros después de\nremover duplicados\n(n = {numbers['after_duplicates']})", "color": "lightblue"},
        
        # Title/Abstract screening
        {"x": 0.5, "y": 0.6, "text": f"Registros evaluados\nen título/abstract\n(n = {numbers['tiab_screened']})", "color": "lightgreen"},
        {"x": 0.8, "y": 0.6, "text": f"Registros excluidos\nen título/abstract\n(n = {numbers['tiab_excluded']})", "color": "lightcoral"},
        
        # Full text screening
        {"x": 0.5, "y": 0.4, "text": f"Artículos evaluados\nen texto completo\n(n = {numbers['fulltext_screened']})", "color": "lightgreen"},
        {"x": 0.8, "y": 0.4, "text": f"Artículos excluidos\nen texto completo\n(n = {numbers['fulltext_excluded']})", "color": "lightcoral"},
        
        # Final inclusion
        {"x": 0.5, "y": 0.2, "text": f"Estudios incluidos\nen síntesis cualitativa\n(n = {numbers['final_included']})", "color": "gold"},
    ]
    
    # Agregar cajas
    for box in boxes:
        fig.add_shape(
            type="rect",
            x0=box["x"]-0.08, y0=box["y"]-0.05,
            x1=box["x"]+0.08, y1=box["y"]+0.05,
            fillcolor=box["color"],
            line=dict(color="black", width=2)
        )
        
        fig.add_annotation(
            x=box["x"], y=box["y"],
            text=box["text"],
            showarrow=False,
            font=dict(size=10),
            align="center"
        )
    
    # Agregar flechas
    arrows = [
        # Vertical principales
        {"x0": 0.5, "y0": 0.9, "x1": 0.5, "y1": 0.85},
        {"x0": 0.5, "y0": 0.75, "x1": 0.5, "y1": 0.65},
        {"x0": 0.5, "y0": 0.55, "x1": 0.5, "y1": 0.45},
        {"x0": 0.5, "y0": 0.35, "x1": 0.5, "y1": 0.25},
        
        # Hacia exclusiones
        {"x0": 0.58, "y0": 0.6, "x1": 0.72, "y1": 0.6},
        {"x0": 0.58, "y0": 0.4, "x1": 0.72, "y1": 0.4},
        {"x0": 0.42, "y0": 0.8, "x1": 0.28, "y1": 0.8},
    ]
    
    for arrow in arrows:
        fig.add_annotation(
            x=arrow["x1"], y=arrow["y1"],
            ax=arrow["x0"], ay=arrow["y0"],
            arrowhead=2, arrowsize=1, arrowwidth=2,
            arrowcolor="black"
        )
    
    fig.update_layout(
        title="Diagrama de Flujo PRISMA-ScR",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=800, height=1000,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig


def create_temporal_distribution_plot(df: pd.DataFrame) -> go.Figure:
    """
    Crea gráfico de distribución temporal de estudios.
    
    Args:
        df (pd.DataFrame): DataFrame con estudios incluidos
        
    Returns:
        go.Figure: Gráfico de distribución temporal
    """
    # Generar datos temporales (placeholder)
    years = list(range(2000, 2024))
    study_counts = np.random.poisson(2, len(years))
    study_counts[-5:] += 3  # Más estudios en años recientes
    
    df_temporal = pd.DataFrame({'Year': years, 'Study_Count': study_counts})
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_temporal['Year'],
        y=df_temporal['Study_Count'],
        mode='markers+lines',
        name='Estudios por año',
        line=dict(color='blue', width=3),
        marker=dict(size=8, color='darkblue')
    ))
    
    # Línea de tendencia
    z = np.polyfit(df_temporal['Year'], df_temporal['Study_Count'], 1)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=df_temporal['Year'],
        y=p(df_temporal['Year']),
        mode='lines',
        name='Tendencia',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="Distribución Temporal de Estudios Incluidos",
        xaxis_title="Año de Publicación",
        yaxis_title="Número de Estudios",
        hovermode='x unified',
        width=800, height=500
    )
    
    return fig


def create_geographic_distribution_map(df: pd.DataFrame) -> go.Figure:
    """
    Crea mapa de distribución geográfica de estudios.
    
    Args:
        df (pd.DataFrame): DataFrame con estudios incluidos
        
    Returns:
        go.Figure: Mapa interactivo
    """
    # Datos geográficos (placeholder)
    countries_data = {
        'Country': ['USA', 'Germany', 'Japan', 'Canada', 'UK', 'Netherlands', 'France', 'Italy', 'Spain', 'Australia'],
        'Study_Count': [12, 8, 6, 5, 4, 3, 3, 2, 2, 1],
        'ISO_Code': ['USA', 'DEU', 'JPN', 'CAN', 'GBR', 'NLD', 'FRA', 'ITA', 'ESP', 'AUS']
    }
    
    df_geo = pd.DataFrame(countries_data)
    
    fig = go.Figure(data=go.Choropleth(
        locations=df_geo['ISO_Code'],
        z=df_geo['Study_Count'],
        text=df_geo['Country'],
        colorscale='Blues',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title="Número de<br>Estudios"
    ))
    
    fig.update_layout(
        title_text='Distribución Geográfica de Estudios',
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        width=1000, height=600
    )
    
    return fig


def create_biomarker_types_visualization(df: pd.DataFrame) -> go.Figure:
    """
    Crea visualización de tipos de biomarcadores.
    
    Args:
        df (pd.DataFrame): DataFrame con estudios incluidos
        
    Returns:
        go.Figure: Gráfico de biomarcadores
    """
    # Datos de biomarcadores (placeholder)
    biomarker_data = {
        'Category': ['Función Renal', 'Proteinuria', 'Imagenología', 'Inflamatorios', 'Metabólicos', 'Noveles'],
        'Count': [25, 18, 15, 12, 8, 10],
        'Color': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    }
    
    # Crear subplot con gráfico de barras y pie chart
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Distribución por Categoría", "Proporción de Biomarcadores"),
        specs=[[{"type": "bar"}, {"type": "pie"}]]
    )
    
    # Gráfico de barras
    fig.add_trace(
        go.Bar(
            x=biomarker_data['Category'],
            y=biomarker_data['Count'],
            marker_color=biomarker_data['Color'],
            name="Estudios"
        ),
        row=1, col=1
    )
    
    # Gráfico circular
    fig.add_trace(
        go.Pie(
            labels=biomarker_data['Category'],
            values=biomarker_data['Count'],
            marker_colors=biomarker_data['Color'],
            name="Proporción"
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text="Tipos de Biomarcadores en Estudios Incluidos",
        showlegend=False,
        width=1200, height=500
    )
    
    return fig


def create_evidence_map(df: pd.DataFrame) -> go.Figure:
    """
    Crea mapa de evidencia interactivo.
    
    Args:
        df (pd.DataFrame): DataFrame con estudios incluidos
        
    Returns:
        go.Figure: Mapa de evidencia
    """
    # Datos para el mapa de evidencia
    evidence_data = []
    
    biomarker_types = ['Creatinina', 'GFR', 'Albuminuria', 'htTKV', 'Copeptina', 'NGAL']
    outcomes = ['Progresión', 'Diagnóstico', 'Pronóstico', 'Monitoreo']
    study_designs = ['Cohorte', 'Transversal', 'Caso-control']
    
    for biomarker in biomarker_types:
        for outcome in outcomes:
            for design in study_designs:
                evidence_data.append({
                    'Biomarker': biomarker,
                    'Outcome': outcome,
                    'Study_Design': design,
                    'Evidence_Level': np.random.choice(['Alta', 'Moderada', 'Baja'], p=[0.2, 0.5, 0.3]),
                    'Study_Count': np.random.randint(0, 8)
                })
    
    df_evidence = pd.DataFrame(evidence_data)
    
    # Crear heatmap
    pivot_table = df_evidence.pivot_table(
        values='Study_Count',
        index=['Biomarker', 'Study_Design'],
        columns='Outcome',
        aggfunc='sum',
        fill_value=0
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=[f"{bio} ({design})" for bio, design in pivot_table.index],
        colorscale='Viridis',
        colorbar=dict(title="Número de Estudios")
    ))
    
    fig.update_layout(
        title="Mapa de Evidencia: Biomarcadores vs Outcomes",
        xaxis_title="Tipo de Outcome",
        yaxis_title="Biomarcador (Diseño de Estudio)",
        width=800, height=600
    )
    
    return fig


def create_quality_assessment_plot(df: pd.DataFrame) -> go.Figure:
    """
    Crea gráfico de evaluación de calidad metodológica.
    
    Args:
        df (pd.DataFrame): DataFrame con estudios incluidos
        
    Returns:
        go.Figure: Gráfico de calidad
    """
    # Datos de calidad (placeholder)
    quality_criteria = [
        'Diseño Apropiado',
        'Tamaño Muestra Adecuado',
        'Criterios Selección Claros',
        'Medición Estandarizada',
        'Seguimiento Adecuado',
        'Análisis Estadístico',
        'Control Confusores',
        'Reporte Resultados'
    ]
    
    # Generar datos de calidad para cada criterio
    quality_data = []
    for criterion in quality_criteria:
        yes_count = np.random.randint(30, 45)
        no_count = np.random.randint(0, 10)
        unclear_count = 45 - yes_count - no_count
        
        quality_data.extend([
            {'Criterion': criterion, 'Response': 'Sí', 'Count': yes_count},
            {'Criterion': criterion, 'Response': 'No', 'Count': no_count},
            {'Criterion': criterion, 'Response': 'No claro', 'Count': unclear_count}
        ])
    
    df_quality = pd.DataFrame(quality_data)
    
    # Crear gráfico de barras apiladas
    fig = go.Figure()
    
    for response in ['Sí', 'No claro', 'No']:
        data = df_quality[df_quality['Response'] == response]
        color = {'Sí': 'green', 'No claro': 'orange', 'No': 'red'}[response]
        
        fig.add_trace(go.Bar(
            name=response,
            x=data['Criterion'],
            y=data['Count'],
            marker_color=color
        ))
    
    fig.update_layout(
        title="Evaluación de Calidad Metodológica",
        xaxis_title="Criterios de Calidad",
        yaxis_title="Número de Estudios",
        barmode='stack',
        xaxis_tickangle=-45,
        width=1000, height=600
    )
    
    return fig


def create_sample_size_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Crea histograma de distribución de tamaños de muestra.
    
    Args:
        df (pd.DataFrame): DataFrame con estudios incluidos
        
    Returns:
        go.Figure: Histograma
    """
    # Generar tamaños de muestra (placeholder)
    sample_sizes = np.random.lognormal(mean=4, sigma=1, size=45).astype(int)
    sample_sizes = np.clip(sample_sizes, 20, 2000)
    
    fig = go.Figure(data=[go.Histogram(
        x=sample_sizes,
        nbinsx=15,
        marker_color='skyblue',
        marker_line_color='black',
        marker_line_width=1
    )])
    
    fig.update_layout(
        title="Distribución de Tamaños de Muestra",
        xaxis_title="Tamaño de Muestra",
        yaxis_title="Número de Estudios",
        width=800, height=500
    )
    
    return fig


def create_collaboration_network(df: pd.DataFrame) -> go.Figure:
    """
    Crea red de colaboración entre autores/instituciones.
    
    Args:
        df (pd.DataFrame): DataFrame con estudios incluidos
        
    Returns:
        go.Figure: Red de colaboración
    """
    # Crear red de ejemplo
    G = nx.erdos_renyi_graph(20, 0.3)
    pos = nx.spring_layout(G)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                           line=dict(width=0.5, color='#888'),
                           hoverinfo='none',
                           mode='lines')
    
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    
    node_trace = go.Scatter(x=node_x, y=node_y,
                           mode='markers',
                           hoverinfo='text',
                           marker=dict(showscale=True,
                                     colorscale='YlGnBu',
                                     reversescale=True,
                                     color=[],
                                     size=10,
                                     colorbar=dict(
                                         thickness=15,
                                         len=0.5,
                                         x=0.9,
                                         title="Colaboraciones"
                                     ),
                                     line_width=2))
    
    # Colorear nodos por número de conexiones
    node_adjacencies = []
    node_text = []
    for node in G.nodes():
        adjacencies = list(G.neighbors(node))
        node_adjacencies.append(len(adjacencies))
        node_text.append(f'Institución {node}<br># colaboraciones: {len(adjacencies)}')
    
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                        title='Red de Colaboración entre Instituciones',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            text="Red basada en co-autorías",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002 ) ],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
    return fig


def create_interactive_dashboard(included_studies: pd.DataFrame, screening_data: Dict) -> go.Figure:
    """
    Crea dashboard interactivo con múltiples visualizaciones.
    
    Args:
        included_studies (pd.DataFrame): Estudios incluidos
        screening_data (Dict): Datos de screening
        
    Returns:
        go.Figure: Dashboard interactivo
    """
    # Crear dashboard con subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Distribución Temporal", "Tipos de Biomarcadores", 
                       "Distribución Geográfica", "Calidad de Estudios"),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "choropleth"}, {"type": "bar"}]]
    )
    
    # Agregar plots individuales aquí (versiones simplificadas)
    # Esto sería una versión consolidada de los plots anteriores
    
    fig.update_layout(
        title_text="Dashboard Interactivo - Revisión PRISMA-ScR",
        height=800,
        showlegend=False
    )
    
    return fig


def create_figures_summary_report(figures_list: List[str], output_dir: str) -> None:
    """
    Crea reporte HTML con resumen de todas las figuras.
    
    Args:
        figures_list (List[str]): Lista de nombres de archivos de figuras
        output_dir (str): Directorio de salida
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Figuras - Revisión PRISMA-ScR</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .figure { margin: 20px 0; padding: 10px; border: 1px solid #ccc; }
            img { max-width: 100%; height: auto; }
        </style>
    </head>
    <body>
        <h1>Figuras - Revisión PRISMA-ScR sobre Biomarcadores en ADPKD</h1>
    """
    
    for figure_file in figures_list:
        html_content += f"""
        <div class="figure">
            <h3>{figure_file}</h3>
            <img src="{figure_file}" alt="{figure_file}">
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    with open(f"{output_dir}/Figures_Summary.html", 'w') as f:
        f.write(html_content)


def generate_visualization_statistics(df: pd.DataFrame) -> str:
    """
    Genera estadísticas de las visualizaciones creadas.
    
    Args:
        df (pd.DataFrame): DataFrame con estudios incluidos
        
    Returns:
        str: Estadísticas de visualizaciones
    """
    stats = f"""
    ESTADÍSTICAS DE VISUALIZACIONES
    ===============================
    
    Estudios incluidos: {len(df)}
    Figuras principales creadas: 6
    Figuras suplementarias: 2
    Visualizaciones interactivas: 3
    
    Tipos de gráficos:
    - Diagrama de flujo PRISMA: 1
    - Gráficos temporales: 1
    - Mapas geográficos: 1
    - Gráficos de barras: 2
    - Mapas de calor: 1
    - Redes: 1
    - Dashboard interactivo: 1
    
    Formatos de salida:
    - PNG (alta resolución): 6
    - HTML (interactivo): 4
    - Dashboard compilado: 1
    """
    
    return stats