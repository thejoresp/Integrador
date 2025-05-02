import os
import logging
from dotenv import load_dotenv
from typing import Set, Tuple, Any
from pathlib import Path

load_dotenv()

# Configuración base
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# Asegurar que existan los directorios necesarios
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Modelos y rutas de archivos pre-entrenados
MODEL_DIR = os.path.join(BASE_DIR, "models", "pretrained")
os.makedirs(MODEL_DIR, exist_ok=True)

# Configuración de modelos
MODELS_DIR = os.path.join(BASE_DIR, "app", "models")

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def ensure_upload_dir():
    """Asegura que exista el directorio de uploads"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)

class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # App Configuration
    UPLOAD_FOLDER: str = 'uploads'
    MAX_CONTENT_LENGTH: int = 15 * 1024 * 1024  # 15MB max-limit (Optimizado para fotos faciales)
    ALLOWED_EXTENSIONS: Set[str] = {'jpg', 'jpeg', 'png'}
    
    # Configuraciones de optimización
    IMG_COMPRESSION_QUALITY: int = int(os.getenv('IMG_COMPRESSION_QUALITY', '85'))
    MAINTENANCE_TOKEN: str = os.getenv('MAINTENANCE_TOKEN', 'cambiar-en-produccion')
    
    # FastAPI Configuration
    FASTAPI_HOST: str = os.getenv('FASTAPI_HOST', '0.0.0.0')
    FASTAPI_PORT: int = int(os.getenv('FASTAPI_PORT', '8080'))
    WORKERS: int = int(os.getenv('WORKERS', '1'))
    
    # Modo de desarrollo o producción (afecta configuraciones de optimización)
    ENV_MODE: str = os.getenv('FASTAPI_ENV', 'development')
    
    @property
    def is_production(self) -> bool:
        return self.ENV_MODE == 'production'

# Configuración de la app
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

# Configuraciones de modelos específicos
FACE_DETECTION_MODEL = "mediapipe"  # Alternativas: 'dlib', 'opencv'
AGE_GENDER_MODEL = "face-recognition"  # Alternativas: 'insightface'
EMOTION_MODEL = "mediapipe"  # Alternativas: 'fer'