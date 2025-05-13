from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
import os
import uuid
from pathlib import Path
import traceback
import sys
import logging
import shutil

from app.services.skin_service import SkinService
from app.models.skin_models import (
    SkinAnalysisResult,
    MoleAnalysisResult,
    SkinToneResult,
    CompleteSkinAnalysisResult
)
from app.core.logger import get_logger
from app.config import get_settings
from app.dependencies import get_skin_service, verify_optional_api_key

# Configuración
settings = get_settings()
logger = get_logger(__name__)

# Configuración de log más detallado
logging.basicConfig(level=logging.DEBUG)

# Crear router, quitando dependencias de autenticación
router = APIRouter(
    prefix="/skin",
    tags=["skin"],
    dependencies=[],  # Eliminamos dependencias a nivel de router
    responses={404: {"description": "No encontrado"}},
)


@router.post("/analyze/condition", response_model=SkinAnalysisResult)
async def analyze_skin_condition(
    file: UploadFile = File(...),
    skin_service: SkinService = Depends(get_skin_service)
):
    """
    Analiza la condición general de la piel, incluyendo hidratación, textura, poros y grasa.
    """
    try:
        logger.info(f"Solicitud de análisis de condición de piel recibida: {file.filename}")
        print(f"Solicitud de análisis de condición de piel recibida: {file.filename}", file=sys.stderr)
        
        # Imprimir cabeceras para depuración
        print(f"Content-Type: {file.content_type}", file=sys.stderr)
        
        # Verificar si content_type es None
        content_type = file.content_type or 'application/octet-stream'
        logger.info(f"Content-Type (ajustado): {content_type}")
        print(f"Content-Type (ajustado): {content_type}", file=sys.stderr)
        
        # Validar tipo de archivo
        if not _is_valid_image_content_type(content_type):
            logger.warning(f"Tipo de contenido no válido: {content_type}")
            # Intentaremos inferir el tipo de archivo desde la extensión
            extension = os.path.splitext(file.filename)[1].lower() if file.filename else ''
            if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                logger.info(f"La extensión del archivo es válida: {extension}, continuando a pesar del tipo de contenido")
                print(f"La extensión del archivo es válida: {extension}, continuando a pesar del tipo de contenido", file=sys.stderr)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Tipo de archivo no válido. Debe ser una imagen (jpg, png, etc.)"
                )
        
        # Guardar archivo subido
        file_path = await save_upload_file(file)
        logger.info(f"Archivo guardado en: {file_path}")
        print(f"Archivo guardado en: {file_path}", file=sys.stderr)
        
        # Verificar que el archivo realmente existe
        if not os.path.exists(file_path):
            logger.error(f"¡ERROR CRÍTICO! El archivo no existe después de guardarlo: {file_path}")
            print(f"¡ERROR CRÍTICO! El archivo no existe después de guardarlo: {file_path}", file=sys.stderr)
            raise HTTPException(
                status_code=500,
                detail=f"Error interno: el archivo no se guardó correctamente"
            )
            
        # Verificar tamaño del archivo
        file_size = os.path.getsize(file_path)
        logger.info(f"Tamaño del archivo guardado: {file_size} bytes")
        print(f"Tamaño del archivo guardado: {file_size} bytes", file=sys.stderr)
        
        if file_size == 0:
            logger.error(f"¡ERROR CRÍTICO! El archivo guardado está vacío: {file_path}")
            print(f"¡ERROR CRÍTICO! El archivo guardado está vacío: {file_path}", file=sys.stderr)
            raise HTTPException(
                status_code=500,
                detail=f"Error interno: el archivo guardado está vacío"
            )
        
        # Realizar análisis
        logger.info(f"Iniciando análisis de condición...")
        print(f"Iniciando análisis de condición...", file=sys.stderr)
        result = await skin_service.analyze_skin_condition(file_path)
        logger.info(f"Análisis de condición completado exitosamente")
        print(f"Análisis de condición completado exitosamente", file=sys.stderr)
        
        return result
    except FileNotFoundError as e:
        logger.error(f"Archivo no encontrado: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"Archivo no encontrado: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        raise HTTPException(
            status_code=404,
            detail=f"Archivo no encontrado: {str(e)}"
        )
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"Error de validación: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        raise HTTPException(
            status_code=400,
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error en analyze_skin_condition: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"Error en analyze_skin_condition: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        raise HTTPException(
            status_code=500,
            detail=f"Error al analizar la condición de la piel: {str(e)}"
        )


