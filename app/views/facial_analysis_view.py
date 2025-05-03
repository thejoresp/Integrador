"""
Vista para formatear los resultados del análisis facial.
Se encarga de transformar los modelos de dominio a esquemas Pydantic para la API.
"""

import logging
from typing import Dict, Any

from app.models.domain.facial_analysis import (
    FacialAnalysisResult, Face, AgeAnalysis,
    EmotionType
)
from app.schemas.facial_analysis import (
    FacialAnalysisResponseSchema, FaceSchema,
    AgeSchema, GenderSchema, EmotionSchema, 
    SkinSchema, HealthSchema, BoundingBoxSchema,
    LandmarksSchema, PointSchema
)

logger = logging.getLogger(__name__)


class FacialAnalysisView:
    """
    Vista para transformar los resultados del análisis facial en formatos apropiados
    para la respuesta API.
    """
    
    def format_analysis_result(self, result: FacialAnalysisResult) -> FacialAnalysisResponseSchema:
        """
        Formatea el resultado del análisis facial para la respuesta API.
        
        Args:
            result: Resultado del análisis facial (modelo de dominio)
            
        Returns:
            FacialAnalysisResponseSchema: Esquema formateado para la API
        """
        faces_schema = []
        
        for face in result.faces:
            # Formatear datos del rostro para la API
            face_schema = self._format_face(face)
            faces_schema.append(face_schema)
        
        # Crear respuesta completa
        response = FacialAnalysisResponseSchema(
            image_url=result.image_url,
            faces=faces_schema
        )
        
        return response
    
    def _format_face(self, face: Face) -> FaceSchema:
        """
        Formatea un objeto Face para la respuesta API.
        
        Args:
            face: Objeto Face con los análisis
            
        Returns:
            FaceSchema: Esquema del rostro formateado para la API
        """
        # Formatear caja delimitadora
        bounding_box = BoundingBoxSchema(
            x1=face.bounding_box.x1,
            y1=face.bounding_box.y1,
            x2=face.bounding_box.x2,
            y2=face.bounding_box.y2
        )
        
        # Formatear landmarks si existen
        landmarks = None
        if face.landmarks:
            points = [
                PointSchema(x=point.x, y=point.y)
                for point in face.landmarks.points
            ]
            landmarks = LandmarksSchema(points=points)
        
        # Formatear edad si existe
        age = None
        if face.age:
            age = AgeSchema(
                years=face.age.years,
                range=f"{face.age.range_min}-{face.age.range_max}"
            )
        
        # Formatear género si existe
        gender = None
        if face.gender:
            gender = GenderSchema(
                label=face.gender.label.value,
                confidence=face.gender.confidence
            )
        
        # Formatear emociones si existen
        emotions = None
        if face.emotions:
            emotions = EmotionSchema(
                dominant=face.emotions.dominant.value,
                scores={
                    emotion.value: score
                    for emotion, score in face.emotions.scores.items()
                }
            )
        
        # Formatear análisis de piel si existe
        skin = None
        if face.skin:
            skin = SkinSchema(
                texture=face.skin.texture,
                tone=face.skin.tone,
                features=face.skin.features
            )
        
        # Formatear indicadores de salud si existen
        health = None
        if face.health:
            health = HealthSchema(
                stress_level=face.health.stress_level,
                rest_indicator=face.health.rest_indicator,
                health_score=face.health.health_score
            )
        
        # Crear y devolver esquema completo
        return FaceSchema(
            bounding_box=bounding_box,
            landmarks=landmarks,
            age=age,
            gender=gender,
            emotions=emotions,
            skin=skin,
            health=health
        ) 