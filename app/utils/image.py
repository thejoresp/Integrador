"""
Utilidades para el procesamiento y manipulación de imágenes.

Este módulo proporciona funciones para validar, procesar y limpiar
archivos de imágenes utilizados en el análisis facial.
"""
import cv2
import numpy as np
import os
from typing import Optional, Tuple, Union
from fastapi import UploadFile

from app.config import logger, config

def validate_image(file: UploadFile) -> bool:
    """
    Valida que el archivo sea una imagen en formato permitido.
    
    Args:
        file: Archivo subido por el usuario
        
    Returns:
        bool: True si el archivo es válido, False en caso contrario
    """
    # Verificar que existe el archivo
    if not file or not file.filename:
        logger.warning("Intento de validar un archivo sin nombre")
        return False
    
    # Verificar extensión
    if not config.validate_file_extension(file.filename):
        logger.warning(f"Extensión no válida: {file.filename}")
        return False
    
    # Verificar content_type
    valid_types = ['image/jpeg', 'image/png']
    if file.content_type not in valid_types:
        logger.warning(f"Tipo de contenido no válido: {file.content_type}")
        return False
    
    return True

def process_image(
    image_path: str, 
    max_size: int = 800,
    grayscale: bool = False
) -> np.ndarray:
    """
    Procesa una imagen para análisis, redimensionándola si es necesario.
    
    Args:
        image_path: Ruta absoluta a la imagen
        max_size: Tamaño máximo para cualquier dimensión
        grayscale: Si es True, convierte la imagen a escala de grises
        
    Returns:
        np.ndarray: Imagen procesada como array de NumPy
        
    Raises:
        ValueError: Si no se puede leer la imagen o hay otro error de procesamiento
    """
    try:
        # Leer imagen
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"No se pudo leer la imagen en {image_path}")
        
        # Redimensionar si es necesario
        height, width = img.shape[:2]
        if height > max_size or width > max_size:
            scale = max_size / max(height, width)
            img = cv2.resize(img, (int(width * scale), int(height * scale)))
        
        # Convertir a escala de grises si se solicita
        if grayscale:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
        return img
        
    except Exception as e:
        logger.error(f"Error al procesar imagen {image_path}: {str(e)}")
        raise ValueError(f"Error al procesar la imagen: {str(e)}") from e

def cleanup_uploaded_file(file_path: str) -> bool:
    """
    Elimina un archivo temporal después de procesarlo.
    
    Args:
        file_path: Ruta absoluta al archivo a eliminar
        
    Returns:
        bool: True si se eliminó correctamente, False en caso contrario
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Archivo eliminado correctamente: {file_path}")
            return True
        else:
            logger.warning(f"Intento de eliminar un archivo inexistente: {file_path}")
            return False
    except Exception as e:
        logger.error(f"Error al eliminar archivo {file_path}: {str(e)}")
        return False

def crop_face(
    image: Union[str, np.ndarray], 
    face_location: Tuple[int, int, int, int],
    add_margin: float = 0.0
) -> np.ndarray:
    """
    Recorta un rostro de una imagen basándose en sus coordenadas.
    
    Args:
        image: Ruta a la imagen o array de NumPy
        face_location: Tupla (x, y, w, h) con las coordenadas del rostro
        add_margin: Margen adicional alrededor del rostro (0.2 = 20%)
        
    Returns:
        np.ndarray: Imagen recortada con el rostro
    """
    # Cargar imagen si se proporciona ruta
    if isinstance(image, str):
        img = cv2.imread(image)
        if img is None:
            raise ValueError(f"No se pudo leer la imagen en {image}")
    else:
        img = image.copy()
    
    # Extraer coordenadas
    x, y, w, h = face_location
    
    # Calcular margen adicional
    if add_margin > 0:
        margin_x = int(w * add_margin)
        margin_y = int(h * add_margin)
        
        # Ajustar coordenadas con margen, respetando límites de la imagen
        height, width = img.shape[:2]
        x = max(0, x - margin_x)
        y = max(0, y - margin_y)
        w = min(width - x, w + 2 * margin_x)
        h = min(height - y, h + 2 * margin_y)
    
    # Recortar y devolver
    return img[y:y+h, x:x+w]
