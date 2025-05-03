"""
Configuración centralizada para la aplicación de análisis facial.
Define constantes, configuraciones y ajustes para toda la aplicación.
"""

import os
import logging
from functools import lru_cache
from typing import Set, Dict, Any
from pydantic_settings import BaseSettings
from pathlib import Path

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
    # Configuración de la aplicación
    APP_NAME: str = "Sistema de Análisis Facial"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API para análisis de rostros usando deep learning y visión por computadora"
    
    # Configuración del servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8080"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cambiar-en-produccion-clave-secreta-larga")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de carga de archivos
    UPLOAD_FOLDER: str = UPLOAD_DIR
    MAX_CONTENT_LENGTH: int = 15 * 1024 * 1024  # 15MB
    ALLOWED_EXTENSIONS: Set[str] = {"jpg", "jpeg", "png"}
    
    # Optimización de imágenes
    IMG_COMPRESSION_QUALITY: int = int(os.getenv("IMG_COMPRESSION_QUALITY", "85"))
    IMG_MAX_DIMENSION: int = 1920  # Dimensión máxima para imágenes grandes
    
    # Mantenimiento
    MAINTENANCE_MODE: bool = os.getenv("MAINTENANCE_MODE", "False").lower() in ("true", "1", "t")
    MAINTENANCE_TOKEN: str = os.getenv("MAINTENANCE_TOKEN", "cambiar-en-produccion")
    
    # Configuración de modelos
    FACE_DETECTION_MODEL: str = os.getenv("FACE_DETECTION_MODEL", "mediapipe")
    AGE_GENDER_MODEL: str = os.getenv("AGE_GENDER_MODEL", "face-recognition")
    EMOTION_MODEL: str = os.getenv("EMOTION_MODEL", "mediapipe")
    SKIN_ANALYSIS_MODEL: str = os.getenv("SKIN_ANALYSIS_MODEL", "custom")
    
    # Modo de entorno (desarrollo, producción, pruebas)
    ENV: str = os.getenv("ENV", "development")
    
    class Config:
        """Configuración interna de Pydantic."""
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Permite campos extras
    
    @property
    def is_production(self) -> bool:
        """Indica si la aplicación está en modo producción."""
        return self.ENV.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Indica si la aplicación está en modo desarrollo."""
        return self.ENV.lower() == "development"
    
    @property
    def is_testing(self) -> bool:
        """Indica si la aplicación está en modo pruebas."""
        return self.ENV.lower() == "testing"


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