from fastapi import APIRouter, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import shutil
from pathlib import Path
import asyncio

# Importar el servicio de análisis de piel
from app.services.skin_analysis_service import get_image_embeddings, load_skin_model

# Configurar el router
router = APIRouter()

# Plantillas
templates = Jinja2Templates(directory="app/views/templates")

UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Precargar el modelo al iniciar esta parte de la aplicación (opcional pero recomendado)
# Esto asegura que el modelo esté listo cuando llegue la primera solicitud a este controlador.
# Si tienes un evento de startup global en main.py, es mejor hacerlo allí.
# Por ahora, lo llamaremos aquí para asegurarnos de que se intente cargar.
# En un entorno de producción real, la gestión de la carga del modelo 
# y los errores asociados debería ser más robusta.
@router.on_event("startup")
async def startup_event():
    print("Intentando precargar el modelo de análisis de piel...")
    load_skin_model() # Esta función ahora imprime si tiene éxito o falla

@router.get("/", response_class=HTMLResponse)
async def get_upload_page(request: Request):
    """Sirve la página principal para cargar imágenes."""
    return templates.TemplateResponse("upload.html", {"request": request})

@router.post("/upload") # Quitamos response_class=HTMLResponse para que FastAPI infiera por el return
async def handle_image_upload(request: Request, file: UploadFile = File(...)):
    """
    Maneja la subida de la imagen, la procesa con el servicio de análisis de piel,
    y luego redirige a la página de resultados.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")

    try:
        image_bytes = await file.read() # Leer los bytes del archivo subido
        
        print(f"Procesando imagen: {file.filename}")
        embeddings = get_image_embeddings(image_bytes)
        
        if embeddings is not None:
            print(f"Embeddings obtenidos para {file.filename}: {embeddings[:10]}... (primeros 10 de {len(embeddings)})")
            # Aquí podrías guardar los embeddings, o pasarlos a la página de resultados
            # Por ahora, solo imprimimos y mantenemos la redirección simple
            # Para pasar datos a la página de resultados, necesitarías un mecanismo
            # como guardarlos en una base de datos/caché con un ID y pasar ese ID,
            # o pasarlos directamente si son pequeños y la URL lo permite (no recomendado para embeddings)
        else:
            print(f"No se pudieron obtener embeddings para {file.filename}.")
            # Considerar devolver un mensaje de error al usuario aquí
            # Por ejemplo, renderizar de nuevo la página de subida con un error:
            return templates.TemplateResponse("upload.html", {
                "request": request, 
                "error_message": f"Error al procesar la imagen: No se pudieron generar los embeddings."
            }, status_code=500)

        # Guardar el archivo temporalmente (opcional, si aún lo necesitas para algo)
        # file_path = UPLOAD_DIR / file.filename
        # with open(file_path, "wb") as buffer:
        #     # Como ya leímos file.file, necesitamos volver al inicio si queremos guardarlo así
        #     await file.seek(0)
        #     shutil.copyfileobj(file.file, buffer)
        
        return RedirectResponse(url=f"/results?image_name={file.filename}&analysis_status=success", status_code=303)

    except HTTPException as http_exc:
        raise http_exc # Re-lanzar HTTPExceptions para que FastAPI las maneje
    except Exception as e:
        print(f"Error crítico al procesar la imagen: {e}")
        return templates.TemplateResponse("upload.html", {
            "request": request, 
            "error_message": f"Error crítico al procesar la imagen: {str(e)}"
        }, status_code=500)

@router.get("/results", response_class=HTMLResponse)
async def get_results_page(request: Request, image_name: str = None, analysis_status: str = None):
    """Sirve la página de resultados."""
    # Aquí, en una aplicación real, obtendrías los resultados del análisis
    # basados en algún identificador o de una sesión.
    # Por ahora, solo usamos el image_name y un estado simulado.
    mock_results = {
        "image_name": image_name if image_name else "Imagen de ejemplo",
        "condition": "Análisis en proceso... (simulado)" if analysis_status == "success" else "Análisis fallido (simulado)",
        "severity": "-",
        "recommendation": "Los embeddings se han generado y mostrado en consola (simulado)."
    }
    if analysis_status == "success" and image_name:
         mock_results["info"] = f"Los embeddings para {image_name} se generaron (ver consola del servidor)."
    elif image_name:
        mock_results["info"] = f"Hubo un problema al generar embeddings para {image_name}."

    return templates.TemplateResponse("results.html", {"request": request, "results": mock_results})

@router.post("/api/analyze", tags=["Skin Analysis API"])
async def api_analyze_skin(file: UploadFile = File(...)):
    """Endpoint API para analizar una imagen y devolver embeddings en JSON."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")
    
    try:
        image_bytes = await file.read()
        embeddings = get_image_embeddings(image_bytes)
        
        if embeddings is not None:
            return {
                "filename": file.filename,
                "content_type": file.content_type,
                "embeddings": embeddings.tolist(), # Convertir array numpy a lista para JSON
                "embedding_shape": embeddings.shape
            }
        else:
            raise HTTPException(status_code=500, detail="No se pudieron generar embeddings para la imagen.")
    except Exception as e:
        print(f"Error en API /api/analyze: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor al analizar la imagen: {str(e)}") 