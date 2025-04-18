"""
Router para endpoints de análisis facial siguiendo el patrón MVC.

Este módulo define las rutas API para el análisis facial, conectando
los controladores con las solicitudes HTTP entrantes.
"""
import os
import uuid
from typing import List

from fastapi import (
    APIRouter, 
    File, 
    UploadFile, 
    HTTPException, 
    Form, 
    Request, 
    BackgroundTasks,
    Depends
)
from fastapi.responses import HTMLResponse

from app.config import UPLOAD_DIR, config, logger
from app.models.dto.api_models import AnalysisRequestDTO, AnalysisResultDTO
from app.services.image_processor import save_upload
from app.dependencies import get_analyzers
from app.controllers.facial_analysis_controller import FacialAnalysisController
from app.views.facial_analysis_view import FacialAnalysisView
from app.utils.image import cleanup_uploaded_file


router = APIRouter(prefix="/api/analysis", tags=["analysis"])

# Inicializar vista
facial_analysis_view = FacialAnalysisView()

@router.post("/face", response_model=AnalysisResultDTO)
async def analyze_face(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    analysis_types: List[str] = Form(["all"]),
    analyzers = Depends(get_analyzers)
):
    """
    Analiza una imagen facial y devuelve los resultados según los tipos de análisis solicitados.
    
    Args:
        background_tasks: Tareas en segundo plano para limpieza de archivos
        image: Imagen facial a analizar
        analysis_types: Tipos de análisis a realizar (all, age_gender, emotion, skin, health, symmetry)
        analyzers: Diccionario con los analizadores faciales inyectados
        
    Returns:
        AnalysisResultDTO: Resultado del análisis facial
        
    Raises:
        HTTPException: Si hay errores en el procesamiento o análisis
    """
    try:
        # Validar la imagen
        if not config.validate_file_extension(image.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"Formato de archivo no permitido. Use: {', '.join(config.allowed_extensions)}"
            )
        
        # Guardar la imagen con nombre único
        image_id = f"{uuid.uuid4()}.{image.filename.rsplit('.', 1)[1].lower()}"
        image_path = os.path.join(UPLOAD_DIR, image_id)
        
        if not await save_upload(image, image_path):
            raise HTTPException(status_code=400, detail="Error al procesar la imagen")
        
        # Crear el controlador
        controller = FacialAnalysisController(analyzers)
        
        # Crear la solicitud
        request = AnalysisRequestDTO(analysis_types=analysis_types)
        
        # Procesar la solicitud a través del controlador (patrón MVC)
        result, error_message = await controller.process_analysis_request(image_path, request)
        
        if error_message:
            raise HTTPException(status_code=400, detail=error_message)
        
        # Programar limpieza del archivo en segundo plano
        background_tasks.add_task(cleanup_uploaded_file, image_path)
        
        return result
    
    except HTTPException:
        # Re-lanzar excepciones HTTP para mantener el status code
        raise
    except Exception as e:
        # Log detallado del error
        logger.error(f"Error en análisis facial: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error en el análisis: {str(e)}"
        )

@router.get("/result/{image_id}", response_class=HTMLResponse)
async def get_analysis_result(request: Request, image_id: str):
    """
    Muestra los resultados del análisis de forma visual.
    
    Args:
        request: Objeto de solicitud HTTP
        image_id: ID de la imagen analizada
        
    Returns:
        Plantilla HTML con los resultados visualizados
        
    Raises:
        HTTPException: Si no se encuentra el análisis
    """
    # Verificar si la imagen existe
    image_path = os.path.join(UPLOAD_DIR, image_id)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Análisis no encontrado")
    
    # Crear controlador (sin analizadores, solo para mock)
    controller = FacialAnalysisController({})
    
    # Obtener resultados (mock por ahora)
    mock_results = controller.generate_mock_result(image_id)
    
    # Renderizar resultados usando la vista (patrón MVC)
    return facial_analysis_view.render_result_page(
        request, 
        mock_results, 
        f"/uploads/{image_id}"
    )
