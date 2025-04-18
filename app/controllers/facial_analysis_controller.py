"""
Controlador principal para análisis facial.

Este módulo implementa el controlador que maneja las solicitudes de análisis facial,
siguiendo el patrón MVC (Modelo-Vista-Controlador).
"""
import os
import uuid
import cv2
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional

from app.models.domain.facial_analysis import (
    Face, 
    AgeGenderAnalysis,
    EmotionAnalysis,
    SkinAnalysis,
    HealthAnalysis,
    SymmetryAnalysis
)
from app.models.dto.api_models import (
    AnalysisRequestDTO,
    AnalysisResultDTO,
    FaceDTO
)
from app.config import UPLOAD_DIR, logger
from app.utils.image import cleanup_uploaded_file
from app.services.face_detector import detect_faces
from app.services.image_processor import validate_image, save_upload
from app.dependencies import get_analyzers


class FacialAnalysisController:
    """
    Controlador para el análisis facial.
    
    Esta clase maneja las operaciones relacionadas con el análisis de rostros en imágenes,
    coordinando la interacción entre los modelos y las vistas.
    """
    
    def __init__(self, analyzers: Dict[str, Any]):
        """
        Inicializa el controlador con los analizadores necesarios.
        
        Args:
            analyzers: Diccionario con los analizadores de características faciales
        """
        self.analyzers = analyzers
        
    async def process_analysis_request(
        self, 
        image_path: str, 
        request: AnalysisRequestDTO
    ) -> Tuple[Optional[AnalysisResultDTO], Optional[str]]:
        """
        Procesa una solicitud de análisis facial.
        
        Args:
            image_path: Ruta a la imagen a analizar
            request: DTO con la configuración del análisis
            
        Returns:
            Tuple con el DTO de resultado y un mensaje de error (si ocurre)
        """
        try:
            # Validar que la imagen contiene un rostro
            if not await validate_image(image_path):
                cleanup_uploaded_file(image_path)
                return None, "No se detectó un rostro válido en la imagen"
            
            # Detectar rostros
            faces = await detect_faces(image_path)
            if not faces:
                cleanup_uploaded_file(image_path)
                return None, "No se pudo analizar el rostro correctamente"
            
            # Obtener nombre del archivo
            file_name = os.path.basename(image_path)
            
            # Preparar resultados
            result = AnalysisResultDTO(
                image_id=file_name,
                timestamp=datetime.now(),
                face_count=len(faces),
                analyses={}
            )
            
            # Obtener imagen como array para los analizadores
            image_array = cv2.imread(image_path)
            
            # Realizar análisis solicitados
            await self._perform_analyses(image_array, result, request.analysis_types)
            
            return result, None
            
        except Exception as e:
            logger.error(f"Error en análisis facial: {str(e)}", exc_info=True)
            return None, f"Error en el análisis: {str(e)}"
    
    async def _perform_analyses(
        self, 
        image_array, 
        result: AnalysisResultDTO, 
        analysis_types: List[str]
    ) -> None:
        """
        Realiza los análisis solicitados en la imagen.
        
        Args:
            image_array: Imagen como array de numpy
            result: DTO donde se guardarán los resultados
            analysis_types: Tipos de análisis solicitados
        """
        analysis_mapping = {
            "age_gender": self.analyzers["age_gender"],
            "emotion": self.analyzers["emotion"],
            "skin": self.analyzers["skin"],
            "health": self.analyzers["health"],
            "symmetry": self.analyzers["symmetry"]
        }
        
        # Determinar qué análisis realizar
        analyses_to_perform = list(analysis_mapping.keys()) if "all" in analysis_types else analysis_types
        
        # Realizar cada análisis solicitado
        for analysis_type in analyses_to_perform:
            if analysis_type in analysis_mapping:
                analyzer = analysis_mapping[analysis_type]
                result.analyses[analysis_type] = analyzer.analyze(image_array)
    
    def generate_mock_result(self, image_id: str) -> AnalysisResultDTO:
        """
        Genera resultados simulados para demostración.
        
        Args:
            image_id: ID de la imagen
            
        Returns:
            DTO con resultados simulados
        """
        return AnalysisResultDTO(
            image_id=image_id,
            timestamp=datetime.now(),
            face_count=1,
            analyses={
                "age_gender": {"age": 28, "gender": "Masculino", "confidence": 0.92},
                "emotion": {
                    "dominant": "Neutral", 
                    "emotions": {"neutral": 0.7, "happy": 0.2, "sad": 0.05, "angry": 0.05}
                },
                "skin": {"hydration": "Buena", "texture": "Normal", "pores": "Moderados"},
                "health": {"stress_level": "Bajo", "fatigue": "Mínima", "eye_fatigue": "No detectada"},
                "symmetry": {"score": 0.85, "analysis": "Rostro con buena simetría"}
            }
        )