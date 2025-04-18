import os
import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Request, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import UPLOAD_DIR, TEMPLATE_DIR, ALLOWED_EXTENSIONS
from app.services.face_detector import detect_faces
from app.services.image_processor import validate_image, save_upload
from app.services.analyzers.age_gender import analyze_age_gender
from app.services.analyzers.emotion import analyze_emotion
from app.services.analyzers.skin import analyze_skin
from app.services.analyzers.health import analyze_health_indicators
from app.services.analyzers.symmetry import analyze_symmetry
from app.models.schemas import AnalysisResult, AnalysisRequest

router = APIRouter(prefix="/api/analysis", tags=["analysis"])
templates = Jinja2Templates(directory=TEMPLATE_DIR)

@router.post("/face", response_model=AnalysisResult)
async def analyze_face(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    analysis_types: List[str] = Form(["all"]),
):
    """
    Analiza una imagen facial y devuelve los resultados según los tipos de análisis solicitados.
    """
    # Validar la imagen
    if not image.filename or "." not in image.filename:
        raise HTTPException(status_code=400, detail="Archivo inválido")
    
    ext = image.filename.rsplit(".", 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Formato de archivo no permitido. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Guardar la imagen y validar
    image_id = f"{uuid.uuid4()}.{ext}"
    image_path = os.path.join(UPLOAD_DIR, image_id)
    
    if not await save_upload(image, image_path):
        raise HTTPException(status_code=400, detail="Error al procesar la imagen")
    
    # Validar que contiene un rostro
    if not await validate_image(image_path):
        os.remove(image_path)  # Eliminar la imagen inválida
        raise HTTPException(status_code=400, detail="No se detectó un rostro válido en la imagen")
    
    # Detectar rostros
    faces = await detect_faces(image_path)
    if not faces:
        os.remove(image_path)
        raise HTTPException(status_code=400, detail="No se pudo analizar el rostro correctamente")
    
    # Preparar resultados
    results = {
        "image_id": image_id,
        "timestamp": datetime.now().isoformat(),
        "face_count": len(faces),
        "analyses": {}
    }
    
    # Realizar análisis solicitados
    if "all" in analysis_types or "age_gender" in analysis_types:
        results["analyses"]["age_gender"] = await analyze_age_gender(image_path, faces[0])
    
    if "all" in analysis_types or "emotion" in analysis_types:
        results["analyses"]["emotion"] = await analyze_emotion(image_path, faces[0])
    
    if "all" in analysis_types or "skin" in analysis_types:
        results["analyses"]["skin"] = await analyze_skin(image_path, faces[0])
    
    if "all" in analysis_types or "health" in analysis_types:
        results["analyses"]["health"] = await analyze_health_indicators(image_path, faces[0])
    
    if "all" in analysis_types or "symmetry" in analysis_types:
        results["analyses"]["symmetry"] = await analyze_symmetry(image_path, faces[0])
    
    # Programar limpieza del archivo en segundo plano
    background_tasks.add_task(cleanup_uploaded_file, image_path)
    
    return results

@router.get("/result/{image_id}", response_class=HTMLResponse)
async def get_analysis_result(request: Request, image_id: str):
    """
    Muestra los resultados del análisis de forma visual
    """
    # Aquí normalmente recuperarías los resultados de una base de datos
    # Para el ejemplo, simulamos resultados
    
    # Verificar si la imagen existe
    image_path = os.path.join(UPLOAD_DIR, image_id)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Análisis no encontrado")
    
    # En una implementación real, recuperarías los resultados de una base de datos
    mock_results = {
        "image_id": image_id,
        "timestamp": datetime.now().isoformat(),
        "face_count": 1,
        "analyses": {
            "age_gender": {"age": 28, "gender": "Masculino", "confidence": 0.92},
            "emotion": {"dominant": "Neutral", "emotions": {"neutral": 0.7, "happy": 0.2, "sad": 0.05, "angry": 0.05}},
            "skin": {"hydration": "Buena", "texture": "Normal", "pores": "Moderados"},
            "health": {"stress_level": "Bajo", "fatigue": "Mínima", "eye_fatigue": "No detectada"},
            "symmetry": {"score": 0.85, "analysis": "Rostro con buena simetría"}
        }
    }
    
    return templates.TemplateResponse(
        "result.html", 
        {"request": request, "results": mock_results, "image_url": f"/uploads/{image_id}"}
    )

async def cleanup_uploaded_file(file_path: str):
    """Elimina un archivo después de procesarlo"""
    if os.path.exists(file_path):
        os.remove(file_path)
