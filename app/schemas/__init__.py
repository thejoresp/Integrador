"""
Paquete de esquemas para la aplicación de análisis facial.
"""

from app.schemas.facial_analysis import (
    PointSchema, BoundingBoxSchema, LandmarksSchema,
    AgeSchema, GenderSchema, EmotionSchema, SkinSchema,
    HealthSchema, FaceSchema, FacialAnalysisResponseSchema
)

__all__ = [
    "PointSchema",
    "BoundingBoxSchema",
    "LandmarksSchema",
    "AgeSchema",
    "GenderSchema",
    "EmotionSchema",
    "SkinSchema",
    "HealthSchema",
    "FaceSchema",
    "FacialAnalysisResponseSchema"
] 