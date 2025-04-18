"""
Utilidades para manejo centralizado de errores en la aplicación
"""
import sys
import logging
import traceback
from typing import Dict, Any, Optional, Type, Callable
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

# Configurar logger
logger = logging.getLogger(__name__)

# Tipos comunes de excepciones y sus códigos HTTP correspondientes
ERROR_TYPES = {
    ValueError: status.HTTP_400_BAD_REQUEST,
    KeyError: status.HTTP_400_BAD_REQUEST,
    FileNotFoundError: status.HTTP_404_NOT_FOUND,
    PermissionError: status.HTTP_403_FORBIDDEN,
    NotImplementedError: status.HTTP_501_NOT_IMPLEMENTED
}

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Manejador general de excepciones para la aplicación

    Args:
        request: Objeto de solicitud HTTP
        exc: Excepción que fue lanzada

    Returns:
        JSONResponse: Respuesta JSON con información del error
    """
    # Determinar código HTTP apropiado
    error_type = type(exc)
    status_code = ERROR_TYPES.get(error_type, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Registrar excepción con detalles
    logger.error(
        f"Error no controlado: {error_type.__name__}: {str(exc)}\n"
        f"URL: {request.method} {request.url}\n"
        f"Traceback: {''.join(traceback.format_tb(exc.__traceback__))}"
    )
    
    # En desarrollo mostramos más detalles, en producción solo mensaje genérico
    is_production = request.app.state.config.is_production if hasattr(request.app.state, "config") else False
    
    error_detail = {
        "error": error_type.__name__,
        "detail": str(exc) if not is_production or status_code < 500 else "Error interno del servidor"
    }
    
    if not is_production and status_code == 500:
        error_detail["traceback"] = traceback.format_exception(
            type(exc), exc, exc.__traceback__
        )
        
    return JSONResponse(
        status_code=status_code,
        content=error_detail
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Manejador para excepciones HTTP
    
    Args:
        request: Objeto de solicitud HTTP
        exc: Excepción HTTP que fue lanzada
        
    Returns:
        JSONResponse: Respuesta JSON con información del error
    """
    # Registrar excepción HTTP
    if exc.status_code >= 500:
        logger.error(f"Error HTTP {exc.status_code}: {exc.detail}")
    else:
        logger.warning(f"Error HTTP {exc.status_code}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )

def configure_error_handlers(app):
    """
    Configura los manejadores de errores para la aplicación FastAPI
    
    Args:
        app: Instancia de la aplicación FastAPI
    """
    # Registrar handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # Manejadores específicos para ciertos tipos de error
    for error_type, status_code in ERROR_TYPES.items():
        app.add_exception_handler(
            error_type, 
            lambda request, exc, status=status_code: 
                general_exception_handler(request, exc)
        )
