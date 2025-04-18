"""
Módulo de detección facial para análisis de imágenes.

Este módulo proporciona funciones para detectar rostros en imágenes
utilizando diversos algoritmos (MediaPipe, OpenCV) según la configuración.
"""
import cv2
import numpy as np
from typing import List, Dict, Optional, Any, Tuple, Union
import asyncio

from app.config import config, logger

# Importación condicional de MediaPipe
try:
    import mediapipe as mp
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        model_selection=1,  # 0=corta distancia, 1=larga distancia 
        min_detection_confidence=0.5
    )
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    logger.warning("MediaPipe no está disponible. Usando OpenCV para detección facial.")
    MEDIAPIPE_AVAILABLE = False

# Nombres de landmarks faciales para MediaPipe
MEDIAPIPE_KEYPOINT_NAMES = [
    "right_eye", "left_eye", "nose_tip", "mouth_center", 
    "right_ear_tragion", "left_ear_tragion"
]

async def detect_faces(
    image_path: str, 
    detection_method: str = None
) -> List[Dict[str, Any]]:
    """
    Detecta rostros en una imagen y devuelve sus ubicaciones y landmarks.
    
    Args:
        image_path: Ruta absoluta a la imagen a analizar
        detection_method: Método de detección a usar ('mediapipe', 'opencv' o None para usar config)
        
    Returns:
        Lista de diccionarios con información de cada rostro detectado:
        [
            {
                "location": {"x": int, "y": int, "width": int, "height": int},
                "confidence": float,
                "landmarks": {"right_eye": {"x": int, "y": int}, ...}
            },
            ...
        ]
    """
    try:
        # Leer la imagen
        image = cv2.imread(image_path)
        if image is None:
            logger.warning(f"No se pudo leer la imagen: {image_path}")
            return []
        
        # Obtener dimensiones
        height, width = image.shape[:2]
        
        # Determinar el método de detección
        if detection_method is None:
            # Usar configuración global si no se especifica
            model_config = config.get_model_config("face_detection")
            detection_method = model_config["default"]
        
        # Usar el detector según método elegido
        if detection_method == "mediapipe" and MEDIAPIPE_AVAILABLE:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return await _detect_with_mediapipe(image_rgb, height, width)
        elif detection_method == "opencv" or not MEDIAPIPE_AVAILABLE:
            return await _detect_with_opencv(image, height, width)
        else:
            # Fallback a OpenCV si el método no es reconocido
            logger.warning(f"Método de detección '{detection_method}' no reconocido, usando OpenCV")
            return await _detect_with_opencv(image, height, width)
            
    except Exception as e:
        logger.error(f"Error en detección facial: {str(e)}", exc_info=True)
        return []

async def _detect_with_mediapipe(
    image_rgb: np.ndarray, 
    height: int, 
    width: int
) -> List[Dict[str, Any]]:
    """
    Detecta rostros usando MediaPipe.
    
    Args:
        image_rgb: Imagen en formato RGB
        height: Altura de la imagen
        width: Ancho de la imagen
        
    Returns:
        Lista de diccionarios con información de cada rostro
    """
    faces = []
    # Procesar la imagen con MediaPipe
    results = face_detection.process(image_rgb)
    
    if not results.detections:
        return []
        
    for detection in results.detections:
        bbox = detection.location_data.relative_bounding_box
        
        # Convertir coordenadas relativas a absolutas
        x = int(bbox.xmin * width)
        y = int(bbox.ymin * height)
        w = int(bbox.width * width)
        h = int(bbox.height * height)
        
        # Asegurar que las coordenadas estén dentro de la imagen
        x, y, w, h = _normalize_coordinates(x, y, w, h, width, height)
        
        # Crear diccionario con información del rostro
        face_info = {
            "location": (x, y, w, h),
            "confidence": float(detection.score[0]),
            "landmarks": _extract_mediapipe_landmarks(detection, width, height)
        }
        
        faces.append(face_info)
    
    return faces

def _extract_mediapipe_landmarks(detection, width: int, height: int) -> Dict[str, Dict[str, int]]:
    """
    Extrae landmarks faciales de una detección de MediaPipe.
    
    Args:
        detection: Objeto de detección de MediaPipe
        width: Ancho de la imagen
        height: Altura de la imagen
        
    Returns:
        Diccionario con landmarks faciales
    """
    landmarks = {}
    keypoints = detection.location_data.relative_keypoints
    
    for i, keypoint in enumerate(keypoints):
        if i < len(MEDIAPIPE_KEYPOINT_NAMES):
            landmarks[MEDIAPIPE_KEYPOINT_NAMES[i]] = {
                "x": int(keypoint.x * width),
                "y": int(keypoint.y * height)
            }
    
    return landmarks

async def _detect_with_opencv(
    image: np.ndarray, 
    height: int, 
    width: int
) -> List[Dict[str, Any]]:
    """
    Detecta rostros usando OpenCV.
    
    Args:
        image: Imagen en formato BGR
        height: Altura de la imagen
        width: Ancho de la imagen
        
    Returns:
        Lista de diccionarios con información de cada rostro
    """
    # Cargar el clasificador Haar Cascade
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detectar rostros
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        opencv_faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        faces = []
        for (x, y, w, h) in opencv_faces:
            # Asegurar que las coordenadas estén dentro de la imagen
            x, y, w, h = _normalize_coordinates(x, y, w, h, width, height)
            
            face_info = {
                "location": (x, y, w, h),
                "confidence": 0.8,  # OpenCV no proporciona score, usamos valor predeterminado
                "landmarks": {}  # OpenCV necesita un detector separado para landmarks
            }
            faces.append(face_info)
        
        return faces
    except Exception as e:
        logger.error(f"Error en detección con OpenCV: {str(e)}", exc_info=True)
        return []

def _normalize_coordinates(
    x: int, 
    y: int, 
    w: int, 
    h: int, 
    max_width: int, 
    max_height: int
) -> Tuple[int, int, int, int]:
    """
    Normaliza las coordenadas para asegurar que estén dentro de los límites de la imagen.
    
    Args:
        x, y: Coordenadas de la esquina superior izquierda
        w, h: Ancho y alto del rectángulo
        max_width, max_height: Dimensiones máximas permitidas
        
    Returns:
        Tupla con coordenadas normalizadas (x, y, w, h)
    """
    # Asegurar que las coordenadas sean no negativas
    x = max(0, x)
    y = max(0, y)
    
    # Asegurar que el ancho y alto no excedan los límites de la imagen
    w = min(w, max_width - x)
    h = min(h, max_height - y)
    
    return (x, y, w, h)
