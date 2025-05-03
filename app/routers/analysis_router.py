"""
Router para los endpoints de análisis facial.
Define las rutas y endpoints para operaciones de análisis facial.
"""

import logging
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status

from app.controllers.facial_analysis_controller import FacialAnalysisController
from app.schemas.facial_analysis import FacialAnalysisResponseSchema
from app.dependencies import get_facial_analysis_controller

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/analysis",
    tags=["analysis"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
    }
)


@router.post("/analyze", response_model=FacialAnalysisResponseSchema)
async def analyze_facial_image(
    file: UploadFile = File(...),
    controller: FacialAnalysisController = Depends(get_facial_analysis_controller)
):
    """
    Analiza una imagen facial y devuelve un análisis completo.
    
    - **file**: Imagen facial para analizar (.jpg o .png)
    
    Devuelve:
      Un análisis detallado con información sobre:
      - Cajas delimitadoras de rostros detectados
      - Puntos característicos faciales (landmarks)
      - Edad y género estimados
      - Emociones detectadas
      - Análisis de la piel
      - Indicadores de salud basados en la apariencia facial
    """
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionó ningún archivo"
        )
    
    # Validar tipo de contenido
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de contenido no soportado: {content_type}. Utilice JPEG o PNG."
        )
    
    # Delegar el análisis al controlador
    return await controller.analyze_image(file) 