"""
Servicio para el manejo de imágenes.
Proporciona funcionalidades para procesar, guardar y gestionar imágenes.
"""

import os
import uuid
import logging
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException
import numpy as np

from app.config import UPLOAD_DIR
from app.utils.image import validate_image, process_image

logger = logging.getLogger(__name__)

class ImageService:
    """Servicio para gestionar operaciones relacionadas con imágenes"""
    
    @staticmethod
    async def save_and_process_image(file: UploadFile) -> Tuple[str, np.ndarray, str, str]:
        """
        Guarda una imagen subida y la procesa.
        
        Args:
            file: Archivo de imagen subido
            
        Returns:
            Tuple con:
                - Ruta local del archivo
                - Imagen procesada como numpy array
                - Nombre del archivo 
                - URL de la imagen
                
        Raises:
            HTTPException: Si hay error en la validación o procesamiento
        """
        # Validar la imagen
        if not validate_image(file):
            raise HTTPException(status_code=400, detail="Formato de imagen no válido. Use .jpg o .png")
        
        # Generar un nombre de archivo único
        file_id = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1]
        file_name = f"{file_id}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        # Guardar la imagen localmente
        try:
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
        except Exception as e:
            logger.error(f"Error al guardar la imagen: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")
            
        # Procesar la imagen
        try:
            processed_image = process_image(file_path)
        except Exception as e:
            # Limpiar el archivo en caso de error
            if os.path.exists(file_path):
                os.remove(file_path)
            logger.error(f"Error al procesar la imagen: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error procesando la imagen: {str(e)}")
        
        # Generar URL local para la imagen
        image_url = f"/uploads/{file_name}"
        
        return file_path, processed_image, file_name, image_url
    
    @staticmethod
    def cleanup_temp_file(file_path: str) -> None:
        """
        Limpia un archivo temporal si existe
        
        Args:
            file_path: Ruta del archivo a eliminar
        """
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.debug(f"Archivo temporal eliminado: {file_path}")
            except Exception as e:
                logger.error(f"Error al eliminar archivo temporal {file_path}: {str(e)}")