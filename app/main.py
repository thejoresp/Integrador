"""
Punto de entrada principal de la aplicación de análisis facial.
Configura y crea la aplicación FastAPI con todas sus dependencias y rutas.
"""

import logging
import os
import uuid
from typing import List
from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pathlib import Path

from app.config import get_settings
from app.routes import get_all_routes
from app.core.logger import setup_global_logging, get_logger

# Crear instancia de configuración
settings = get_settings()

# Configurar logging
setup_global_logging(log_file="app.log")
logger = get_logger(__name__)

def create_application() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.
    
    Returns:
        FastAPI: Aplicación configurada
    """
    # Crear aplicación
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.ENABLE_DOCS else None,
        redoc_url="/redoc" if settings.ENABLE_DOCS else None,
    )
    
    # Configurar CORS
    if settings.ENABLE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Guardar configuración en el estado de la aplicación
    app.state.config = settings
    
    # Montar directorios estáticos
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Montar directorio de uploads como estático para acceder a las imágenes
    uploads_dir = Path(app.state.config.UPLOAD_DIR)
    if not uploads_dir.exists():
        uploads_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=app.state.config.UPLOAD_DIR), name="uploads")
    
    # Configurar plantillas
    app.state.templates = Jinja2Templates(directory="templates")
    
    # Registrar rutas
    app.include_router(get_all_routes())
    
    # Ruta de redirección para la raíz
    @app.get("/")
    async def redirect_to_app():
        return RedirectResponse(url="/app")
    
    # Configurar manejadores de eventos
    @app.on_event("startup")
    async def startup_event():
        """Acciones a ejecutar al iniciar la aplicación."""
        logger.info(f"Iniciando aplicación {settings.APP_NAME} v{settings.APP_VERSION}")
        
        # Crear directorios necesarios
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Verificar si existe la carpeta de modelos
        models_dir = Path(settings.MODELS_DIR)
        if not models_dir.exists():
            models_dir.mkdir(parents=True, exist_ok=True)
            logger.warning(f"Se creó el directorio de modelos: {models_dir}")
        
        # Carpeta específica para modelos de piel
        skin_models_dir = Path(settings.SKIN_MODELS_DIR)
        if not skin_models_dir.exists():
            skin_models_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Se creó el directorio para modelos de análisis de piel: {skin_models_dir}")
        
        logger.info("Aplicación iniciada correctamente")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Acciones a ejecutar al detener la aplicación."""
        logger.info("Cerrando la aplicación")
    
    # Verificación de estado
    @app.get("/health")
    async def health_check():
        """Endpoint para verificar el estado de la aplicación."""
        return {"status": "ok", "version": settings.APP_VERSION}
    
    # Personalizar documentación OpenAPI
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title=settings.APP_NAME,
            version=settings.APP_VERSION,
            description=settings.APP_DESCRIPTION,
            routes=app.routes,
        )
        
        # Personalizar esquema OpenAPI
        openapi_schema["info"]["x-logo"] = {
            "url": "/static/img/logo.png"
        }
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi
    
    # Middleware para manejar excepciones
    @app.middleware("http")
    async def log_and_add_process_time_header(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Error no manejado: {str(e)}")
            raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    return app

# Crear la aplicación
app = create_application()