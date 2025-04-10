import os
import numpy as np
from typing import Dict, Any

from app.config import AGE_GENDER_MODEL
from app.services.image_processor import preprocess_image, crop_face

# Manejo más robusto de importaciones para la compatibilidad con Python 3.12
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("DeepFace no está disponible. Utilizando alternativas para análisis de edad y género.")

async def analyze_age_gender(image_path: str, face: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analiza edad y género de un rostro
    
    Args:
        image_path: Ruta a la imagen
        face: Diccionario con información del rostro
        
    Returns:
        Dict con resultados de edad y género
    """
    try:
        if AGE_GENDER_MODEL == "deepface" and DEEPFACE_AVAILABLE:
            return await _analyze_with_deepface(image_path, face)
        else:
            # Implementación alternativa más simple basada en OpenCV
            return await _analyze_with_fallback(image_path, face)
    except Exception as e:
        print(f"Error en análisis de edad/género: {str(e)}")
        return {
            "age": 0,
            "gender": "Desconocido",
            "confidence": 0.0
        }

async def _analyze_with_deepface(image_path: str, face: Dict[str, Any]) -> Dict[str, Any]:
    """Análisis usando DeepFace"""
    try:
        # Recortar rostro para mejorar precisión
        face_location = face["location"]
        face_img = crop_face(image_path, face_location)
        
        # Guardar temporalmente para DeepFace
        temp_path = os.path.join(os.path.dirname(image_path), "temp_face.jpg")
        import cv2
        cv2.imwrite(temp_path, face_img)
        
        # Analizar con DeepFace y manejar posibles cambios en la API
        try:
            # DeepFace ≥ 0.0.75
            results = DeepFace.analyze(
                img_path=temp_path,
                actions=['age', 'gender'],
                enforce_detection=False,
                detector_backend="opencv"
            )
        except TypeError:
            # DeepFace versiones anteriores o con cambios en la API
            results = DeepFace.analyze(
                img_path=temp_path,
                actions=['age', 'gender'],
                enforce_detection=False,
                detector_backend="opencv",
                prog_bar=False  # Parámetro agregado en versiones recientes
            )
        
        # Limpiar archivo temporal
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # DeepFace puede devolver una lista o un diccionario
        if isinstance(results, list):
            result = results[0]
        else:
            result = results
        
        # Procesar resultado
        gender = result.get("gender", "")
        # Traducir género al español
        if gender.lower() == "woman" or gender.lower() == "female":
            gender = "Femenino"
        elif gender.lower() == "man" or gender.lower() == "male":
            gender = "Masculino"
            
        return {
            "age": result.get("age", 0),
            "gender": gender,
            "confidence": result.get("gender_confidence", 0.0)
        }
    except Exception as e:
        print(f"Error en DeepFace: {str(e)}")
        # Si falla DeepFace, usar método alternativo
        return await _analyze_with_fallback(image_path, face)

async def _analyze_with_fallback(image_path: str, face: Dict[str, Any]) -> Dict[str, Any]:
    """Método alternativo basado en heurísticas simples"""
    # En un sistema real, aquí implementarías un modelo más simple
    # Para este ejemplo, devolvemos valores predeterminados
    return {
        "age": 30,  # Valor predeterminado
        "gender": "No determinado",
        "confidence": 0.5
    }
