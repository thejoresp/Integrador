"""
Dependencias para la aplicación de análisis facial.
Proporciona funciones para inyección de dependencias en los endpoints.
"""

import logging
from fastapi import Depends

from app.config import get_settings, Config
from app.controllers.facial_analysis_controller import FacialAnalysisController
from app.repositories.image_repository import ImageRepository
from app.repositories.model_repository import ModelRepository
from app.services.facial_analysis_service import FacialAnalysisService
from app.views.facial_analysis_view import FacialAnalysisView

logger = logging.getLogger(__name__)


def get_image_repository(config: Config = Depends(get_settings)) -> ImageRepository:
    """Proporciona un repositorio de imágenes."""
    return ImageRepository(upload_dir=config.UPLOAD_FOLDER)


def get_model_repository() -> ModelRepository:
    """Proporciona un repositorio de modelos de ML."""
    return ModelRepository()


def get_facial_analysis_service(
    model_repository: ModelRepository = Depends(get_model_repository)
) -> FacialAnalysisService:
    """Proporciona un servicio de análisis facial."""
    return FacialAnalysisService(model_repository=model_repository)


def get_facial_analysis_view() -> FacialAnalysisView:
    """Proporciona una vista para formatear resultados de análisis facial."""
    return FacialAnalysisView()


def get_facial_analysis_controller(
    image_repository: ImageRepository = Depends(get_image_repository),
    facial_analysis_service: FacialAnalysisService = Depends(get_facial_analysis_service),
    facial_analysis_view: FacialAnalysisView = Depends(get_facial_analysis_view)
) -> FacialAnalysisController:
    """Proporciona un controlador para el análisis facial."""
    return FacialAnalysisController(
        image_repository=image_repository,
        facial_analysis_service=facial_analysis_service,
        facial_analysis_view=facial_analysis_view
    )
