"""
Servicio de análisis facial.
Proporciona métodos para analizar distintos aspectos de un rostro.
"""

import logging
import numpy as np
from typing import Dict, Any

from app.analyzers.skin import SkinAnalyzer
from app.analyzers.emotion import EmotionAnalyzer
from app.analyzers.age_gender import AgeGenderAnalyzer
from app.analyzers.health import HealthAnalyzer

logger = logging.getLogger(__name__)

class FaceAnalyzerService:
    """
    Servicio que coordina los análisis faciales.
    Encapsula la lógica de los diferentes tipos de análisis faciales.
    """
    
    def __init__(self):
        """Inicializa el servicio con los analizadores necesarios"""
        self.skin_analyzer = SkinAnalyzer()
        self.emotion_analyzer = EmotionAnalyzer()
        self.age_gender_analyzer = AgeGenderAnalyzer()
        self.health_analyzer = HealthAnalyzer()
    
    def analyze_skin(self, image: np.ndarray) -> Dict[str, Any]:
        """Analiza características de la piel"""
        try:
            return self.skin_analyzer.analyze(image)
        except Exception as e:
            logger.error(f"Error en análisis de piel: {str(e)}")
            return {"error": str(e)}
    
    def analyze_emotion(self, image: np.ndarray) -> Dict[str, Any]:
        """Analiza emociones en el rostro"""
        try:
            return self.emotion_analyzer.analyze(image)
        except Exception as e:
            logger.error(f"Error en análisis de emociones: {str(e)}")
            return {"error": str(e)}
    
    def analyze_age_gender(self, image: np.ndarray) -> Dict[str, Any]:
        """Analiza edad y género aparentes"""
        try:
            return self.age_gender_analyzer.analyze(image)
        except Exception as e:
            logger.error(f"Error en análisis de edad y género: {str(e)}")
            return {"error": str(e)}
    
    def analyze_health(self, image: np.ndarray) -> Dict[str, Any]:
        """Analiza indicadores de salud en el rostro"""
        try:
            return self.health_analyzer.analyze(image)
        except Exception as e:
            logger.error(f"Error en análisis de salud: {str(e)}")
            return {"error": str(e)}
    
    def analyze_all(self, image: np.ndarray) -> Dict[str, Dict[str, Any]]:
        """
        Realiza un análisis completo del rostro
        
        Args:
            image: Imagen como array numpy
            
        Returns:
            Diccionario con resultados de todos los análisis
        """
        results = {
            "skin": self.analyze_skin(image),
            "emotion": self.analyze_emotion(image),
            "age_gender": self.analyze_age_gender(image),
            "health": self.analyze_health(image)
        }
        
        return results
