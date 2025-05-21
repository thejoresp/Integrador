"""
Excepciones personalizadas para la aplicación de análisis facial.
Estas excepciones permiten un mejor manejo de errores específicos del dominio.
"""

class BaseFacialAnalysisError(Exception):
    """Excepción base para todos los errores de la aplicación de análisis facial."""
    def __init__(self, message: str = "Error en el sistema de análisis facial"):
        self.message = message
        super().__init__(self.message)


class ImageProcessingError(BaseFacialAnalysisError):
    """Excepción para errores en el procesamiento de imágenes."""
    def __init__(self, message: str = "Error al procesar la imagen"):
        super().__init__(message)


class FaceDetectionError(BaseFacialAnalysisError):
    """Excepción para errores en la detección de rostros."""
    def __init__(self, message: str = "Error al detectar rostros en la imagen"):
        super().__init__(message)


class InvalidImageFormatError(BaseFacialAnalysisError):
    """Excepción para formatos de imagen no válidos."""
    def __init__(self, message: str = "Formato de imagen no válido. Use .jpg o .png"):
        super().__init__(message)


class AnalysisError(BaseFacialAnalysisError):
    """Excepción para errores generales en el análisis facial."""
    def __init__(self, message: str = "Error durante el análisis facial"):
        super().__init__(message) 