@router.post("/analyze/moles", response_model=MoleAnalysisResult)
async def analyze_skin_moles(
    file: UploadFile = File(...),
    skin_service: SkinService = Depends(get_skin_service)
):
    """
    Detecta y analiza lunares en la imagen, clasificándolos como benignos, malignos o sospechosos.
    """
    try:
        logger.info(f"Solicitud de análisis de lunares recibida: {file.filename}")
        
        # Validar tipo de archivo
        if not _is_valid_image_content_type(file.content_type):
            logger.warning(f"Tipo de contenido no válido: {file.content_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de archivo no válido. Debe ser una imagen (jpg, png, etc.)"
            )
        
        # Guardar archivo subido
        file_path = await save_upload_file(file)
        logger.info(f"Archivo guardado en: {file_path}")
        
        # Realizar análisis
        result = await skin_service.analyze_moles(file_path)
        logger.info(f"Análisis de lunares completado exitosamente")
        
        return result
    except FileNotFoundError as e:
        logger.error(f"Archivo no encontrado: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail=f"Archivo no encontrado: {str(e)}"
        )
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error en analyze_skin_moles: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error al analizar lunares: {str(e)}"
        )


@router.post("/analyze/tone", response_model=SkinToneResult)
async def analyze_skin_tone(
    file: UploadFile = File(...),
    skin_service: SkinService = Depends(get_skin_service)
):
    """
    Analiza el tono de piel según la escala Fitzpatrick y proporciona recomendaciones.
    """
    try:
        logger.info(f"Solicitud de análisis de tono de piel recibida: {file.filename}")
        
        # Validar tipo de archivo
        if not _is_valid_image_content_type(file.content_type):
            logger.warning(f"Tipo de contenido no válido: {file.content_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de archivo no válido. Debe ser una imagen (jpg, png, etc.)"
            )
        
        # Guardar archivo subido
        file_path = await save_upload_file(file)
        logger.info(f"Archivo guardado en: {file_path}")
        
        # Realizar análisis
        result = await skin_service.analyze_skin_tone(file_path)
        logger.info(f"Análisis de tono completado exitosamente")
        
        return result
    except FileNotFoundError as e:
        logger.error(f"Archivo no encontrado: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail=f"Archivo no encontrado: {str(e)}"
        )
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error en analyze_skin_tone: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error al analizar el tono de piel: {str(e)}"
        )


@router.post("/analyze/complete")
async def analyze_skin_complete(file: UploadFile = File(...)):
    """
    Análisis completo de piel que incluye todos los tipos de análisis disponibles.
    
    Args:
        file: Imagen a analizar
        
    Returns:
        dict: Resultados combinados de los análisis
    """
    logger.info("Iniciando análisis completo de piel")
    
    try:
        # Guardar archivo temporalmente
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Realizar análisis completo
        skin_service = get_skin_service()
        result = await skin_service.perform_complete_analysis(file_path)
        
        # Agregar URL de la imagen al resultado para que el frontend pueda mostrarla
        file_url = f"/uploads/{unique_filename}"
        if isinstance(result, dict):
            result["image_url"] = file_url
        
        logger.info("Análisis completo finalizado exitosamente")
        return result
    except FileNotFoundError as e:
        logger.error(f"Archivo no encontrado: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail=f"Archivo no encontrado: {str(e)}"
        )
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error en analyze_skin_complete: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error al realizar análisis completo de piel: {str(e)}"
        )


