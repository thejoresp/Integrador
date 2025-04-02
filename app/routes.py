from fastapi import APIRouter, Request, File, UploadFile, Form, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List, Dict, Any
import os
from werkzeug.utils import secure_filename
import uuid
from PIL import Image
import io
import datetime
import json
from pydantic import BaseModel

router = APIRouter()

def get_settings(request: Request):
    return request.app.state.config

def get_s3_client(request: Request):
    return request.app.state.s3

def allowed_file(filename: str, allowed_extensions: set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

class ImageProcessRequest(BaseModel):
    images: List[str]
    height: float
    session_id: Optional[str] = None

class CleanupRequest(BaseModel):
    auth_token: str
    days_threshold: Optional[int] = 30

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return request.app.state.templates.TemplateResponse("index.html", {"request": request})

@router.post("/upload")
async def upload_image(
    request: Request,
    image: UploadFile = File(...),
    session_id: Optional[str] = Form(None),
    s3_client = Depends(get_s3_client),
    config = Depends(get_settings)
):
    if not image:
        raise HTTPException(status_code=400, detail="No se encontró archivo de imagen")
    
    if image.filename == "":
        raise HTTPException(status_code=400, detail="No se seleccionó archivo")

    if not allowed_file(image.filename, config.ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido")

    # Generar nombre único para el archivo
    original_filename = secure_filename(image.filename)
    ext = original_filename.rsplit('.', 1)[1].lower()
    if not session_id:
        session_id = str(uuid.uuid4())
    filename = f"{session_id}_{uuid.uuid4().hex[:8]}.{ext}"
    
    # Guardar temporalmente
    temp_path = os.path.join(config.TEMP_DIR, filename)
    
    # Escribir el archivo en el sistema de archivos
    content = await image.read()
    with open(temp_path, "wb") as temp_file:
        temp_file.write(content)

    try:
        # Optimizar la imagen antes de subir
        img = Image.open(temp_path)
        
        # Conservar resolución pero optimizar calidad si es JPEG
        if ext in ['jpg', 'jpeg']:
            # Guardar con compresión optimizada
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=config.IMG_COMPRESSION_QUALITY, optimize=True)
            output.seek(0)
            optimized_temp_path = temp_path + '_optimized'
            with open(optimized_temp_path, 'wb') as f:
                f.write(output.read())
            
            # Subir la versión optimizada
            s3_client.upload_file(
                optimized_temp_path,
                config.S3_BUCKET,
                f"uploads/{session_id}/{filename}",
                ExtraArgs={'ContentType': f'image/{ext}', 'Metadata': {'upload-date': datetime.datetime.now().isoformat()}}
            )
            # Limpiar archivos temporales
            os.remove(optimized_temp_path)
        else:
            # Para otros formatos, subir directamente
            s3_client.upload_file(
                temp_path,
                config.S3_BUCKET,
                f"uploads/{session_id}/{filename}",
                ExtraArgs={'ContentType': f'image/{ext}', 'Metadata': {'upload-date': datetime.datetime.now().isoformat()}}
            )

        # Limpiar archivo temporal original
        os.remove(temp_path)

        return {
            'success': True,
            'filename': filename,
            'session_id': session_id,
            'url': f"https://{config.S3_BUCKET}.s3.amazonaws.com/uploads/{session_id}/{filename}"
        }

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/maintenance/cleanup")
async def cleanup_old_files(
    request: CleanupRequest,
    config = Depends(get_settings)
):
    # Verificar contraseña o token de autorización
    if request.auth_token != config.MAINTENANCE_TOKEN:
        raise HTTPException(status_code=403, detail="No autorizado")
        
    try:
        # Listar objetos en el bucket con más de X días
        days_threshold = request.days_threshold
        threshold_date = datetime.datetime.now() - datetime.timedelta(days=days_threshold)
        
        # Solo se implementaría la lógica real en producción
        # Este es un placeholder para la implementación
        return {
            'success': True,
            'message': f'Limpieza programada para archivos con más de {days_threshold} días'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process")
async def process_images(
    request: ImageProcessRequest,
    s3_client = Depends(get_s3_client),
    config = Depends(get_settings)
):
    if not request.images:
        raise HTTPException(status_code=400, detail="Faltan imágenes requeridas")
    
    session_id = request.session_id
    
    # Generar ID único para este procesamiento
    process_id = str(uuid.uuid4())
    
    # Parámetros optimizados según configuración
    resolution_factor = 0.5 if config.LOW_RESOURCE_MODE else 1.0
    
    try:
        # Los resultados del procesamiento se guardarán en S3
        model_key = f"models/{session_id}/{process_id}.obj"
        
        # Simular procesamiento (en el MVP real, aquí realizarías el modelado 3D)
        # Esta implementación solo es un placeholder para mostrar la optimización
        
        # Subir archivo de resultado (esto es solo un placeholder)
        # En una implementación real, generarías el modelo 3D y lo subirías a S3
        # usando la StorageClass adecuada según la configuración
        
        storage_class = 'REDUCED_REDUNDANCY' if config.S3_REDUCED_REDUNDANCY else 'STANDARD'
        
        # Configurar metadatos para facilitar limpieza posterior
        metadata = {
            'creation-date': datetime.datetime.now().isoformat(),
            'session-id': session_id or 'unknown',
            'process-id': process_id
        }
        
        # URL donde se guardaría el modelo (en una implementación real)
        model_url = f"https://{config.S3_BUCKET}.s3.amazonaws.com/{model_key}"
        
        # Simular medidas basadas en la altura (esto sería calculado por el modelado 3D real)
        measurements = {
            'height': request.height,
            'shoulder_width': request.height * 0.259,  # Proporción promedio
            'chest': request.height * 0.279,           # Proporción promedio
            'waist': request.height * 0.235,           # Proporción promedio
            'hips': request.height * 0.291             # Proporción promedio
        }
        
        return {
            'success': True,
            'model_url': model_url,
            'process_id': process_id,
            'measurements': measurements
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 