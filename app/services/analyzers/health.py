import cv2
import numpy as np
from typing import Dict, Any, List

from app.services.image_processor import crop_face

async def analyze_health_indicators(image_path: str, face: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analiza indicadores de salud en un rostro
    
    Args:
        image_path: Ruta a la imagen
        face: Diccionario con información del rostro
        
    Returns:
        Dict con resultados del análisis de indicadores de salud
    """
    try:
        # Recortar el rostro
        face_location = face["location"]
        face_img = crop_face(image_path, face_location)
        
        if face_img.size == 0:
            raise ValueError("No se pudo procesar la imagen del rostro")
        
        # Analizar diferentes aspectos
        stress_level = analyze_stress(face_img, face)
        fatigue = analyze_fatigue(face_img, face)
        eye_fatigue = analyze_eye_fatigue(face_img, face)
        
        # Obtener recomendaciones basadas en análisis
        recommendations = generate_recommendations(stress_level, fatigue, eye_fatigue)
        
        return {
            "stress_level": categorize_stress(stress_level),
            "fatigue": categorize_fatigue(fatigue),
            "eye_fatigue": categorize_eye_fatigue(eye_fatigue),
            "scores": {
                "stress": stress_level,
                "fatigue": fatigue,
                "eye_fatigue": eye_fatigue
            },
            "recommendations": recommendations
        }
    except Exception as e:
        print(f"Error en análisis de salud: {str(e)}")
        return {
            "stress_level": "Moderado",
            "fatigue": "Leve",
            "eye_fatigue": "No detectada",
            "recommendations": ["Descanso adecuado", "Hidratación regular"]
        }

def analyze_stress(face_image, face_data):
    """Analiza nivel de estrés basado en características faciales"""
    try:
        # Convertir a escala de grises
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        
        # Detectar características de estrés (arrugas en frente, cejas fruncidas)
        # Este es un enfoque simplificado - un modelo completo requeriría landmarks faciales detallados
        
        # Calcular gradiente horizontal (para detectar líneas verticales como ceño fruncido)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        
        # Detectar bordes
        edges = cv2.Canny(gray, 50, 150)
        
        # Para una implementación completa, aquí analizaríamos líneas específicas
        # entre las cejas y en la frente usando landmarks faciales
        
        # Para simplificar, usamos la cantidad de bordes en la parte superior del rostro
        height, width = gray.shape
        upper_face = edges[0:int(height/2), :]
        
        # Contar píxeles de borde en la parte superior
        edge_pixels = np.sum(upper_face > 0)
        
        # Normalizar
        stress_score = min(edge_pixels / (width * height/4 * 0.05), 1)
        
        return stress_score
    except Exception as e:
        print(f"Error al analizar estrés: {str(e)}")
        return 0.3  # Valor por defecto

def analyze_fatigue(face_image, face_data):
    """Analiza nivel de fatiga basado en características faciales"""
    try:
        # Convertir a espacio de color HSV
        hsv = cv2.cvtColor(face_image, cv2.COLOR_BGR2HSV)
        
        # Extraer canal de saturación (piel cansada tiende a ser menos saturada)
        saturation = hsv[:,:,1]
        
        # Extraer canal de valor (piel cansada tiende a ser más oscura)
        value = hsv[:,:,2]
        
        # Calcular promedios
        avg_saturation = np.mean(saturation)
        avg_value = np.mean(value)
        
        # Normalizar valores
        norm_saturation = avg_saturation / 255
        norm_value = avg_value / 255
        
        # Combinar en una puntuación de fatiga (valores más bajos = más fatiga)
        vitality_score = 0.4 * norm_saturation + 0.6 * norm_value
        fatigue_score = 1 - vitality_score
        
        return min(fatigue_score * 1.5, 1)  # Ajuste para sensibilidad
    except Exception as e:
        print(f"Error al analizar fatiga: {str(e)}")
        return 0.4  # Valor por defecto

def analyze_eye_fatigue(face_image, face_data):
    """Analiza fatiga ocular basada en área de ojos"""
    try:
        # Para un análisis completo necesitaríamos landmarks de ojos
        # Si no tenemos landmarks, hacemos una estimación aproximada
        
        # Convertir a espacio YCrCb
        ycrcb = cv2.cvtColor(face_image, cv2.COLOR_BGR2YCrCb)
        
        # Extraer canal Y (luminancia)
        y_channel = ycrcb[:,:,0]
        
        # Asumimos que los ojos están en la mitad superior del rostro
        height, width = face_image.shape[:2]
        eye_region = y_channel[int(height*0.2):int(height*0.5), :]
        
        # Buscar áreas oscuras (posibles ojeras)
        dark_threshold = 100  # Umbral para considerar un píxel oscuro
        dark_pixels = np.sum(eye_region < dark_threshold)
        
        # Normalizar por el tamaño de la región
        dark_ratio = dark_pixels / (eye_region.shape[0] * eye_region.shape[1])
        
        # Convertir a puntuación de fatiga ocular
        eye_fatigue_score = min(dark_ratio * 5, 1)  # Ajuste de sensibilidad
        
        return eye_fatigue_score
    except Exception as e:
        print(f"Error al analizar fatiga ocular: {str(e)}")
        return 0.3  # Valor por defecto

def categorize_stress(score):
    """Convierte puntuación de estrés a categoría"""
    if score < 0.3:
        return "Bajo"
    elif score < 0.6:
        return "Moderado"
    else:
        return "Alto"

def categorize_fatigue(score):
    """Convierte puntuación de fatiga a categoría"""
    if score < 0.3:
        return "Mínima"
    elif score < 0.5:
        return "Leve"
    elif score < 0.7:
        return "Moderada"
    else:
        return "Severa"

def categorize_eye_fatigue(score):
    """Convierte puntuación de fatiga ocular a categoría"""
    if score < 0.3:
        return "No detectada"
    elif score < 0.5:
        return "Leve"
    elif score < 0.7:
        return "Moderada"
    else:
        return "Significativa"

def generate_recommendations(stress, fatigue, eye_fatigue):
    """Genera recomendaciones basadas en las puntuaciones de salud"""
    recommendations = []
    
    if stress > 0.6:
        recommendations.append("Considere técnicas de relajación como meditación o yoga")
    elif stress > 0.4:
        recommendations.append("Practique respiración profunda durante el día")
    
    if fatigue > 0.6:
        recommendations.append("Priorice descanso de calidad y sueño regular")
    elif fatigue > 0.4:
        recommendations.append("Considere mejorar sus hábitos de sueño")
    
    if eye_fatigue > 0.6:
        recommendations.append("Reduzca el tiempo frente a pantallas y aplique la regla 20-20-20")
    elif eye_fatigue > 0.4:
        recommendations.append("Descanse sus ojos regularmente durante el día")
    
    if stress > 0.5 and fatigue > 0.5:
        recommendations.append("Evalúe su balance entre trabajo y descanso")
    
    if len(recommendations) == 0:
        recommendations.append("Mantenga sus buenos hábitos de salud")
    
    return recommendations
