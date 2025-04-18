import os
import logging
from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import STATIC_DIR, TEMPLATE_DIR, UPLOAD_DIR, ensure_upload_dir
from app.routers import analysis, api, web
from app.controllers.facial_analysis_controller import FacialAnalysisController
from app.schemas.response import FaceAnalysisResponse

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Configurar plantillas
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# Inicializar controladores
facial_analysis_controller = FacialAnalysisController()

@app.on_event("startup")
async def startup():
    ensure_upload_dir()
    logger.info("Aplicación iniciada correctamente")

# Registrar routers
app.include_router(web.router)
app.include_router(api.router)
app.include_router(analysis.router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Vista principal de la aplicación"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la aplicación"""
    return {"status": "ok", "message": "El servicio está funcionando correctamente"}

# Mantener el endpoint /analyze para compatibilidad con versiones anteriores
@app.post("/analyze", response_model=FaceAnalysisResponse)
async def analyze_face(
    file: UploadFile = File(...),
    controller: FacialAnalysisController = Depends(web.get_facial_analysis_controller)
):
    """
    Analiza una imagen facial y devuelve un análisis completo
    
    Esta ruta se mantiene para compatibilidad con versiones anteriores.
    Se recomienda usar /api/analyze en su lugar.
    """
    try:
        # Delegar procesamiento al controlador
        return await controller.analyze_image(file)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error no controlado en la API: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)