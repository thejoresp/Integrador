import logging
from fastapi import UploadFile, HTTPException

from app.schemas.response import FaceAnalysisResponse
from app.services.image_service import ImageService
from app.services.face_analyzer import FaceAnalyzerService

# Configurar logging
logger = logging.getLogger(__name__)

class FacialAnalysisController:
    """
    Controlador para el análisis facial.
    Maneja la coordinación entre servicios para el análisis facial.
    """
    
    def __init__(self):
        """Inicializa el controlador con los servicios necesarios"""
        self.image_service = ImageService()
        self.face_analyzer_service = FaceAnalyzerService()
    
    async def analyze_image(self, file: UploadFile) -> FaceAnalysisResponse:
        """
        Analiza una imagen facial y retorna los resultados del análisis.
        
        Args:
            file: Imagen facial a analizar
            
        Returns:
            Objeto FaceAnalysisResponse con los resultados del análisis
            
        Raises:
            HTTPException: Si hay un error durante el procesamiento o análisis
        """
        file_path = None
        
        try:
            # Procesar imagen usando el servicio de imágenes
            file_path, processed_image, _, image_url = await self.image_service.save_and_process_image(file)
            
            # Realizar análisis usando el servicio de análisis facial
            analysis_results = self.face_analyzer_service.analyze_all(processed_image)
            
            # Construir respuesta
            response = FaceAnalysisResponse(
                image_url=image_url,
                skin=analysis_results["skin"],
                emotion=analysis_results["emotion"],
                age_gender=analysis_results["age_gender"],
                health=analysis_results["health"]
            )
            
            return response
        
        except HTTPException:
            # Re-lanzar excepciones HTTP para mantener el código de estado
            raise
        except Exception as e:
            logger.error(f"Error en el análisis facial: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error en el análisis: {str(e)}")
        finally:
            # Limpiar archivo temporal usando el servicio
            if file_path:
                self.image_service.cleanup_temp_file(file_path)