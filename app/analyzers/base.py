import abc
import numpy as np
import cv2
from typing import Dict, Any

class BaseAnalyzer(abc.ABC):
    """Clase base para todos los analizadores faciales"""
    
    def __init__(self):
        """Inicializa el analizador"""
        self._load_models()
    
    @abc.abstractmethod
    def _load_models(self):
        """Carga los modelos necesarios. Se debe implementar en las subclases."""
        pass
    
    @abc.abstractmethod
    def analyze(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Analiza una imagen y retorna los resultados
        
        Args:
            image: Imagen como array de numpy (BGR)
            
        Returns:
            Dict: Resultados del análisis
        """
        pass
    
    def _detect_face(self, image: np.ndarray):
        """
        Detecta rostros en una imagen usando OpenCV
        
        Args:
            image: Imagen como array de numpy (BGR)
            
        Returns:
            tuple: (x, y, w, h) coordenadas del rostro o None si no se encuentra
        """
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            return None
        
        # Devolver el rostro más grande
        return max(faces, key=lambda face: face[2] * face[3])
