"""
Repositorio para el acceso a los modelos de machine learning.
Proporciona una capa de abstracción para cargar y utilizar diferentes modelos.
"""

import os
import logging
from typing import Dict, Any, Optional
import numpy as np

from app.config import MODEL_DIR

logger = logging.getLogger(__name__)


class ModelRepository:
    """
    Repositorio para gestionar el acceso a modelos de machine learning.
    
    Esta clase abstrae la carga y provisión de modelos preentrenados,
    proporcionando una interfaz única independiente de la tecnología subyacente.
    """
    
    def __init__(self):
        """Inicializa el repositorio con los modelos necesarios."""
        self._models = {}
        self._model_configs = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Inicializa y configura todos los modelos necesarios."""
        logger.info("Inicializando modelos de ML...")
        
        # En una implementación real, cargaríamos los modelos desde disco
        # Por ahora, simplemente registramos los modelos disponibles
        self._register_face_detection_models()
        self._register_age_gender_models()
        self._register_emotion_models()
        self._register_skin_analysis_models()
        
        logger.info(f"Modelos inicializados: {list(self._models.keys())}")
    
    def _register_face_detection_models(self):
        """Registra los modelos disponibles para detección facial."""
        self._model_configs["face_detection"] = {
            "mediapipe": {"name": "MediaPipe Face Detection"},
            "dlib": {"name": "Dlib Face Detection"},
            "opencv": {"name": "OpenCV Haar Cascade Face Detection"}
        }
    
    def _register_age_gender_models(self):
        """Registra los modelos disponibles para análisis de edad y género."""
        self._model_configs["age_gender"] = {
            "face-recognition": {"name": "Face Recognition Age-Gender Model"},
            "insightface": {"name": "InsightFace Age-Gender Model"},
            "deepface": {"name": "DeepFace Age-Gender Model"}
        }
    
    def _register_emotion_models(self):
        """Registra los modelos disponibles para análisis de emociones."""
        self._model_configs["emotion"] = {
            "mediapipe": {"name": "MediaPipe Emotion Analysis"},
            "fer": {"name": "FER Emotion Recognition"},
            "deepface": {"name": "DeepFace Emotion Recognition"}
        }
    
    def _register_skin_analysis_models(self):
        """Registra los modelos disponibles para análisis de piel."""
        self._model_configs["skin"] = {
            "custom": {"name": "Custom Skin Analysis Model"}
        }
    
    def get_model(self, model_type: str, model_name: Optional[str] = None) -> Any:
        """
        Obtiene un modelo específico.
        
        Args:
            model_type: Tipo de modelo (face_detection, age_gender, emotion, skin)
            model_name: Nombre específico del modelo (si no se proporciona, se usa el predeterminado)
            
        Returns:
            El modelo solicitado
            
        Raises:
            ValueError: Si el tipo o nombre de modelo no es válido
        """
        # Validar tipo de modelo
        if model_type not in self._model_configs:
            raise ValueError(f"Tipo de modelo no válido: {model_type}")
        
        # Si no se especifica modelo, usar el predeterminado para el tipo
        if model_name is None:
            model_name = self._get_default_model(model_type)
        
        # Validar nombre de modelo
        if model_name not in self._model_configs[model_type]:
            raise ValueError(f"Nombre de modelo no válido para {model_type}: {model_name}")
        
        # Si el modelo no está cargado, cargarlo
        model_key = f"{model_type}_{model_name}"
        if model_key not in self._models:
            self._load_model(model_type, model_name)
        
        return self._models.get(model_key)
    
    def _get_default_model(self, model_type: str) -> str:
        """Obtiene el modelo predeterminado para un tipo específico."""
        defaults = {
            "face_detection": "mediapipe",
            "age_gender": "face-recognition",
            "emotion": "mediapipe",
            "skin": "custom"
        }
        return defaults.get(model_type)
    
    def _load_model(self, model_type: str, model_name: str):
        """
        Carga un modelo específico en memoria.
        
        En una implementación real, aquí cargaríamos el modelo desde disco
        usando la biblioteca correspondiente (TensorFlow, PyTorch, etc.)
        """
        model_key = f"{model_type}_{model_name}"
        logger.info(f"Cargando modelo: {model_key}")
        
        # Simulamos la carga del modelo
        # En una implementación real, aquí cargaríamos el modelo real
        self._models[model_key] = {
            "type": model_type,
            "name": model_name,
            "config": self._model_configs[model_type][model_name]
        }
        
        logger.info(f"Modelo {model_key} cargado correctamente")
    
    def clean_up(self):
        """Libera recursos utilizados por los modelos."""
        logger.info("Liberando recursos de modelos...")
        self._models.clear() 