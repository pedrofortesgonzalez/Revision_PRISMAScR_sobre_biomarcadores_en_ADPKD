import re

###################################################################################################################################################
def extraer_apellido_y_ano(texto):
    """
    Extrae el primer apellido del autor y el año de publicación de una cadena que contiene 
    la lista completa de autores y el año.

    Args:
        texto : Cadena con autores y año de publicación (por ejemplo: "González, Pérez, López, 2021").

    Returns:
        Cadena en formato "Apellido, Año". Si alguno no se encuentra, retorna vacío en su lugar.
    """
    # extrae 1º apellido (antes de 1ª ",")
    m_apellido = re.match(r'([^,]+),', texto)
    primer_apellido = m_apellido.group(1) if m_apellido else ""
    
    # extrae num. al final de la cadena
    m_ano = re.search(r'(\d{4})$', texto)
    ultimo_ano = m_ano.group(1) if m_ano else ""
    
    # unir ambos con un " "
    return f"{primer_apellido}, {ultimo_ano}"

###################################################################################################################################################
def extraer_ano(texto):
    """
    Extrae el año de publicación de una cadena con autor y año.

    Args:
        texto : Cadena que contiene el año de publicación al final (por ejemplo: "González 2021").

    Returns:
        Año extraído como texto. Si no se encuentra, retorna vacío.
    """
    # extrae num. al final de la cadena
    m_ano = re.search(r'(\d{4})$', texto)
    ultimo_ano = m_ano.group(1) if m_ano else ""
    
    # unir ambos con un " "
    return f"{ultimo_ano}"



###################################################################################################################################################
def formato_bullets(dict_omicas):
    """
    Convierte un diccionario de ómicas y técnicas asociadas en un formato de lista con viñetas 
    estilo Markdown.

    Args:
        dict_omicas : Diccionario donde las llaves son nombres de ómicas y los valores son listas de técnicas asociadas.

    Returns: 
        Cadena en formato lista Markdown con cada ómica y sus técnicas. Si no hay técnicas, indica "sin técnicas especificadas".
    """
    
    if not isinstance(dict_omicas, dict):
        return ""
    
    bullets = []
    # Iteramos sobre cada par clave-valor del diccionario
    for omica, tecnicas in dict_omicas.items():
        # Unimos las técnicas en un string con comas
        tecnicas_str = ', '.join(tecnicas) if tecnicas else "sin técnicas especificadas"
        # Añadimos el bullet point
        bullets.append(f"- {omica}: {tecnicas_str}")
    
    return '\n'.join(bullets)