import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re
import seaborn as sns
from collections import Counter



def create_box(ax, x, y, width, height, text, max_chars=30, fontsize=10, edgecolor='black', 
               facecolor='white', align_bullets=True):
    """
    Crea un cuadro de texto con opción para alinear listas con viñetas a la izquierda.
    
    Args:
        ax: Ejes de matplotlib
        x, y: Posición central del cuadro
        width, height: Dimensiones del cuadro
        text: Texto a mostrar
        max_chars: Caracteres máximos por línea
        fontsize: Tamaño de la fuente
        edgecolor: Color del borde
        facecolor: Color de fondo
        align_bullets: Si True, las líneas con viñetas se alinean a la izquierda
    Return:
        None
    """
    # Crear el rectángulo
    rect = patches.Rectangle(
        (x - width / 2, y - height / 2), 
        width, 
        height, 
        linewidth=1, 
        edgecolor=edgecolor, 
        facecolor=facecolor
    )
    ax.add_patch(rect)
    
    # Si queremos alinear las viñetas y hay viñetas en el texto
    if align_bullets and '•' in text:
        # Dividir el texto en líneas
        lines = text.split('\n')
        
        # Calcular el número de líneas para centrar verticalmente
        num_lines = len(lines)
        
        # Calcular el espaciado vertical entre líneas (CORREGIDO)
        # Valor mucho más grande para evitar superposición
        line_height = height / (num_lines + 1)
        
        # Posición inicial (desde arriba)
        y_top = y + height/2 - line_height * 0.8
        
        for i, line in enumerate(lines):
            current_y = y_top - i * line_height
            
            if line.strip().startswith('•'):
                # Para líneas con viñetas, alinear a la izquierda con padding
                ax.text(
                    x - width/2 + 0.15,  # Pequeño margen desde el borde izquierdo
                    current_y,
                    line,
                    fontsize=fontsize,
                    verticalalignment='center',
                    horizontalalignment='left'
                )
            else:
                # Para líneas normales, centrar
                ax.text(
                    x,
                    current_y,
                    line,
                    fontsize=fontsize,
                    verticalalignment='center',
                    horizontalalignment='center'
                )
    else:
        # Comportamiento original para texto sin viñetas (centrado)
        ax.text(
            x, 
            y, 
            text, 
            fontsize=fontsize,
            horizontalalignment='center',
            verticalalignment='center',
            wrap=True
        )
    
    return rect




def create_vertical_arrow(ax, x, y_start, y_end):
    """
    Dibuja una flecha vertical en los ejes dados desde y_start hasta y_end en la posición x.

    Args:
        ax: Ejes sobre los que se dibuja la flecha.
        x : Posición x donde se dibuja la flecha.
        y_start : Coordenada y inicial de la flecha.
        y_end : Coordenada y final de la flecha.

    Returns:
        None
    """
    arrow_height = abs(y_end - y_start)
    arrow_length = min(0.2, arrow_height * 0.2)  # Tamaño proporcional
    
    ax.arrow(x, y_start, 0, y_end-y_start, 
             head_width=0.2, head_length=arrow_length, 
             fc='black', ec='black', length_includes_head=True,
             zorder=5)  # zorder para que aparezca por encima



def create_horizontal_arrow(ax, x_start, x_end, y):
    """
    Dibuja una flecha horizontal en los ejes dados desde x_start hasta x_end en la posición y.

    Args:
        ax : Ejes sobre los que se dibuja la flecha.
        x_start : Coordenada x inicial de la flecha.
        x_end : Coordenada x final de la flecha.
        y : Posición y donde se dibuja la flecha.

    Returns:
        None
    """
    arrow_width = abs(x_end - x_start)
    arrow_length = min(0.2, arrow_width * 0.2)  # Tamaño proporcional
    
    ax.arrow(x_start, y, x_end-x_start, 0, 
             head_width=0.2, head_length=arrow_length, 
             fc='black', ec='black', length_includes_head=True,
             zorder=5)  # zorder para que aparezca por encima




# Función para formatear strings manteniendo ciertas palabras en minúscula (para barplots)
def format_string(text, lowercase_words, special_words):
    """
    Formatea un texto para mantener ciertas palabras en minúscula y otras con formato especial.

    Args:
        text : Texto a formatear.
        lowercase_words : Palabras que deben permanecer en minúscula (excepto si son la primera palabra).
        special_words : Palabras que deben conservar su formato especial (mayúsculas, acrónimos, etc).

    Returns:
        Texto formateado.
    """
    
    # Primero aplicamos title() a todo el texto
    text_titled = text.title()
    
    # Dividimos en palabras
    words = text_titled.split()
    
    # Procesamos palabra por palabra
    for i, word in enumerate(words):
        # Si la palabra está en lowercase_words y no es la primera palabra, la ponemos en minúsculas
        if word.lower() in lowercase_words and i > 0:
            words[i] = word.lower()
        # Si la palabra está en special_words, usamos esa versión exacta
        elif word.upper() in [w.upper() for w in special_words]:
            for special in special_words:
                if word.upper() == special.upper():
                    words[i] = special
                    break
    
    # Unimos nuevamente las palabras
    return ' '.join(words)



    
# Función para extraer ómicas y técnicas de tabla_3 (para barplots)
def extract_omics_and_techniques(data):
    """
    Extrae listas de ómicas y técnicas de una columna tipo tabla_3, para uso en gráficos de barras.

    Args:
        data : Lista de textos que contienen ómicas y técnicas separadas por guiones y dos puntos.

    Returns:
        Una tupla con dos listas: (todas_las_omicas, todas_las_tecnicas)
    """
    
    all_omics = []
    all_techniques = []
    
    for entry in data:
        if not isinstance(entry, str):
            continue
            
        # Limpiar las comillas si existen
        entry = entry.strip('"')
        
        # Dividir por líneas y procesar cada una
        lines = entry.split('\n')
        for line in lines:
            if not line.strip() or not line.startswith('-'):
                continue
                
            # Extraer la parte después del guión
            parts = line.strip('- ').split(':', 1)
            if len(parts) < 2:
                continue
                
            omic = parts[0].strip()
            techniques_part = parts[1].strip()
            
            # Manejar ómicas múltiples (separadas por coma o por "y")
            omics_list = [o.strip() for o in re.split(r',', omic)]
            for o in omics_list:
                if o and o != "sin técnicas especificadas":
                    all_omics.append(o)
            
            # Extraer técnicas
            if "sin técnicas especificadas" not in techniques_part:
                techniques = [t.strip() for t in techniques_part.split(',')]
                all_techniques.extend(techniques)
    
    return all_omics, all_techniques