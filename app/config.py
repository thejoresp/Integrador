"""
Configuración centralizada para la aplicación de análisis facial.
Define constantes, configuraciones y ajustes para toda la aplicación.
"""

import os
import logging
from functools import lru_cache
from typing import Set, Dict, Any, List, Optional, Union
from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import validator

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

# Configuración base de directorios
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
MODEL_DIR = os.path.join(BASE_DIR, "models", "pretrained")

# Asegurar que existan los directorios necesarios
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Config(BaseSettings):
    """
    Configuración central de la aplicación utilizando Pydantic para validación.
    Los valores por defecto pueden ser sobrescritos por variables de entorno.
    """
    # Directorios de la aplicación (importante asegurar que estén disponibles)
    BASE_DIR: str = str(BASE_DIR)
    STATIC_DIR: str = STATIC_DIR
    TEMPLATE_DIR: str = TEMPLATE_DIR
    UPLOAD_DIR: str = UPLOAD_DIR
    
    # Configuración de la aplicación
    APP_NAME: str = "Sistema de Análisis de Piel - PielSana IA"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = "Plataforma avanzada para análisis de piel con detección de condiciones cutáneas, lunares y evaluación de tono."
    
    # Configuración del servidor
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True
    
    # Seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-for-development-only")
    API_KEY: str = os.getenv("API_KEY", "default-api-key-change-in-production")
    AUTH_ENABLED: bool = False  # Por defecto desactivada en desarrollo
    MAINTENANCE_TOKEN: str = os.getenv("MAINTENANCE_TOKEN", "maintenance-token")
    
    # Configuración de CORS
    ENABLE_CORS: bool = True
    CORS_ORIGINS: List[str] = ["*"]
    
    # Configuración de documentación
    ENABLE_DOCS: bool = True
    
    # Configuración de logs
    LOG_LEVEL: str = "INFO"
    
    # Configuración de límite de tasa
    RATE_LIMIT_ENABLED: bool = False
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Configuración de carga de archivos
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS: Set[str] = {"jpg", "jpeg", "png", "gif"}
    IMG_COMPRESSION_QUALITY: int = 85  # Calidad de compresión JPEG
    
    # Configuración de modelos
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")
    PRETRAINED_MODELS_DIR: str = os.path.join(MODELS_DIR, "pretrained")
    
    # Nuevas configuraciones para análisis de piel
    SKIN_MODELS_DIR: str = os.path.join(PRETRAINED_MODELS_DIR, "skin")
    ENABLE_SKIN_ANALYSIS: bool = True
    
    # Configuración de análisis facial
    FACIAL_MODELS_DIR: str = os.path.join(PRETRAINED_MODELS_DIR, "facial")
    ENABLE_FACIAL_ANALYSIS: bool = False
    
    # Configuración de hardware
    FORCE_CPU: bool = os.getenv("FORCE_CPU", "false").lower() == "true"
    
    # Configuración de entorno
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Características y capacidades
    ENABLE_AUTHENTICATION: bool = False
    
    class Config:
        """Configuración interna de Pydantic."""
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Permite campos extras
    
    @property
    def is_production(self) -> bool:
        """Indica si la aplicación está en entorno de producción."""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Indica si la aplicación está en entorno de desarrollo."""
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def is_testing(self) -> bool:
        """Indica si la aplicación está en modo pruebas."""
        return self.ENVIRONMENT.lower() == "testing"
    
    # Validadores
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parsea los orígenes CORS desde una cadena separada por comas."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_EXTENSIONS", pre=True)
    def parse_allowed_extensions(cls, v):
        """Parsea las extensiones permitidas desde una cadena separada por comas."""
        if isinstance(v, str):
            return {ext.strip().lower() for ext in v.split(",")}
        return v


@lru_cache()
def get_settings() -> Config:
    """
    Obtiene la configuración de la aplicación.
    
    La función está decorada con lru_cache para evitar cargar la configuración
    múltiples veces durante el ciclo de vida de la aplicación.
    
    Returns:
        Config: Objeto con la configuración de la aplicación
    """
    return Config()


def ensure_upload_dir():
    """
    Asegura que exista el directorio de uploads.
    Utilizada durante el inicio de la aplicación.
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)