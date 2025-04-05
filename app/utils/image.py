import cv2
import numpy as np
from fastapi import UploadFile
import os

def validate_image(file: UploadFile) -> bool:
    """
    Valida que el archivo sea una imagen en formato permitido
    
    Args:
        file: Archivo subido
        
    Returns:
        bool: True si el archivo es válido, False en caso contrario
    """
    # Verificar extensión
    valid_extensions = ['.jpg', '.jpeg', '.png']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in valid_extensions:
        return False
    
    # Verificar content_type
    valid_types = ['image/jpeg', 'image/png']
    if file.content_type not in valid_types:
        return False
    
    return True

def process_image(image_path: str, max_size: int = 800) -> np.ndarray:
    """
    Procesa una imagen para análisis
    
    Args:
        image_path: Ruta de la imagen
        max_size: Tamaño máximo para cualquier dimensión
        
    Returns:
        np.ndarray: Imagen procesada
    """
    # Leer imagen
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("No se pudo leer la imagen")
    
    # Redimensionar si es necesario
    height, width = img.shape[:2]
    if height > max_size or width > max_size:
        scale = max_size / max(height, width)
        img = cv2.resize(img, (int(width * scale), int(height * scale)))
    
    return img
