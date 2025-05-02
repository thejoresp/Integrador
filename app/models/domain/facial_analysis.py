from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union, Tuple

@dataclass
class FaceLocation:
    """Representa la ubicación de un rostro en una imagen"""
    x: int
    y: int
    width: int
    height: int

@dataclass
class AgeAnalysis:
    """Representa el análisis de edad de un rostro"""
    years: int
    range: str
    confidence: float

@dataclass
class GenderAnalysis:
    """Representa el análisis de género de un rostro"""
    label: str
    confidence: float

@dataclass
class SymmetryAnalysis:
    """Representa el análisis de simetría facial"""
    score: float
    level: str

@dataclass
class AgeGenderAnalysis:
    """Representa el análisis combinado de edad y género"""
    age: AgeAnalysis
    gender: GenderAnalysis
    symmetry: SymmetryAnalysis

@dataclass
class EmotionScores:
    """Representa los puntajes de cada emoción detectada"""
    happy: float = 0.0
    sad: float = 0.0
    angry: float = 0.0
    fear: float = 0.0
    surprise: float = 0.0
    neutral: float = 0.0
    disgust: float = 0.0
    contempt: float = 0.0

@dataclass
class StressLevel:
    """Representa el nivel de estrés detectado"""
    score: float
    level: str

@dataclass
class EmotionAnalysis:
    """Representa el análisis emocional completo"""
    dominant_emotion: str
    emotions: Dict[str, float]
    stress_level: StressLevel
    social_expression: str

@dataclass
class SkinMetric:
    """Representa una métrica de análisis de piel"""
    score: float
    level: str

@dataclass
class SkinAnalysis:
    """Representa el análisis completo de la piel"""
    hydration: SkinMetric
    acne: SkinMetric
    wrinkles: SkinMetric
    pores: SkinMetric

@dataclass
class HealthMetric:
    """Representa una métrica de salud"""
    score: float
    level: str

@dataclass
class HealthAnalysis:
    """Representa el análisis de indicadores de salud"""
    fatigue: HealthMetric
    stress: HealthMetric
    sleep: HealthMetric

@dataclass
class FacialAnalysis:
    """Representa el análisis facial completo"""
    image_path: str
    image_url: Optional[str] = None
    session_id: Optional[str] = None
    face_location: Optional[FaceLocation] = None
    age_gender: Optional[AgeGenderAnalysis] = None
    emotion: Optional[EmotionAnalysis] = None
    skin: Optional[SkinAnalysis] = None
    health: Optional[HealthAnalysis] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el análisis facial a un diccionario"""
        result = {
            "image_url": self.image_url,
            "session_id": self.session_id
        }
        
        # Incluir análisis de edad y género si está disponible
        if self.age_gender:
            result["age_gender"] = {
                "age": {
                    "years": self.age_gender.age.years,
                    "range": self.age_gender.age.range,
                    "confidence": self.age_gender.age.confidence
                },
                "gender": {
                    "label": self.age_gender.gender.label,
                    "confidence": self.age_gender.gender.confidence
                },
                "symmetry": {
                    "score": self.age_gender.symmetry.score,
                    "level": self.age_gender.symmetry.level
                }
            }
        
        # Incluir análisis de emociones si está disponible
        if self.emotion:
            result["emotion"] = {
                "dominant_emotion": self.emotion.dominant_emotion,
                "emotions": self.emotion.emotions,
                "stress_level": {
                    "score": self.emotion.stress_level.score,
                    "level": self.emotion.stress_level.level
                },
                "social_expression": self.emotion.social_expression
            }
        
        # Incluir análisis de piel si está disponible
        if self.skin:
            result["skin"] = {
                "hydration": {
                    "score": self.skin.hydration.score,
                    "level": self.skin.hydration.level
                },
                "acne": {
                    "score": self.skin.acne.score,
                    "level": self.skin.acne.level
                },
                "wrinkles": {
                    "score": self.skin.wrinkles.score,
                    "level": self.skin.wrinkles.level
                },
                "pores": {
                    "score": self.skin.pores.score,
                    "level": self.skin.pores.level
                }
            }
        
        # Incluir análisis de salud si está disponible
        if self.health:
            result["health"] = {
                "fatigue": {
                    "score": self.health.fatigue.score,
                    "level": self.health.fatigue.level
                },
                "stress": {
                    "score": self.health.stress.score,
                    "level": self.health.stress.level
                },
                "sleep": {
                    "score": self.health.sleep.score,
                    "level": self.health.sleep.level
                }
            }
        
        return result
