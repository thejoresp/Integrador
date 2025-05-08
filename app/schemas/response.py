from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class SkinFeatures(BaseModel):
    """Características de la piel analizadas."""
    texture: str
    tone: str
    conditions: List[str]

class DermAnalysis(BaseModel):
    """Resultados del análisis de piel con Derm Foundation."""
    status: str
    embedding_dimensions: int
    skin_features: SkinFeatures
    message: Optional[str] = None

class FaceAnalysisResponse(BaseModel):
    """Respuesta completa del análisis facial."""
    image_url: str
    skin: Dict[str, Any]
    emotion: Dict[str, Any]
    age_gender: Dict[str, Any]
    health: Dict[str, Any]
    derm_analysis: Optional[DermAnalysis] = None
