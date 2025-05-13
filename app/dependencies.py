"""
Dependencias para la aplicación de análisis facial.
Proporciona funciones para inyección de dependencias en los endpoints.
"""

import logging
from fastapi import Depends

from app.config import get_settings, Config

import os
from functools import lru_cache
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.logger import get_logger

# Importar los servicios
from app.services.skin_service import SkinService

logger = get_logger(__name__)
settings = get_settings()

# Configurar autenticación como deshabilitada
settings.AUTH_ENABLED = False

# Sistema de autenticación básico
security = HTTPBearer(auto_error=False)  # Hacemos que no lance errores automáticamente

# Instancia singleton de servicios
skin_service_instance = None

@lru_cache
def get_skin_service() -> SkinService:
    """
    Devuelve una instancia singleton del servicio de análisis de piel.
    
    Returns:
        SkinService: Instancia del servicio
    """
    global skin_service_instance
    
    if skin_service_instance is None:
        try:
            # Configurar la ruta a los modelos
            base_dir = settings.BASE_DIR
            models_path = os.path.join(base_dir, "models", "pretrained", "skin")
            
            # Asegurar que el directorio existe
            os.makedirs(models_path, exist_ok=True)
            
            # Determinar el dispositivo a utilizar ('cpu' o 'cuda')
            device = 'cpu'  # Por defecto usamos CPU
            # Si el sistema tiene GPU y las configuraciones lo permiten, usar cuda
            try:
                import torch
                if torch.cuda.is_available() and not settings.FORCE_CPU:
                    device = 'cuda'
                    logger.info("Aceleración GPU disponible y habilitada")
            except ImportError:
                logger.warning("PyTorch no está disponible, usando CPU para inferencia")
            
            # Crear instancia
            logger.info(f"Inicializando Skin Service con modelos en: {models_path}, dispositivo: {device}")
            skin_service_instance = SkinService(models_path=models_path, device=device)
            logger.info("Skin Service inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar Skin Service: {str(e)}")
            # No elevamos la excepción aquí, sino que permitimos la creación con None
            # y manejamos los errores en los endpoints
            skin_service_instance = SkinService()
    
    return skin_service_instance


# Función para verificar API key o token - AHORA SIEMPRE DEVUELVE TRUE
async def verify_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> bool:
    """
    Verifica la API key o token de autenticación.
    Ahora simplemente devuelve True para facilitar pruebas.
    
    Args:
        credentials: Credenciales HTTP (opcional)
        
    Returns:
        bool: True siempre
    """
    # Autenticación deshabilitada para pruebas
    return True


# Dependencia opcional para verificar API key solo si está habilitada
async def verify_optional_api_key(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> bool:
    """
    Siempre permite el acceso, incluso sin token.
    
    Args:
        request: Solicitud HTTP
        credentials: Credenciales HTTP (opcional)
        
    Returns:
        bool: True siempre
    """
    # Autenticación deshabilitada para pruebas
    return True


# Dependencia para limitar la tasa de solicitudes
async def rate_limit(request: Request) -> None:
    """
    Limita la tasa de solicitudes a la API.
    Actualmente deshabilitado para pruebas.
    
    Args:
        request: Solicitud HTTP
    """
    # Rate limit deshabilitado para pruebas
    return None
