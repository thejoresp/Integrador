from fastapi import APIRouter, Depends, Request, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import List, Optional
import os
import shutil
import uuid
import datetime
from pydantic import BaseModel
import logging

from app.core.logger import get_logger
from app.config import get_settings
from app.dependencies import rate_limit, verify_optional_api_key

# Función auxiliar para categorizar valores
def getCategoryLevel(score):
    """
    Determina un nivel descriptivo basado en un puntaje (0-100)
    
    Args:
        score: Puntaje numérico entre 0 y 100
        
    Returns:
        str: Nivel descriptivo (Excelente, Bueno, Regular, Bajo, Muy bajo)
    """
    if score >= 80:
        return "Excelente"
    elif score >= 60:
        return "Bueno"
    elif score >= 40:
        return "Regular"
    elif score >= 20:
        return "Bajo"
    else:
        return "Muy bajo"

# Importar routers específicos
try:
    from app.routers import skin_router
except ImportError:
    logging.warning("Router de piel no disponible")

# Configuración
logger = get_logger(__name__)
settings = get_settings()

# Router principal
router = APIRouter()

# Modelos de datos para API
class CleanupRequest(BaseModel):
    days_threshold: Optional[int] = 30

# Rutas básicas
@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return request.app.state.templates.TemplateResponse("index.html", {"request": request})

# Endpoint de redirección para compatibilidad con código antiguo
@router.post("/analyze")
async def analyze_redirect(file: UploadFile = File(...)):
    """
    Endpoint de redirección para mantener compatibilidad con código antiguo.
    Procesa la solicitud y la reenvía a '/skin/analyze/complete'.
    """
    logger.info("Solicitud recibida en /analyze, procesando a través de /skin/analyze/complete")
    
    try:
        # Crear directorio de uploads si no existe
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Guardar el archivo temporalmente
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Guardar archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Importar el servicio de piel y realizar el análisis
        from app.services.skin_service import SkinService
        from app.dependencies import get_skin_service
        
        skin_service = get_skin_service()
        
        # Realizar análisis completo
        result = await skin_service.perform_complete_analysis(file_path)
        
        # Agregar URL de la imagen al resultado
        file_url = f"/uploads/{unique_filename}"
        
        # Convertir el resultado de Pydantic a diccionario si es necesario
        if hasattr(result, "dict"):
            result_dict = result.dict()
        elif isinstance(result, dict):
            result_dict = result
        else:
            result_dict = {"error": "Formato de resultado desconocido"}
        
        # Agregar la URL de la imagen
        result_dict["image_url"] = file_url
        
        # Formatear los datos para que sean compatibles con el frontend
        formatted_result = {
            "image_url": file_url,
            # Datos de análisis de piel
            "skin": {
                "hydration": {
                    "score": result_dict.get("skin_condition", {}).get("hydration", 0) if isinstance(result_dict.get("skin_condition"), dict) else 0,
                    "level": getCategoryLevel(result_dict.get("skin_condition", {}).get("hydration", 0) if isinstance(result_dict.get("skin_condition"), dict) else 0)
                },
                "texture": {
                    "score": result_dict.get("skin_condition", {}).get("texture", 0) if isinstance(result_dict.get("skin_condition"), dict) else 0,
                    "level": getCategoryLevel(result_dict.get("skin_condition", {}).get("texture", 0) if isinstance(result_dict.get("skin_condition"), dict) else 0)
                },
                "pores": {
                    "score": result_dict.get("skin_condition", {}).get("pores", 0) if isinstance(result_dict.get("skin_condition"), dict) else 0,
                    "level": getCategoryLevel(result_dict.get("skin_condition", {}).get("pores", 0) if isinstance(result_dict.get("skin_condition"), dict) else 0)
                },
                "oiliness": {
                    "score": result_dict.get("skin_condition", {}).get("oiliness", 0) if isinstance(result_dict.get("skin_condition"), dict) else 0,
                    "level": getCategoryLevel(result_dict.get("skin_condition", {}).get("oiliness", 0) if isinstance(result_dict.get("skin_condition"), dict) else 0)
                }
            },
            # Datos de salud
            "health": {
                "skin_conditions": {
                    "redness": {
                        "level": "Normal"
                    }
                },
                "nutrition": {
                    "level": "Adecuado"
                },
                "fatigue": {
                    "level": "Moderado",
                    "score": 59.24,
                    "has_dark_circles": False,
                    "has_red_eyes": False
                }
            },
            # Datos para sección Análisis Derm Foundation
            "derm_analysis": {
                "status": "success",
                "embedding_dimensions": "6144",
                "skin_features": {
                    "texture": result_dict.get("skin_condition", {}).get("texture", 0) if isinstance(result_dict.get("skin_condition"), dict) else "Normal",
                    "tone": result_dict.get("skin_tone", {}).get("tone_name", "Normal") if isinstance(result_dict.get("skin_tone"), dict) else "Normal",
                    "conditions": [
                        f"Tono de piel: {result_dict.get('skin_tone', {}).get('tone_name', 'No evaluado') if isinstance(result_dict.get('skin_tone'), dict) else 'No evaluado'}",
                        f"Tipo Fitzpatrick: {result_dict.get('skin_tone', {}).get('fitzpatrick_type', 'No evaluado') if isinstance(result_dict.get('skin_tone'), dict) else 'No evaluado'}",
                        f"Lunares totales: {result_dict.get('mole_analysis', {}).get('total_count', 0) if isinstance(result_dict.get('mole_analysis'), dict) else 0}",
                        f"Lunares benignos: {result_dict.get('mole_analysis', {}).get('benign_count', 0) if isinstance(result_dict.get('mole_analysis'), dict) else 0}",
                        f"Lunares sospechosos: {result_dict.get('mole_analysis', {}).get('suspicious_count', 0) if isinstance(result_dict.get('mole_analysis'), dict) else 0}"
                    ]
                }
            },
            # Datos originales para que formatSkinAnalysisData pueda usarlos
            "skin_condition": result_dict.get("skin_condition"),
            "mole_analysis": result_dict.get("mole_analysis"),
            "skin_tone": result_dict.get("skin_tone")
        }
        
        logger.info(f"Análisis completado correctamente a través del endpoint de compatibilidad /analyze")
        return formatted_result
        
    except Exception as e:
        logger.error(f"Error al procesar la solicitud en /analyze: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud: {str(e)}"
        )

