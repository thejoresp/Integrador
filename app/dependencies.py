"""
Módulo de dependencias para inyección en FastAPI.

Centraliza la creación e inicialización de servicios y componentes 
que serán inyectados como dependencias en las rutas.
"""
from typing import Dict, Tuple, Any
from fastapi import Depends

from app.analyzers.age_gender import AgeGenderAnalyzer
from app.analyzers.emotion import EmotionAnalyzer
from app.analyzers.skin import SkinAnalyzer
from app.analyzers.health import HealthAnalyzer
from app.analyzers.symmetry import SymmetryAnalyzer

# Caché de instancias singleton
_age_gender_analyzer = None
_emotion_analyzer = None
_skin_analyzer = None
_health_analyzer = None
_symmetry_analyzer = None

def get_age_gender_analyzer() -> AgeGenderAnalyzer:
    """Proporciona una instancia singleton del analizador de edad y género."""
    global _age_gender_analyzer
    if _age_gender_analyzer is None:
        _age_gender_analyzer = AgeGenderAnalyzer()
    return _age_gender_analyzer

def get_emotion_analyzer() -> EmotionAnalyzer:
    """Proporciona una instancia singleton del analizador de emociones."""
    global _emotion_analyzer
    if _emotion_analyzer is None:
        _emotion_analyzer = EmotionAnalyzer()
    return _emotion_analyzer

def get_skin_analyzer() -> SkinAnalyzer:
    """Proporciona una instancia singleton del analizador de piel."""
    global _skin_analyzer
    if _skin_analyzer is None:
        _skin_analyzer = SkinAnalyzer()
    return _skin_analyzer

def get_health_analyzer() -> HealthAnalyzer:
    """Proporciona una instancia singleton del analizador de salud."""
    global _health_analyzer
    if _health_analyzer is None:
        _health_analyzer = HealthAnalyzer()
    return _health_analyzer

def get_symmetry_analyzer() -> SymmetryAnalyzer:
    """Proporciona una instancia singleton del analizador de simetría."""
    global _symmetry_analyzer
    if _symmetry_analyzer is None:
        _symmetry_analyzer = SymmetryAnalyzer()
    return _symmetry_analyzer

def get_analyzers(
    age_gender: AgeGenderAnalyzer = Depends(get_age_gender_analyzer),
    emotion: EmotionAnalyzer = Depends(get_emotion_analyzer),
    skin: SkinAnalyzer = Depends(get_skin_analyzer),
    health: HealthAnalyzer = Depends(get_health_analyzer),
    symmetry: SymmetryAnalyzer = Depends(get_symmetry_analyzer)
) -> Dict[str, Any]:
    """
    Proporciona todos los analizadores como un diccionario para inyección en endpoints.
    
    Args:
        age_gender: Analizador de edad y género
        emotion: Analizador de emociones
        skin: Analizador de piel
        health: Analizador de salud
        symmetry: Analizador de simetría
        
    Returns:
        Dict con todos los analizadores
    """
    return {
        "age_gender": age_gender,
        "emotion": emotion,
        "skin": skin,
        "health": health,
        "symmetry": symmetry
    }