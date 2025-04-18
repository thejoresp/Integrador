"""
Enrutador para las vistas web.
Define las rutas para la interfaz de usuario.
"""

import logging
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import TEMPLATE_DIR
from app.controllers.facial_analysis_controller import FacialAnalysisController

logger = logging.getLogger(__name__)

# Crear el enrutador
router = APIRouter(tags=["web"])

# Configurar plantillas
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# Dependencia para obtener el controlador
def get_facial_analysis_controller():
    return FacialAnalysisController()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Página principal de la aplicación
    
    Args:
        request: Objeto Request de FastAPI
        
    Returns:
        Plantilla HTML renderizada
    """
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/analyze-web", response_class=HTMLResponse)
async def analyze_web(
    request: Request,
    file: UploadFile = File(...),
    controller: FacialAnalysisController = Depends(get_facial_analysis_controller)
):
    """
    Analiza una imagen y muestra los resultados en una página web
    
    Args:
        request: Objeto Request de FastAPI
        file: Imagen a analizar
        controller: Controlador para el análisis facial (inyectado)
        
    Returns:
        Página web con los resultados del análisis
    """
    try:
        # Realizar análisis
        results = await controller.analyze_image(file)
        
        # Renderizar plantilla con resultados
        return templates.TemplateResponse(
            "result.html", 
            {
                "request": request,
                "results": results
            }
        )
    except HTTPException as e:
        # Mostrar error en la interfaz
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_code": e.status_code,
                "error_message": e.detail
            }
        )
    except Exception as e:
        logger.error(f"Error no controlado en la interfaz web: {str(e)}", exc_info=True)
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_code": 500,
                "error_message": f"Error en el servidor: {str(e)}"
            }
        )