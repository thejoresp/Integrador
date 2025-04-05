import cv2
import numpy as np
from typing import Dict, Any

from app.services.image_processor import crop_face

async def analyze_skin(image_path: str, face: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analiza características de la piel en un rostro
    
    Args:
        image_path: Ruta a la imagen
        face: Diccionario con información del rostro
        
    Returns:
        Dict con resultados del análisis de piel
    """
    try:
        # Recortar el rostro
        face_location = face["location"]
        face_img = crop_face(image_path, face_location)
        
        if face_img.size == 0:
            raise ValueError("No se pudo procesar la imagen del rostro")
        
        # Extraer región de la piel
        skin_mask = extract_skin_mask(face_img)
        
        # Analizar características
        hydration_score = analyze_hydration(face_img, skin_mask)
        texture_score = analyze_texture(face_img, skin_mask)
        pores_score = analyze_pores(face_img, skin_mask)
        
        # Convertir puntuaciones a categorías
        hydration_category = score_to_category(hydration_score)
        texture_category = texture_to_category(texture_score)
        pores_category = pores_to_category(pores_score)
        
        return {
            "hydration": hydration_category,
            "texture": texture_category,
            "pores": pores_category,
            "scores": {
                "hydration": hydration_score,
                "texture": texture_score,
                "pores": pores_score
            }
        }
    except Exception as e:
        print(f"Error en análisis de piel: {str(e)}")
        return {
            "hydration": "Normal",
            "texture": "Normal",
            "pores": "Normales",
            "scores": {
                "hydration": 0.5,
                "texture": 0.5,
                "pores": 0.5
            }
        }

def extract_skin_mask(face_image):
    """Extrae una máscara de la piel del rostro"""
    # Convertir a espacio de color YCrCb (mejor para detección de piel)
    ycrcb = cv2.cvtColor(face_image, cv2.COLOR_BGR2YCrCb)
    
    # Rango de color de piel en YCrCb
    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)
    
    # Crear máscara para la piel
    skin_mask = cv2.inRange(ycrcb, lower, upper)
    
    # Aplicar operaciones morfológicas para mejorar la máscara
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skin_mask = cv2.erode(skin_mask, kernel, iterations=2)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=2)
    
    # Suavizar máscara
    skin_mask = cv2.GaussianBlur(skin_mask, (3, 3), 0)
    
    return skin_mask

def analyze_hydration(face_image, skin_mask):
    """Analiza el nivel de hidratación basado en características de la piel"""
    # Extraer canal de luminancia (Y en YCrCb)
    ycrcb = cv2.cvtColor(face_image, cv2.COLOR_BGR2YCrCb)
    y_channel = ycrcb[:,:,0]
    
    # Aplicar la máscara
    masked_y = cv2.bitwise_and(y_channel, y_channel, mask=skin_mask)
    
    # Calcular estadísticas en la región de piel
    non_zero = masked_y[skin_mask > 0]
    if len(non_zero) == 0:
        return 0.5  # Valor por defecto
    
    # Calcular puntuación basada en brillo y varianza
    avg_brightness = np.mean(non_zero)
    std_brightness = np.std(non_zero)
    
    # Normalizar: piel bien hidratada tiene brillo moderado y baja varianza
    hydration_score = 0.7 * (1 - abs(avg_brightness - 128) / 128) + 0.3 * (1 - min(std_brightness / 40, 1))
    
    return max(0, min(hydration_score, 1))  # Asegurar valor entre 0 y 1

def analyze_texture(face_image, skin_mask):
    """Analiza la textura de la piel"""
    # Convertir a escala de grises
    gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar la máscara
    masked_gray = cv2.bitwise_and(gray, gray, mask=skin_mask)
    
    # Calcular el gradiente usando Sobel
    sobelx = cv2.Sobel(masked_gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(masked_gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Magnitud del gradiente
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
    
    # Extraer valores no cero (solo piel)
    non_zero = gradient_magnitude[skin_mask > 0]
    if len(non_zero) == 0:
        return 0.5  # Valor por defecto
    
    # Piel suave tiene gradientes pequeños
    avg_gradient = np.mean(non_zero)
    
    # Normalizar: valores más bajos indican piel más suave
    texture_score = 1 - min(avg_gradient / 20, 1)
    
    return max(0, min(texture_score, 1))

def analyze_pores(face_image, skin_mask):
    """Analiza los poros de la piel"""
    # Convertir a escala de grises
    gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar la máscara
    masked_gray = cv2.bitwise_and(gray, gray, mask=skin_mask)
    
    # Aplicar filtro de detección de bordes
    edges = cv2.Canny(masked_gray, 50, 150)
    
    # Contar píxeles de borde en relación al área de piel
    edge_pixels = np.sum(edges > 0)
    skin_pixels = np.sum(skin_mask > 0)
    
    if skin_pixels == 0:
        return 0.5  # Valor por defecto
    
    # Calcular densidad de bordes (relacionada con poros y textura)
    edge_density = edge_pixels / skin_pixels
    
    # Normalizar: más bordes indican más poros/textura irregular
    pore_score = 1 - min(edge_density * 100, 1)
    
    return max(0, min(pore_score, 1))

def score_to_category(score):
    """Convierte puntuación de hidratación a categoría"""
    if score >= 0.8:
        return "Excelente"
    elif score >= 0.6:
        return "Buena"
    elif score >= 0.4:
        return "Normal"
    elif score >= 0.2:
        return "Baja"
    else:
        return "Muy baja"

def texture_to_category(score):
    """Convierte puntuación de textura a categoría"""
    if score >= 0.8:
        return "Muy suave"
    elif score >= 0.6:
        return "Suave"
    elif score >= 0.4:
        return "Normal"
    elif score >= 0.2:
        return "Áspera"
    else:
        return "Muy áspera"

def pores_to_category(score):
    """Convierte puntuación de poros a categoría"""
    if score >= 0.8:
        return "Apenas visibles"
    elif score >= 0.6:
        return "Finos"
    elif score >= 0.4:
        return "Normales"
    elif score >= 0.2:
        return "Dilatados"
    else:
        return "Muy dilatados"
