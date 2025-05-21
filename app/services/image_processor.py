import os
import cv2
import numpy as np
from fastapi import UploadFile
from typing import Any, Tuple
from PIL import Image

from app.services.face_detector import detect_faces

async def validate_image(image_path: str) -> bool:
    """
    Valida que una imagen sea adecuada para el análisis facial
    
    Args:
        image_path: Ruta a la imagen a validar
        
    Returns:
        bool: True si la imagen es válida, False en caso contrario
    """
    try:
        # Verificar que el archivo existe
        if not os.path.exists(image_path):
            return False
        
        # Leer la imagen
        image = cv2.imread(image_path)
        if image is None:
            return False
        
        # Verificar dimensiones mínimas
        height, width = image.shape[:2]
        if height < 100 or width < 100:
            return False
        
        # Verificar que contenga al menos un rostro
        faces = await detect_faces(image_path)
        if not faces:
            return False
        
        return True
    except Exception as e:
        print(f"Error al validar imagen: {str(e)}")
        return False

async def save_upload(upload_file: UploadFile, destination: str) -> bool:
    """
    Guarda un archivo subido a la ubicación especificada
    
    Args:
        upload_file: Archivo subido por el usuario
        destination: Ruta donde guardar el archivo
        
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        # Leer el contenido del archivo
        content = await upload_file.read()
        
        # Verificar que el archivo no esté vacío
        if not content:
            return False
        
        # Guardar el archivo
        with open(destination, "wb") as f:
            f.write(content)
            
        return os.path.exists(destination)
    except Exception as e:
        print(f"Error al guardar archivo: {str(e)}")
        return False

def preprocess_image(image_path: str, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """
    Preprocesa una imagen para análisis con redes neuronales
    
    Args:
        image_path: Ruta a la imagen
        target_size: Tamaño objetivo para redimensionar
        
    Returns:
        numpy.ndarray: Imagen preprocesada
    """
    try:
        # Abrir la imagen con PIL
        img = Image.open(image_path)
        img = img.resize(target_size)
        img_array = np.array(img) / 255.0  # Normalización
        
        # Expandir dimensiones para modelos que esperan lotes
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        print(f"Error al preprocesar imagen: {str(e)}")
        return np.array([])

def crop_face(image_path: str, face_location: dict) -> np.ndarray:
    """
    Recorta un rostro de una imagen
    
    Args:
        image_path: Ruta a la imagen
        face_location: Diccionario con las coordenadas del rostro
        
    Returns:
        numpy.ndarray: Imagen recortada del rostro
    """
    try:
        image = cv2.imread(image_path)
        x = face_location["x"]
        y = face_location["y"]
        w = face_location["width"]
        h = face_location["height"]
        
        # Aplicar un pequeño margen
        margin = int(min(w, h) * 0.1)
        x = max(0, x - margin)
        y = max(0, y - margin)
        w = min(image.shape[1] - x, w + 2 * margin)
        h = min(image.shape[0] - y, h + 2 * margin)
        
        face_img = image[y:y+h, x:x+w]
        return face_img
    except Exception as e:
        print(f"Error al recortar rostro: {str(e)}")
        return np.array([])
