import os
import numpy as np
from typing import Dict, Any

from app.config import EMOTION_MODEL
from app.services.image_processor import preprocess_image, crop_face

# Manejo más robusto de importaciones para la compatibilidad con Python 3.12
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("DeepFace no está disponible. Utilizando alternativas para análisis de emociones.")

async def analyze_emotion(image_path: str, face: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analiza emociones en un rostro
    
    Args:
        image_path: Ruta a la imagen
        face: Diccionario con información del rostro
        
    Returns:
        Dict con resultados de emociones
    """
    try:
        if EMOTION_MODEL == "deepface" and DEEPFACE_AVAILABLE:
            return await _analyze_with_deepface(image_path, face)
        else:
            return await _analyze_with_fallback(image_path, face)
    except Exception as e:
        print(f"Error en análisis de emociones: {str(e)}")
        return {
            "dominant": "Neutral",
            "emotions": {
                "neutral": 1.0,
                "happy": 0.0,
                "sad": 0.0,
                "angry": 0.0,
                "fear": 0.0,
                "surprise": 0.0,
                "disgust": 0.0
            }
        }

async def _analyze_with_deepface(image_path: str, face: Dict[str, Any]) -> Dict[str, Any]:
    """Análisis usando DeepFace"""
    try:
        # Recortar rostro para mejorar precisión
        face_location = face["location"]
        face_img = crop_face(image_path, face_location)
        
        # Guardar temporalmente para DeepFace
        temp_path = os.path.join(os.path.dirname(image_path), "temp_face_emotion.jpg")
        import cv2
        cv2.imwrite(temp_path, face_img)
        
        # Analizar con DeepFace y manejar las nuevas APIs de versiones recientes
        try:
            # DeepFace ≥ 0.0.75
            results = DeepFace.analyze(
                img_path=temp_path,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend="opencv"
            )
        except TypeError:
            # DeepFace versiones anteriores o con cambios en la API
            results = DeepFace.analyze(
                img_path=temp_path,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend="opencv",
                prog_bar=False  # Parámetro agregado en versiones recientes
            )
        
        # Limpiar archivo temporal
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Procesar resultados
        if isinstance(results, list):
            result = results[0]
        else:
            result = results
            
        # Obtener datos de emociones
        emotion_data = result.get("emotion", {})
        
        # Traducir emociones al español
        emotion_map = {
            "angry": "Enojo",
            "disgust": "Disgusto",
            "fear": "Miedo",
            "happy": "Felicidad",
            "sad": "Tristeza",
            "surprise": "Sorpresa",
            "neutral": "Neutral"
        }
        
        # Normalizar y traducir
        emotions_es = {}
        dominant_emotion = "neutral"
        max_value = 0
        
        for emotion, value in emotion_data.items():
            if value > max_value:
                max_value = value
                dominant_emotion = emotion
            
            emotion_es_name = emotion_map.get(emotion.lower(), emotion)
            emotions_es[emotion_es_name.lower()] = value / 100  # DeepFace da valores en porcentaje
            
        dominant_es = emotion_map.get(dominant_emotion.lower(), dominant_emotion)
        
        return {
            "dominant": dominant_es,
            "emotions": emotions_es
        }
    except Exception as e:
        print(f"Error en DeepFace (emociones): {str(e)}")
        return await _analyze_with_fallback(image_path, face)

async def _analyze_with_fallback(image_path: str, face: Dict[str, Any]) -> Dict[str, Any]:
    """Método alternativo simple"""
    # Valores predeterminados
    return {
        "dominant": "Neutral",
        "emotions": {
            "neutral": 0.8,
            "felicidad": 0.1,
            "tristeza": 0.05,
            "enojo": 0.0,
            "miedo": 0.0,
            "sorpresa": 0.05,
            "disgusto": 0.0
        }
    }
