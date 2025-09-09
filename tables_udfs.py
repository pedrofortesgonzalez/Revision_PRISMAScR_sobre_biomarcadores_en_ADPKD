import re

###################################################################################################################################################
def extraer_apellido_y_ano(texto):
    """Extrae apellido del primer autor y año de publicación de lista completa de autores + año"""
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
    """Extrae año de publicación de autor + año"""
    # extrae num. al final de la cadena
    m_ano = re.search(r'(\d{4})$', texto)
    ultimo_ano = m_ano.group(1) if m_ano else ""
    # unir ambos con un " "
    return f"{ultimo_ano}"



###################################################################################################################################################
def formato_bullets(dict_omicas):
    """Convierte un diccionario de ómicas en formato bullet markdown."""
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