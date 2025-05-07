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
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.config import get_settings, STATIC_DIR, TEMPLATE_DIR, UPLOAD_DIR, ensure_upload_dir
from app.routers import analysis_router
from app.analyzers.skin import SkinAnalyzer
from app.analyzers.emotion import EmotionAnalyzer
from app.analyzers.age_gender import AgeGenderAnalyzer
from app.analyzers.health import HealthAnalyzer
from app.schemas.response import FaceAnalysisResponse
from app.utils.image import validate_image, process_image
from app.exceptions.base import BaseFacialAnalysisError

# Configurar logging
logger = logging.getLogger(__name__)

# Obtener configuración
config = get_settings()

def create_application() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.
    
    Returns:
        FastAPI: Aplicación configurada
    """
    # Crear aplicación
    app = FastAPI(
        title=config.APP_NAME,
        description=config.APP_DESCRIPTION,
        version=config.APP_VERSION,
        docs_url="/docs" if not config.is_production else None,
        redoc_url="/redoc" if not config.is_production else None,
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Guardar configuración en el estado de la aplicación
    app.state.config = config
    
    # Configurar plantillas
    templates = Jinja2Templates(directory=TEMPLATE_DIR)
    app.state.templates = templates
    
    # Montar archivos estáticos
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
    
    # Registrar rutas
    app.include_router(analysis_router.router)
    
    # Configurar manejadores de eventos
    @app.on_event("startup")
    async def startup_event():
        """Acciones a ejecutar al iniciar la aplicación."""
        logger.info("Iniciando aplicación de análisis facial...")
        ensure_upload_dir()
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Acciones a ejecutar al detener la aplicación."""
        logger.info("Deteniendo aplicación de análisis facial...")
    
    # Configurar manejo de excepciones
    @app.exception_handler(BaseFacialAnalysisError)
    async def facial_analysis_exception_handler(request: Request, exc: BaseFacialAnalysisError):
        """Manejador para excepciones del dominio de análisis facial."""
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "detail": str(exc)
        }
    
    # Ruta principal
    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Página de inicio de la aplicación."""
        return templates.TemplateResponse("index.html", {"request": request})
    
    # Verificación de estado
    @app.get("/health")
    async def health_check():
        """Endpoint para verificar el estado de la aplicación."""
        return {"status": "ok", "version": config.APP_VERSION}
    
    # Personalizar documentación OpenAPI
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title=config.APP_NAME,
            version=config.APP_VERSION,
            description=config.APP_DESCRIPTION,
            routes=app.routes,
        )
        
        # Personalizar esquema OpenAPI
        openapi_schema["info"]["x-logo"] = {
            "url": "/static/img/logo.png"
        }
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi
    
    return app

# Crear la aplicación
app = create_application()

@app.post("/analyze", response_model=FaceAnalysisResponse)
async def analyze_face(file: UploadFile = File(...)):
    """
    Analiza una imagen facial y devuelve un análisis completo
    """
    # Validar la imagen
    if not validate_image(file):
        raise HTTPException(status_code=400, detail="Formato de imagen no válido. Use .jpg o .png")
    
    # Generar un nombre de archivo único
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{file_id}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    # Guardar la imagen localmente
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Procesar la imagen
    try:
        image = process_image(file_path)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Error procesando la imagen: {str(e)}")
    
    # Generar URL local
    image_url = f"/uploads/{file_name}"
    
    # Realizar análisis
    try:
        skin_analyzer = SkinAnalyzer()
        emotion_analyzer = EmotionAnalyzer()
        age_gender_analyzer = AgeGenderAnalyzer()
        health_analyzer = HealthAnalyzer()
        
        skin_results = skin_analyzer.analyze(image)
        emotion_results = emotion_analyzer.analyze(image)
        age_gender_results = age_gender_analyzer.analyze(image)
        health_results = health_analyzer.analyze(image)
        
        # Construir respuesta
        response = FaceAnalysisResponse(
            image_url=image_url,
            skin=skin_results,
            emotion=emotion_results,
            age_gender=age_gender_results,
            health=health_results
        )
        
        return response
    
    except Exception as e:
        # En caso de error, no eliminar la imagen para debugging
        raise HTTPException(status_code=500, detail=f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Configuración para desarrollo local
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",  # Solo accesible localmente
        port=8000,
        reload=True,
        log_level="info"
    )