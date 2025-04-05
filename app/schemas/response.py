from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class FaceAnalysisResponse(BaseModel):
    """Modelo de respuesta para análisis facial completo"""
    image_url: str
    skin: Optional[Dict[str, Any]] = None
    emotion: Optional[Dict[str, Any]] = None
    age_gender: Optional[Dict[str, Any]] = None
    health: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
