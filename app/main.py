import os
import uuid
from typing import List
from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import STATIC_DIR, TEMPLATE_DIR, UPLOAD_DIR, ensure_upload_dir
from app.routers import analysis
from app.aws.s3 import upload_file, get_file_url
from app.analyzers.skin import SkinAnalyzer
from app.analyzers.emotion import EmotionAnalyzer
from app.analyzers.age_gender import AgeGenderAnalyzer
from app.analyzers.health import HealthAnalyzer
from app.schemas.response import FaceAnalysisResponse
from app.utils.image import validate_image, process_image

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

# Configurar plantillas
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# Inicializar analizadores
skin_analyzer = SkinAnalyzer()
emotion_analyzer = EmotionAnalyzer()
age_gender_analyzer = AgeGenderAnalyzer()
health_analyzer = HealthAnalyzer()

@app.on_event("startup")
async def startup():
    ensure_upload_dir()

# Registrar routers
app.include_router(analysis.router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "El servicio está funcionando correctamente"}

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
    
    # Subir a S3
    s3_key = f"uploads/{file_name}"
    upload_file(file_path, s3_key)
    image_url = get_file_url(s3_key)
    
    # Realizar análisis
    try:
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
        raise HTTPException(status_code=500, detail=f"Error en el análisis: {str(e)}")
    finally:
        # Limpiar archivo temporal
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)