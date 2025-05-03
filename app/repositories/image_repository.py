"""
Repositorio para la gestión de imágenes.
Proporciona una capa de abstracción para las operaciones de almacenamiento y recuperación de imágenes.
"""

import os
import uuid
import logging
from typing import Tuple, Optional
import cv2
import numpy as np
from fastapi import UploadFile

from app.config import UPLOAD_DIR
from app.exceptions.base import ImageProcessingError, InvalidImageFormatError

logger = logging.getLogger(__name__)


class ImageRepository:
    """
    Repositorio para gestionar el almacenamiento y recuperación de imágenes.
    
    Esta clase proporciona métodos para guardar, recuperar y procesar imágenes,
    abstrayendo los detalles de implementación del almacenamiento.
    """
    
    def __init__(self, upload_dir: str = UPLOAD_DIR):
        """
        Inicializa el repositorio con el directorio de carga.
        
        Args:
            upload_dir: Directorio donde se almacenarán las imágenes
        """
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def validate_image(self, file: UploadFile) -> bool:
        """
        Valida que el archivo sea una imagen válida.
        
        Args:
            file: Archivo subido a través de FastAPI
            
        Returns:
            bool: True si es válido, False en caso contrario
            
        Raises:
            InvalidImageFormatError: Si el formato de la imagen no es válido
        """
        allowed_extensions = {"jpg", "jpeg", "png"}
        
        # Verificar extensión
        extension = self._get_file_extension(file.filename)
        if extension.lower() not in allowed_extensions:
            raise InvalidImageFormatError(
                f"Formato no válido: {extension}. Usar: {', '.join(allowed_extensions)}"
            )
        
        return True
    
    def _get_file_extension(self, filename: str) -> str:
        """
        Obtiene la extensión de un archivo.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            str: Extensión del archivo
        """
        return filename.split(".")[-1] if "." in filename else ""
    
    async def save_image(self, file: UploadFile) -> Tuple[str, str]:
        """
        Guarda una imagen en el sistema de archivos.
        
        Args:
            file: Archivo subido a través de FastAPI
            
        Returns:
            Tuple[str, str]: Ruta completa del archivo guardado y nombre del archivo
            
        Raises:
            ImageProcessingError: Si hay un error al guardar la imagen
        """
        # Validar la imagen
        self.validate_image(file)
        
        # Generar un nombre único para el archivo
        file_id = str(uuid.uuid4())
        extension = self._get_file_extension(file.filename)
        file_name = f"{file_id}.{extension}"
        file_path = os.path.join(self.upload_dir, file_name)
        
        # Guardar el archivo
        try:
            # Leer el contenido del archivo
            content = await file.read()
            
            # Escribir el contenido en el sistema de archivos
            with open(file_path, "wb") as f:
                f.write(content)
            
            logger.info(f"Imagen guardada: {file_path}")
            return file_path, file_name
        
        except Exception as e:
            logger.error(f"Error al guardar la imagen: {str(e)}")
            raise ImageProcessingError(f"Error al guardar la imagen: {str(e)}")
    
    def load_image(self, file_path: str) -> np.ndarray:
        """
        Carga una imagen desde el sistema de archivos.
        
        Args:
            file_path: Ruta del archivo a cargar
            
        Returns:
            np.ndarray: Imagen como matriz numpy
            
        Raises:
            ImageProcessingError: Si hay un error al cargar la imagen
        """
        if not os.path.exists(file_path):
            raise ImageProcessingError(f"No se encontró la imagen: {file_path}")
        
        try:
            # Cargar la imagen con OpenCV
            image = cv2.imread(file_path)
            
            if image is None:
                raise ImageProcessingError(f"No se pudo cargar la imagen: {file_path}")
            
            return image
        
        except Exception as e:
            logger.error(f"Error al cargar la imagen: {str(e)}")
            raise ImageProcessingError(f"Error al cargar la imagen: {str(e)}")
    
    def process_image(self, image: np.ndarray, resize: Optional[Tuple[int, int]] = None) -> np.ndarray:
        """
        Procesa una imagen para prepararla para el análisis.
        
        Args:
            image: Imagen como matriz numpy
            resize: Dimensiones a las que redimensionar la imagen (opcional)
            
        Returns:
            np.ndarray: Imagen procesada
            
        Raises:
            ImageProcessingError: Si hay un error al procesar la imagen
        """
        try:
            # Asegurarse de que la imagen tenga el formato correcto
            if image is None or image.size == 0:
                raise ImageProcessingError("Imagen vacía o nula")
            
            # Redimensionar si es necesario
            if resize:
                image = cv2.resize(image, resize)
            
            return image
        
        except Exception as e:
            logger.error(f"Error al procesar la imagen: {str(e)}")
            raise ImageProcessingError(f"Error al procesar la imagen: {str(e)}")
    
    def delete_image(self, file_path: str) -> bool:
        """
        Elimina una imagen del sistema de archivos.
        
        Args:
            file_path: Ruta del archivo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Imagen eliminada: {file_path}")
                return True
            
            logger.warning(f"No se encontró la imagen para eliminar: {file_path}")
            return False
        
        except Exception as e:
            logger.error(f"Error al eliminar la imagen: {str(e)}")
            return False
    
    def get_image_url(self, file_name: str) -> str:
        """
        Obtiene la URL para acceder a una imagen.
        
        Args:
            file_name: Nombre del archivo
            
        Returns:
            str: URL de la imagen
        """
        return f"/uploads/{file_name}" 