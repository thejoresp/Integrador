"""
Enrutador para las API REST.
Define los endpoints para operaciones de análisis facial.
"""

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.controllers.facial_analysis_controller import FacialAnalysisController
from app.schemas.response import FaceAnalysisResponse

logger = logging.getLogger(__name__)

# Crear el enrutador
router = APIRouter(prefix="/api", tags=["api"])

# Dependencia para obtener el controlador
def get_facial_analysis_controller():
    return FacialAnalysisController()

@router.post("/analyze", response_model=FaceAnalysisResponse)
async def analyze_face(
    file: UploadFile = File(...),
    controller: FacialAnalysisController = Depends(get_facial_analysis_controller)
):
    """
    Analiza una imagen facial y devuelve los resultados del análisis.
    
    Args:
        file: Imagen a analizar
        controller: Controlador para el análisis facial (inyectado)
        
    Returns:
        Resultados del análisis facial
    """
    try:
        return await controller.analyze_image(file)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error no controlado en API: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")