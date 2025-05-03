"""
Modelos de dominio para el análisis facial.
Estos modelos representan las entidades principales del dominio del análisis facial.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum


class Gender(str, Enum):
    """Enumeración para género."""
    MALE = "masculino"
    FEMALE = "femenino"
    UNKNOWN = "desconocido"


class EmotionType(str, Enum):
    """Enumeración para tipos de emoción."""
    HAPPY = "feliz"
    SAD = "triste"
    ANGRY = "enojado"
    SURPRISED = "sorprendido"
    FEARFUL = "temeroso"
    DISGUSTED = "disgustado"
    NEUTRAL = "neutral"


@dataclass
class Point:
    """Representa un punto 2D."""
    x: float
    y: float


@dataclass
class BoundingBox:
    """Representa una caja delimitadora de un rostro."""
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1


@dataclass
class FacialLandmarks:
    """Puntos clave faciales."""
    points: List[Point]


@dataclass
class AgeAnalysis:
    """Análisis de edad."""
    years: float
    range_min: int
    range_max: int


@dataclass
class GenderAnalysis:
    """Análisis de género."""
    label: Gender
    confidence: float


@dataclass
class SymmetryAnalysis:
    """Análisis de simetría facial."""
    score: float
    level: str


@dataclass
class EmotionAnalysis:
    """Análisis de emociones."""
    dominant: EmotionType
    scores: Dict[EmotionType, float]


@dataclass
class SkinAnalysis:
    """Análisis de la piel."""
    texture: str
    tone: str
    features: Dict[str, float]


@dataclass
class HealthIndicators:
    """Indicadores de salud basados en apariencia facial."""
    stress_level: float
    rest_indicator: float
    health_score: float


@dataclass
class Face:
    """Representa un rostro detectado con todas sus características."""
    bounding_box: BoundingBox
    landmarks: Optional[FacialLandmarks] = None
    age: Optional[AgeAnalysis] = None
    gender: Optional[GenderAnalysis] = None
    symmetry: Optional[SymmetryAnalysis] = None
    emotions: Optional[EmotionAnalysis] = None
    skin: Optional[SkinAnalysis] = None
    health: Optional[HealthIndicators] = None


@dataclass
class FacialAnalysisResult:
    """Resultado del análisis facial completo."""
    image_url: str
    faces: List[Face]