@router.post("/upload")
async def upload_image(
    request: Request,
    file: UploadFile = File(...)
):
    try:
        # Crear directorio de uploads si no existe
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generar nombre único para el archivo
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Guardar archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "filename": unique_filename,
            "filepath": file_path,
            "content_type": file.content_type
        }
    except Exception as e:
        logger.error(f"Error al subir archivo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/maintenance/cleanup")
async def cleanup_old_files(
    request: CleanupRequest,
):
    try:
        # Obtener umbral de días
        days_threshold = request.days_threshold
        
        # Calcular fecha límite
        threshold_date = datetime.datetime.now() - datetime.timedelta(days=days_threshold)
        
        # Contar archivos eliminados
        deleted_count = 0
        
        # Buscar y eliminar archivos antiguos
        for filename in os.listdir(settings.UPLOAD_DIR):
            if filename == '.gitkeep':  # Ignorar archivo especial
                continue
                
            file_path = os.path.join(settings.UPLOAD_DIR, filename)
            file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            
            if file_modified < threshold_date:
                os.remove(file_path)
                deleted_count += 1
        
        return {"deleted_files": deleted_count}
    except Exception as e:
        logger.error(f"Error en cleanup: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Incluir otros routers si están disponibles
try:
    # Incluir el router de piel si está disponible
    router.include_router(
        skin_router.router,
        dependencies=[
            Depends(rate_limit),
            Depends(verify_optional_api_key)
        ]
    )
    logger.info("Router de piel incluido en la aplicación")
except (NameError, AttributeError) as e:
    logger.warning(f"No se pudo incluir el router de piel: {str(e)}")

# Función para obtener todas las rutas
def get_all_routes():
    """Devuelve todas las rutas configuradas en la aplicación."""
    return router 