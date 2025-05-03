"""
Controlador para el análisis facial.
Gestiona las peticiones de análisis facial y coordina las respuestas.
"""

import logging
from fastapi import UploadFile, Depends, HTTPException, status
from typing import Dict, Any

from app.exceptions.base import BaseFacialAnalysisError
from app.repositories.image_repository import ImageRepository
from app.services.facial_analysis_service import FacialAnalysisService
from app.schemas.facial_analysis import FacialAnalysisResponseSchema
from app.views.facial_analysis_view import FacialAnalysisView

logger = logging.getLogger(__name__)


class FacialAnalysisController:
    """
    Controlador para gestionar las peticiones de análisis facial.
    
    Este controlador se encarga de recibir las solicitudes, coordinar la ejecución
    de los servicios necesarios y formatear las respuestas.
    """
    
    def __init__(
        self,
        image_repository: ImageRepository,
        facial_analysis_service: FacialAnalysisService,
        facial_analysis_view: FacialAnalysisView
    ):
        """
        Inicializa el controlador con los servicios necesarios.
        
        Args:
            image_repository: Repositorio para gestionar imágenes
            facial_analysis_service: Servicio para análisis facial
            facial_analysis_view: Vista para formatear respuestas
        """
        self.image_repository = image_repository
        self.facial_analysis_service = facial_analysis_service
        self.view = facial_analysis_view
    
    async def analyze_image(self, file: UploadFile) -> FacialAnalysisResponseSchema:
        """
        Procesa una solicitud de análisis facial.
        
        Args:
            file: Archivo de imagen subido
            
        Returns:
            FacialAnalysisResponseSchema: Resultado del análisis facial
            
        Raises:
            HTTPException: Si hay un error en el procesamiento
        """
        try:
            # 1. Guardar la imagen
            file_path, file_name = await self.image_repository.save_image(file)
            
            # 2. Cargar la imagen para análisis
            image = self.image_repository.load_image(file_path)
            
            # 3. Procesar la imagen
            processed_image = self.image_repository.process_image(image)
            
            # 4. Obtener URL de la imagen
            image_url = self.image_repository.get_image_url(file_name)
            
            # 5. Realizar análisis facial
            analysis_result = self.facial_analysis_service.analyze_image(
                image=processed_image,
                image_url=image_url
            )
            
            # 6. Formatear respuesta
            response = self.view.format_analysis_result(analysis_result)
            
            return response
            
        except BaseFacialAnalysisError as e:
            logger.error(f"Error en análisis facial: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno al procesar la imagen"
            )