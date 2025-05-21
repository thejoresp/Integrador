"""
Paquete de excepciones para la aplicación de análisis facial.
"""

from app.exceptions.base import (
    BaseFacialAnalysisError,
    ImageProcessingError,
    FaceDetectionError,
    InvalidImageFormatError,
    AnalysisError
)

__all__ = [
    "BaseFacialAnalysisError",
    "ImageProcessingError",
    "FaceDetectionError",
    "InvalidImageFormatError",
    "AnalysisError"
] 