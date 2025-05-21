"""
Utilidades para configuración y gestión de logs
"""
import logging
import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, Union
from fastapi import Request, Response

# Formateadores de logs
class JsonFormatter(logging.Formatter):
    """Formateador de logs en formato JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Formatea un registro de log como JSON
        
        Args:
            record: Registro de log a formatear
            
        Returns:
            str: Registro formateado como JSON
        """
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Incluir excepción si existe
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
        
        # Incluir datos extra si existen
        if hasattr(record, 'extra'):
            log_data['extra'] = record.extra
            
        return json.dumps(log_data)

def configure_logging(
    log_level: str = "INFO", 
    json_format: bool = False,
    log_file: Optional[str] = None
) -> None:
    """
    Configura el sistema de logging
    
    Args:
        log_level: Nivel de logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Si es True, usa formato JSON para logs
        log_file: Ruta opcional para guardar logs en archivo
    """
    # Obtener nivel de log numérico
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Crear formateador según formato solicitado
    if json_format:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    # Configurar handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    handlers = [console_handler]
    
    # Agregar handler para archivo si se especificó
    if log_file:
        # Crear directorio para logs si no existe
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    # Configurar logger raíz
    logging.basicConfig(
        level=numeric_level,
        handlers=handlers
    )

class RequestResponseLogger:
    """Utilidad para registrar detalles de solicitudes y respuestas HTTP"""
    
    def __init__(self, include_headers: bool = False, include_body: bool = False):
        """
        Inicializa el logger de solicitudes
        
        Args:
            include_headers: Si es True, incluye headers en logs
            include_body: Si es True, incluye cuerpo de solicitudes en logs
        """
        self.logger = logging.getLogger("api.request")
        self.include_headers = include_headers
        self.include_body = include_body
    
    async def log_request(self, request: Request) -> None:
        """
        Registra detalles de una solicitud HTTP
        
        Args:
            request: Objeto de solicitud FastAPI
        """
        log_data = {
            'method': request.method,
            'path': request.url.path,
            'query': str(request.query_params),
            'client': request.client.host if request.client else "unknown"
        }
        
        if self.include_headers:
            log_data['headers'] = dict(request.headers)
            
        if self.include_body and request.method in ['POST', 'PUT', 'PATCH']:
            try:
                # Para solicitudes estándar
                body = await request.json()
                log_data['body'] = body
            except:
                # Para formularios y otros tipos de contenido
                log_data['body'] = 'non-json-body'
        
        self.logger.info(f"Solicitud recibida: {json.dumps(log_data)}")
    
    def log_response(self, response: Response, processing_time: float) -> None:
        """
        Registra detalles de una respuesta HTTP
        
        Args:
            response: Objeto de respuesta HTTP
            processing_time: Tiempo de procesamiento en segundos
        """
        log_data = {
            'status_code': response.status_code,
            'processing_time_ms': round(processing_time * 1000, 2)
        }
        
        if self.include_headers:
            log_data['headers'] = dict(response.headers)
            
        self.logger.info(f"Respuesta enviada: {json.dumps(log_data)}")

def get_method_logger(module_name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para el módulo especificado
    
    Args:
        module_name: Nombre del módulo
        
    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(module_name)
