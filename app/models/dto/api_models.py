from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field

class AnalysisRequestDTO(BaseModel):
    """DTO para las solicitudes de análisis facial"""
    session_id: Optional[str] = None
    options: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "abc123",
                "options": {
                    "detect_age": True,
                    "detect_gender": True,
                    "detect_emotion": True,
                    "detect_skin": True,
                    "detect_health": True
                }
            }
        }

class EmotionResultDTO(BaseModel):
    """DTO para los resultados de análisis de emociones"""
    dominant_emotion: str
    emotions: Dict[str, float]
    stress_level: Dict[str, Union[str, float]]
    social_expression: str

class AgeGenderResultDTO(BaseModel):
    """DTO para los resultados de edad y género"""
    age: Dict[str, Union[int, str]]
    gender: Dict[str, Union[str, float]]
    symmetry: Dict[str, Union[str, float]]

class SkinResultDTO(BaseModel):
    """DTO para los resultados de análisis de piel"""
    hydration: Dict[str, Union[str, float]]
    acne: Dict[str, Union[str, float]]
    wrinkles: Dict[str, Union[str, float]]
    pores: Dict[str, Union[str, float]]

class HealthResultDTO(BaseModel):
    """DTO para los indicadores de salud"""
    fatigue: Dict[str, Union[str, float]]
    stress: Dict[str, Union[str, float]]
    sleep: Dict[str, Union[str, float]]

class AnalysisResultDTO(BaseModel):
    """DTO para los resultados completos del análisis facial"""
    image_url: str
    session_id: Optional[str] = None
    age_gender: Optional[AgeGenderResultDTO] = None
    emotion: Optional[EmotionResultDTO] = None
    skin: Optional[SkinResultDTO] = None
    health: Optional[HealthResultDTO] = None
