"""
Punto de entrada principal de la aplicación de análisis facial.

Este módulo configura la aplicación FastAPI e implementa el patrón MVC
(Modelo-Vista-Controlador) para la estructura general del proyecto.
"""
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import (
    STATIC_DIR, 
    TEMPLATE_DIR, 
    UPLOAD_DIR,
    config, 
    ensure_dirs,
    logger
)
from app.routers import analysis
from app.dependencies import get_analyzers
from app.views.facial_analysis_view import FacialAnalysisView

# Crear la aplicación FastAPI
app = FastAPI(
    title="FaceAnalyzer API",
    description="API para análisis de rostros usando deep learning y visión por computadora",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Inicializar vista
facial_analysis_view = FacialAnalysisView()

@app.on_event("startup")
async def startup_event():
    """
    Función ejecutada al iniciar la aplicación.
    Prepara directorios y recursos necesarios.
    """
    # Asegurar que existan los directorios necesarios
    ensure_dirs()
    
    # Log de modo de la aplicación
    if config.is_production:
        logger.info("Ejecutando en modo PRODUCCIÓN")
    else:
        logger.info("Ejecutando en modo DESARROLLO")

# Registrar routers
app.include_router(analysis.router)

@app.get("/")
async def index(request: Request):
    """
    Ruta principal que muestra la interfaz de usuario.
    
    Args:
        request: Objeto de solicitud HTTP
        
    Returns:
        Plantilla HTML renderizada usando la vista (patrón MVC)
    """
    return facial_analysis_view.render_index_page(request)

@app.get("/health")
async def health_check():
    """
    Endpoint para verificar la salud del servicio.
    
    Returns:
        Dict: Estado y mensaje del servicio
    """
    return {
        "status": "ok", 
        "message": "El servicio está funcionando correctamente",
        "environment": config.env_mode
    }

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Manejador global de excepciones para capturar errores no controlados.
    
    Args:
        request: Objeto Request de FastAPI
        exc: Excepción capturada
        
    Returns:
        HTTPException con mensaje apropiado
    """
    logger.error(f"Error no controlado: {str(exc)}", exc_info=True)
    return HTTPException(
        status_code=500,
        detail="Error interno del servidor. Por favor, inténtelo más tarde."
    )

if __name__ == "__main__":
    """Punto de entrada para ejecución directa"""
    uvicorn.run(
        "app.main:app", 
        host=config.host, 
        port=config.port,
        reload=not config.is_production,
        workers=config.workers
    )