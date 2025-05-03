"""
Esquemas Pydantic para la validación y serialización de datos de análisis facial.
Estos modelos definen la estructura de datos para las API de análisis facial.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class PointSchema(BaseModel):
    """Esquema para un punto 2D."""
    x: float = Field(..., description="Coordenada X del punto")
    y: float = Field(..., description="Coordenada Y del punto")


class BoundingBoxSchema(BaseModel):
    """Esquema para la caja delimitadora de un rostro."""
    x1: int = Field(..., description="Coordenada X1 (superior izquierda)")
    y1: int = Field(..., description="Coordenada Y1 (superior izquierda)")
    x2: int = Field(..., description="Coordenada X2 (inferior derecha)")
    y2: int = Field(..., description="Coordenada Y2 (inferior derecha)")


class LandmarksSchema(BaseModel):
    """Esquema para los puntos característicos faciales."""
    points: List[PointSchema] = Field(..., description="Lista de puntos faciales")


class AgeSchema(BaseModel):
    """Esquema para el análisis de edad."""
    years: float = Field(..., description="Edad estimada en años")
    range: str = Field(..., description="Rango de edad estimado")


class GenderSchema(BaseModel):
    """Esquema para el análisis de género."""
    label: str = Field(..., description="Género estimado")
    confidence: float = Field(..., ge=0, le=1, description="Confianza de la estimación")


class EmotionSchema(BaseModel):
    """Esquema para el análisis de emociones."""
    dominant: str = Field(..., description="Emoción dominante")
    scores: Dict[str, float] = Field(
        ..., description="Puntuaciones para cada emoción detectada"
    )


class SkinSchema(BaseModel):
    """Esquema para el análisis de piel."""
    texture: str = Field(..., description="Textura de la piel")
    tone: str = Field(..., description="Tono de la piel")
    features: Dict[str, float] = Field(
        ..., description="Características detectadas y sus puntuaciones"
    )


class HealthSchema(BaseModel):
    """Esquema para indicadores de salud."""
    stress_level: float = Field(..., ge=0, le=1, description="Nivel de estrés estimado")
    rest_indicator: float = Field(..., ge=0, le=1, description="Indicador de descanso")
    health_score: float = Field(..., ge=0, le=1, description="Puntuación general de salud")


class FaceSchema(BaseModel):
    """Esquema para un rostro detectado con su análisis."""
    bounding_box: BoundingBoxSchema
    landmarks: Optional[LandmarksSchema] = None
    age: Optional[AgeSchema] = None
    gender: Optional[GenderSchema] = None
    emotions: Optional[EmotionSchema] = None
    skin: Optional[SkinSchema] = None
    health: Optional[HealthSchema] = None

    class Config:
        json_schema_extra = {
            "example": {
                "bounding_box": {"x1": 10, "y1": 20, "x2": 210, "y2": 220},
                "landmarks": {"points": [{"x": 50, "y": 60}, {"x": 70, "y": 80}]},
                "age": {"years": 28.5, "range": "25-32"},
                "gender": {"label": "masculino", "confidence": 0.92},
                "emotions": {
                    "dominant": "feliz",
                    "scores": {"feliz": 0.8, "neutral": 0.15, "triste": 0.05}
                }
            }
        }


class FacialAnalysisResponseSchema(BaseModel):
    """Esquema para la respuesta de análisis facial."""
    image_url: str = Field(..., description="URL de la imagen analizada")
    faces: List[FaceSchema] = Field(..., description="Lista de rostros detectados y analizados")

    class Config:
        json_schema_extra = {
            "example": {
                "image_url": "/uploads/8cb8e51e-b5e9-401e-9c7a-fa01ce5363d3.jpg",
                "faces": [
                    {
                        "bounding_box": {"x1": 10, "y1": 20, "x2": 210, "y2": 220},
                        "age": {"years": 28.5, "range": "25-32"},
                        "gender": {"label": "masculino", "confidence": 0.92},
                        "emotions": {
                            "dominant": "feliz",
                            "scores": {"feliz": 0.8, "neutral": 0.15, "triste": 0.05}
                        }
                    }
                ]
            }
        } 