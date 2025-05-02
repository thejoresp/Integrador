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

def allowed_file(filename: str, allowed_extensions: set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

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
    
    # Obtener la ruta de la carpeta uploads y asegurar que exista
    upload_folder = getattr(config, "UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    
    # Guardar archivo localmente
    temp_path = os.path.join(upload_folder, filename)
    
    # Escribir el archivo en el sistema de archivos
    content = await image.read()
    with open(temp_path, "wb") as temp_file:
        temp_file.write(content)

    try:
        # Optimizar la imagen antes si es JPEG
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
            
            # Reemplazar el archivo original con la versión optimizada
            os.remove(temp_path)
            os.rename(optimized_temp_path, temp_path)

        # Generar URL para acceso local
        file_url = f"/uploads/{filename}"
        
        return {
            'success': True,
            'filename': filename,
            'session_id': session_id,
            'url': file_url
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
        # Buscar archivos en la carpeta uploads con más de X días
        days_threshold = request.days_threshold
        threshold_date = datetime.datetime.now() - datetime.timedelta(days=days_threshold)
        
        # Obtener la ruta de la carpeta uploads
        upload_folder = getattr(config, "UPLOAD_FOLDER", "uploads")
        if not os.path.exists(upload_folder):
            return {
                'success': True,
                'message': f'No existe la carpeta {upload_folder}'
            }
        
        # Contar archivos eliminados
        deleted_count = 0
        
        # Recorrer todos los archivos y verificar su fecha de modificación
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path):
                # Obtener la fecha de modificación del archivo
                file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mtime < threshold_date:
                    # Eliminar el archivo
                    os.remove(file_path)
                    deleted_count += 1
        
        return {
            'success': True,
            'message': f'Se eliminaron {deleted_count} archivos con más de {days_threshold} días'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 