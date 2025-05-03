"""
Paquete de repositorios para la aplicación de análisis facial.
"""

from app.repositories.image_repository import ImageRepository
from app.repositories.model_repository import ModelRepository

__all__ = ["ImageRepository", "ModelRepository"] 