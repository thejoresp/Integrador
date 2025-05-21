"""
Utilidades para validación de datos y parámetros de la aplicación
"""
import re
import logging
import os
from typing import List, Dict, Any, Optional, Union, Set
from fastapi import UploadFile, HTTPException

# Configurar logger
logger = logging.getLogger(__name__)

def validate_file_size(file: UploadFile, max_size_mb: float = 10.0) -> bool:
    """
    Valida que un archivo no exceda el tamaño máximo permitido
    
    Args:
        file: El archivo a validar
        max_size_mb: Tamaño máximo en MB
        
    Returns:
        bool: True si el archivo es válido, False si excede el tamaño
    """
    try:
        # Posición actual en el archivo
        current_pos = file.file.tell()
        
        # Ir al final del archivo para obtener tamaño
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        
        # Volver a la posición original
        file.file.seek(current_pos)
        
        # Convertir MB a bytes y comparar
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if size > max_size_bytes:
            logger.warning(f"Archivo demasiado grande: {size/1024/1024:.2f}MB > {max_size_mb}MB")
            return False
            
        return True
    except Exception as e:
        logger.error(f"Error al validar tamaño de archivo: {str(e)}")
        return False

def validate_file_extension(filename: str, allowed_extensions: Set[str]) -> bool:
    """
    Valida que la extensión de un archivo sea permitida
    
    Args:
        filename: Nombre del archivo a validar
        allowed_extensions: Conjunto de extensiones permitidas (ej: {'.jpg', '.png'})
        
    Returns:
        bool: True si la extensión es permitida, False en caso contrario
    """
    if not filename or '.' not in filename:
        return False
        
    extension = os.path.splitext(filename)[1].lower()
    is_valid = extension in allowed_extensions
    
    if not is_valid:
        logger.warning(f"Extensión no permitida: {extension}")
        
    return is_valid

def validate_email(email: str) -> bool:
    """
    Valida que una cadena tenga formato de correo electrónico
    
    Args:
        email: La dirección de correo a validar
        
    Returns:
        bool: True si el formato es válido, False en caso contrario
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_parameters(parameters: Dict[str, Any], required_params: List[str]) -> None:
    """
    Valida que todos los parámetros requeridos estén presentes
    
    Args:
        parameters: Diccionario de parámetros a validar
        required_params: Lista de nombres de parámetros requeridos
        
    Raises:
        HTTPException: Si falta algún parámetro requerido
    """
    missing_params = [param for param in required_params if param not in parameters]
    
    if missing_params:
        missing_str = ", ".join(missing_params)
        logger.warning(f"Parámetros faltantes: {missing_str}")
        raise HTTPException(
            status_code=400, 
            detail=f"Faltan los siguientes parámetros requeridos: {missing_str}"
        )

def safe_int_parse(value: Union[str, int, None], default: int = 0) -> int:
    """
    Convierte un valor a entero de manera segura
    
    Args:
        value: El valor a convertir
        default: Valor por defecto si falla la conversión
        
    Returns:
        int: El valor convertido o el valor por defecto
    """
    if value is None:
        return default
        
    if isinstance(value, int):
        return value
        
    try:
        return int(value)
    except (ValueError, TypeError):
        logger.debug(f"No se pudo convertir '{value}' a entero, usando valor por defecto: {default}")
        return default

def safe_float_parse(value: Union[str, float, None], default: float = 0.0) -> float:
    """
    Convierte un valor a punto flotante de manera segura
    
    Args:
        value: El valor a convertir
        default: Valor por defecto si falla la conversión
        
    Returns:
        float: El valor convertido o el valor por defecto
    """
    if value is None:
        return default
        
    if isinstance(value, float):
        return value
        
    try:
        return float(value)
    except (ValueError, TypeError):
        logger.debug(f"No se pudo convertir '{value}' a float, usando valor por defecto: {default}")
        return default