@router.get("/recommendations", response_model=List[str])
async def get_skin_recommendations(
    hydration: Optional[float] = Query(None, ge=0, le=100, description="Nivel de hidratación (0-100)"),
    texture: Optional[float] = Query(None, ge=0, le=100, description="Calidad de la textura (0-100)"),
    pores: Optional[float] = Query(None, ge=0, le=100, description="Visibilidad de poros (0-100)"),
    oiliness: Optional[float] = Query(None, ge=0, le=100, description="Nivel de grasa (0-100)"),
    fitzpatrick_type: Optional[int] = Query(None, ge=1, le=6, description="Tipo de piel según Fitzpatrick (1-6)"),
    has_suspicious_moles: Optional[bool] = Query(None, description="Presencia de lunares sospechosos")
):
    """
    Genera recomendaciones personalizadas basadas en diferentes parámetros de la piel.
    """
    try:
        recommendations = []
        
        # Recomendaciones basadas en hidratación
        if hydration is not None and hydration < 60:
            recommendations.append("Aumentar la hidratación de la piel con productos hidratantes")
            
        # Recomendaciones basadas en textura
        if texture is not None and texture < 60:
            recommendations.append("Usar exfoliantes suaves para mejorar la textura de la piel")
            
        # Recomendaciones basadas en poros
        if pores is not None and pores < 60:
            recommendations.append("Utilizar productos astringentes para reducir la apariencia de los poros")
            
        # Recomendaciones basadas en grasa
        if oiliness is not None and oiliness < 60:
            recommendations.append("Controlar el exceso de grasa con productos matificantes")
            
        # Recomendaciones basadas en tipo de piel
        if fitzpatrick_type is not None:
            if fitzpatrick_type <= 2:
                recommendations.append("Usar protector solar de amplio espectro SPF 50+")
                recommendations.append("Evitar exposición solar prolongada, especialmente entre 10am-4pm")
            elif fitzpatrick_type <= 4:
                recommendations.append("Usar protector solar de amplio espectro SPF 30+")
            else:
                recommendations.append("Usar protector solar de amplio espectro SPF 15+")
        
        # Recomendaciones basadas en lunares
        if has_suspicious_moles:
            recommendations.append("Consultar a un dermatólogo para evaluar los lunares sospechosos")
        
        if not recommendations:
            recommendations.append("Mantener una rutina regular de cuidado facial")
            recommendations.append("Proteger la piel del sol con protector solar diariamente")
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error en get_skin_recommendations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar recomendaciones: {str(e)}"
        )


# Función auxiliar para guardar archivos
async def save_upload_file(file: UploadFile) -> str:
    """
    Guarda un archivo subido y devuelve su ruta.
    
    Args:
        file: Archivo subido
        
    Returns:
        str: Ruta al archivo guardado
    """
    try:
        # Generar nombre único para el archivo
        file_extension = os.path.splitext(file.filename)[1]
        if not file_extension:
            file_extension = ".jpg"  # Extensión por defecto si no se proporciona
            
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Asegurar que existe el directorio de uploads
        uploads_dir = Path(settings.UPLOAD_DIR)
        if not uploads_dir.exists():
            logger.info(f"Creando directorio de uploads: {uploads_dir}")
            print(f"Creando directorio de uploads: {uploads_dir}", file=sys.stderr)
            uploads_dir.mkdir(parents=True, exist_ok=True)
        
        # Construir ruta completa
        file_path = uploads_dir / unique_filename
        
        # Reutilizar file.file para posición del cursor
        await file.seek(0)
        
        # Guardar archivo
        content = await file.read()
        
        if not content:
            logger.error(f"El contenido del archivo está vacío: {file.filename}")
            print(f"El contenido del archivo está vacío: {file.filename}", file=sys.stderr)
            raise ValueError("El archivo subido no contiene datos")
            
        logger.info(f"Tamaño del contenido a guardar: {len(content)} bytes")
        print(f"Tamaño del contenido a guardar: {len(content)} bytes", file=sys.stderr)
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        logger.info(f"Archivo guardado: {file_path}")
        print(f"Archivo guardado: {file_path}", file=sys.stderr)
        
        # Verificar que el archivo se guardó correctamente
        if not os.path.exists(file_path):
            logger.error(f"Error: el archivo no se guardó correctamente: {file_path}")
            print(f"Error: el archivo no se guardó correctamente: {file_path}", file=sys.stderr)
            raise FileNotFoundError(f"No se pudo guardar el archivo en {file_path}")
        
        return str(file_path)
    except Exception as e:
        logger.error(f"Error al guardar archivo: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"Error al guardar archivo: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        raise


def _is_valid_image_content_type(content_type: str) -> bool:
    """
    Verifica si el tipo de contenido corresponde a una imagen válida.
    
    Args:
        content_type: Tipo de contenido MIME
        
    Returns:
        bool: True si es un tipo de imagen válido
    """
    # Si content_type es None, se considera como octet-stream
    if content_type is None:
        content_type = 'application/octet-stream'
        
    valid_types = [
        'image/jpeg', 
        'image/jpg', 
        'image/png', 
        'image/gif', 
        'image/bmp',
        'application/octet-stream',  # Para compatibilidad con algunos clientes
    ]
    
    # Verificar si el tipo de contenido está entre los válidos
    is_valid = content_type.lower() in valid_types
    
    if not is_valid:
        logger.warning(f"Tipo de contenido no válido: {content_type}")
        print(f"Tipo de contenido no válido: {content_type}", file=sys.stderr)
    else:
        logger.info(f"Tipo de contenido válido: {content_type}")
        print(f"Tipo de contenido válido: {content_type}", file=sys.stderr)
        
    return is_valid 