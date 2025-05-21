from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field

class FaceLocation(BaseModel):
    x: int
    y: int
    width: int
    height: int

class FaceLandmarks(BaseModel):
    points: Dict[str, Dict[str, float]]

class AgeGenderResult(BaseModel):
    age: int
    gender: str
    confidence: float

class EmotionResult(BaseModel):
    dominant: str
    emotions: Dict[str, float]

class SkinAnalysisResult(BaseModel):
    hydration: str
    texture: str
    pores: str
    lesions: Optional[List[str]] = None
    concerns: Optional[List[str]] = None

class HealthIndicators(BaseModel):
    stress_level: str
    fatigue: str
    eye_fatigue: str
    posture: Optional[str] = None
    nutritional_hints: Optional[List[str]] = None

class SymmetryResult(BaseModel):
    score: float
    analysis: str
    details: Optional[Dict[str, Any]] = None

class AnalysisModuleResult(BaseModel):
    age_gender: Optional[AgeGenderResult] = None
    emotion: Optional[EmotionResult] = None
    skin: Optional[SkinAnalysisResult] = None
    health: Optional[HealthIndicators] = None
    symmetry: Optional[SymmetryResult] = None

class AnalysisResult(BaseModel):
    image_id: str
    timestamp: str
    face_count: int
    analyses: AnalysisModuleResult = Field(default_factory=AnalysisModuleResult)

class AnalysisRequest(BaseModel):
    analysis_types: List[str] = ["all"]
