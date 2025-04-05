import cv2
import numpy as np
from typing import Dict, Any
import dlib
from app.services.image_processor import crop_face

# Variable global para cargar el predictor de landmarks una sola vez
face_landmark_predictor = None

async def analyze_symmetry(image_path: str, face: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analiza la simetría facial
    
    Args:
        image_path: Ruta a la imagen
        face: Diccionario con información del rostro
        
    Returns:
        Dict con resultados del análisis de simetría
    """
    try:
        global face_landmark_predictor
        
        # Recortar el rostro
        face_location = face["location"]
        face_img = crop_face(image_path, face_location)
        
        if face_img.size == 0:
            raise ValueError("No se pudo procesar la imagen del rostro")
        
        # Si se proporcionan landmarks en los datos de rostro, usarlos
        if face.get("landmarks") and len(face["landmarks"]) > 0:
            return await analyze_symmetry_from_landmarks(face_img, face["landmarks"])
        
        # Si no hay landmarks, intentar detectarlos con dlib
        try:
            import dlib
            if face_landmark_predictor is None:
                predictor_path = dlib.get_frontal_face_detector()
                face_landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
            
            # Intentar detectar puntos faciales
            detector = dlib.get_frontal_face_detector()
            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 1)
            
            if len(rects) > 0:
                landmarks = face_landmark_predictor(gray, rects[0])
                landmarks_dict = landmarks_to_dict(landmarks)
                return await analyze_symmetry_from_landmarks(face_img, landmarks_dict)
        except Exception as e:
            print(f"Error al usar dlib: {str(e)}")
        
        # Si no se pueden detectar landmarks, usar método alternativo basado en imagen
        return await analyze_symmetry_basic(face_img)
    except Exception as e:
        print(f"Error en análisis de simetría: {str(e)}")
        return {
            "score": 0.75,
            "analysis": "No se pudo completar el análisis de simetría",
            "details": {
                "left_right_ratio": 1.0,
                "key_points_alignment": 0.75
            }
        }

async def analyze_symmetry_from_landmarks(face_image, landmarks):
    """Analiza simetría basándose en puntos de referencia faciales"""
    try:
        # Obtener dimensiones de la imagen
        height, width = face_image.shape[:2]
        midline_x = width / 2
        
        # Extraer puntos clave de ambos lados
        left_eye = landmarks.get("left_eye", {"x": width * 0.35, "y": height * 0.35})
        right_eye = landmarks.get("right_eye", {"x": width * 0.65, "y": height * 0.35})
        
        # Calcular distancias al eje central
        left_dist = abs(left_eye["x"] - midline_x)
        right_dist = abs(right_eye["x"] - midline_x)
        
        # Calcular ratio de distancias (1.0 = perfectamente simétrico)
        if min(left_dist, right_dist) == 0:
            eyes_ratio = 0.5
        else:
            eyes_ratio = min(left_dist, right_dist) / max(left_dist, right_dist)
        
        # Calcular alineación vertical (misma altura)
        vertical_alignment = 1.0 - abs(left_eye["y"] - right_eye["y"]) / height
        
        # Combinar métricas
        symmetry_score = 0.7 * eyes_ratio + 0.3 * vertical_alignment
        
        # Limitar entre 0 y 1
        symmetry_score = max(0, min(symmetry_score, 1))
        
        # Generar análisis textual
        analysis_text = get_symmetry_analysis(symmetry_score)
        
        return {
            "score": round(symmetry_score, 2),
            "analysis": analysis_text,
            "details": {
                "left_right_ratio": round(eyes_ratio, 2),
                "vertical_alignment": round(vertical_alignment, 2)
            }
        }
    except Exception as e:
        print(f"Error en análisis desde landmarks: {str(e)}")
        return await analyze_symmetry_basic(face_image)

async def analyze_symmetry_basic(face_image):
    """
    Analiza la simetría facial sin landmarks, usando propiedades de la imagen
    """
    try:
        # Convertir a escala de grises
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        
        # Voltear la imagen horizontalmente
        flipped = cv2.flip(gray, 1)
        
        # Calcular la diferencia entre la imagen original y espejada
        diff = cv2.absdiff(gray, flipped)
        
        # Calcular el valor medio de la diferencia
        mean_diff = np.mean(diff)
        
        # Normalizar (0 = perfecta simetría, 255 = completa asimetría)
        symmetry_score = 1.0 - (mean_diff / 255.0)
        
        # Ajustar escala para ser más realista (pocos rostros son perfectamente simétricos)
        symmetry_score = 0.5 + (symmetry_score - 0.5) * 0.5
        
        # Generar análisis textual
        analysis_text = get_symmetry_analysis(symmetry_score)
        
        return {
            "score": round(symmetry_score, 2),
            "analysis": analysis_text,
            "details": {
                "pixel_diff": round(mean_diff, 2),
            }
        }
    except Exception as e:
        print(f"Error en análisis básico: {str(e)}")
        return {
            "score": 0.7,  # Valor por defecto
            "analysis": "No se pudo completar el análisis detallado",
            "details": {}
        }

def landmarks_to_dict(landmarks):
    """Convierte landmarks de dlib a diccionario"""
    points = {}
    
    # Mapeo de índices a nombres de points
    landmark_map = {
        36: "right_eye",  # Ojo derecho (desde perspectiva de la imagen)
        45: "left_eye",   # Ojo izquierdo (desde perspectiva de la imagen)
        30: "nose_tip",
        48: "mouth_left",
        54: "mouth_right"
    }
    
    for i in range(68):
        if i in landmark_map:
            points[landmark_map[i]] = {
                "x": landmarks.part(i).x,
                "y": landmarks.part(i).y
            }
    
    return points

def get_symmetry_analysis(score):
    """Genera texto de análisis basado en puntuación de simetría"""
    if score >= 0.9:
        return "Rostro con alta simetría"
    elif score >= 0.8:
        return "Rostro con buena simetría"
    elif score >= 0.7:
        return "Rostro con simetría normal"
    elif score >= 0.6:
        return "Rostro con ligera asimetría"
    else:
        return "Rostro con notable asimetría"
