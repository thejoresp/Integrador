import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Optional, Any, Tuple

from app.config import FACE_DETECTION_MODEL
from app.models.schemas import FaceLocation

# Inicializar MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(
    model_selection=1,  # 0=corta distancia, 1=larga distancia 
    min_detection_confidence=0.5
)

async def detect_faces(image_path: str) -> List[Dict[str, Any]]:
    """
    Detecta rostros en una imagen y devuelve sus ubicaciones y landmarks
    
    Args:
        image_path: Ruta a la imagen a analizar
        
    Returns:
        Lista de diccionarios con información de cada rostro detectado
    """
    try:
        # Leer la imagen
        image = cv2.imread(image_path)
        if image is None:
            return []
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image.shape[:2]
        
        # Usar el detector según configuración
        if FACE_DETECTION_MODEL == "mediapipe":
            return await _detect_with_mediapipe(image_rgb, height, width)
        elif FACE_DETECTION_MODEL == "opencv":
            return await _detect_with_opencv(image, height, width)
        else:
            # Valor por defecto
            return await _detect_with_mediapipe(image_rgb, height, width)
            
    except Exception as e:
        print(f"Error en detección facial: {str(e)}")
        return []

async def _detect_with_mediapipe(image_rgb, height, width) -> List[Dict[str, Any]]:
    """Detecta rostros usando MediaPipe"""
    faces = []
    results = face_detection.process(image_rgb)
    
    if results.detections:
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            
            # Convertir coordenadas relativas a absolutas
            x = int(bbox.xmin * width)
            y = int(bbox.ymin * height)
            w = int(bbox.width * width)
            h = int(bbox.height * height)
            
            # Asegurar que las coordenadas estén dentro de la imagen
            x = max(0, x)
            y = max(0, y)
            w = min(w, width - x)
            h = min(h, height - y)
            
            # Crear diccionario con información del rostro
            face_info = {
                "location": {
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                },
                "confidence": detection.score[0],
                "landmarks": {}
            }
            
            # Extraer landmarks (MediaPipe proporciona 6 puntos clave)
            keypoints = detection.location_data.relative_keypoints
            landmarks = {}
            
            # Mapeo de índices a nombres de landmarks
            keypoint_names = ["right_eye", "left_eye", "nose_tip", "mouth_center", 
                             "right_ear_tragion", "left_ear_tragion"]
            
            for i, keypoint in enumerate(keypoints):
                if i < len(keypoint_names):
                    landmarks[keypoint_names[i]] = {
                        "x": int(keypoint.x * width),
                        "y": int(keypoint.y * height)
                    }
            
            face_info["landmarks"] = landmarks
            faces.append(face_info)
    
    return faces

async def _detect_with_opencv(image, height, width) -> List[Dict[str, Any]]:
    """Detecta rostros usando OpenCV"""
    # Cargar el clasificador Haar Cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detectar rostros
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    opencv_faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    faces = []
    for (x, y, w, h) in opencv_faces:
        face_info = {
            "location": {
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h)
            },
            "confidence": 1.0,  # OpenCV no proporciona score de confianza con Haar cascades
            "landmarks": {}  # OpenCV necesita un detector separado para landmarks
        }
        faces.append(face_info)
    
    return faces
