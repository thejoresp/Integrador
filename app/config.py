"""
Módulo de configuración centralizada para la aplicación de análisis facial.

Este módulo gestiona todas las configuraciones necesarias para el funcionamiento
de la aplicación, incluyendo rutas, parámetros de AWS, y opciones de los modelos.
"""
import os
import logging
from dotenv import load_dotenv
from typing import Set, Tuple, Any, Dict, Union
from pathlib import Path
from functools import lru_cache

# Cargar variables de entorno del archivo .env
load_dotenv()

# Rutas de directorios principales
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"
UPLOAD_DIR = BASE_DIR / "uploads"
MODEL_DIR = BASE_DIR / "models" / "pretrained"
TEMP_DIR = BASE_DIR / "temp"

# Asegurar que existan los directorios necesarios
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuración de la app
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MIN_IMAGE_RESOLUTION = (2000, 2000)  # Resolución mínima para buena calidad

# Configuraciones de modelos
MODELS_CONFIG = {
    "face_detection": {
        "default": "mediapipe",
        "alternatives": ["dlib", "opencv"]
    },
    "age_gender": {
        "default": "deepface",
        "alternatives": ["insightface"]
    },
    "emotion": {
        "default": "deepface",
        "alternatives": ["fer"]
    }
}


@lru_cache()
def get_aws_config() -> Dict[str, str]:
    """
    Retorna la configuración de AWS con caché para evitar 
    múltiples lecturas de variables de entorno.
    
    Returns:
        Dict[str, str]: Configuración de AWS
    """
    return {
        "region": os.getenv("AWS_REGION", "us-east-1"),
        "access_key_id": os.getenv("AWS_ACCESS_KEY_ID", ""),
        "secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
        "bucket": os.getenv("S3_BUCKET", "facial-analysis-app"),
        "auto_cleanup_enabled": os.getenv("S3_AUTO_CLEANUP_ENABLED", "FALSE").upper() == "TRUE",
        "auto_cleanup_days": int(os.getenv("S3_AUTO_CLEANUP_DAYS", "30")),
        "reduced_redundancy": os.getenv("S3_REDUCED_REDUNDANCY", "TRUE").upper() == "TRUE"
    }


def ensure_dirs() -> None:
    """
    Asegura que existan todos los directorios necesarios para la aplicación.
    """
    for directory in [UPLOAD_DIR, MODEL_DIR, TEMP_DIR, STATIC_DIR]:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Directorio asegurado: {directory}")


class AppConfig:
    """
    Clase de configuración de la aplicación que centraliza todos los parámetros.
    Permite acceso a configuración vía propiedades y métodos.
    """
    def __init__(self):
        """Inicializa la configuración de la aplicación"""
        self.secret_key: str = os.getenv("SECRET_KEY", "dev-key-change-in-production")
        
        # Configuración de la aplicación
        self.env_mode: str = os.getenv("FASTAPI_ENV", "development")
        self.host: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
        self.port: int = int(os.getenv("FASTAPI_PORT", "8000"))
        self.workers: int = int(os.getenv("WORKERS", "1"))
        self.low_resource_mode: bool = os.getenv("LOW_RESOURCE_MODE", "TRUE").upper() == "TRUE"
        
        # Configuración de procesamiento de imágenes
        self.allowed_extensions: Set[str] = ALLOWED_EXTENSIONS
        self.max_upload_size: int = MAX_UPLOAD_SIZE
        self.min_image_resolution: Tuple[int, int] = MIN_IMAGE_RESOLUTION
        self.img_compression_quality: int = int(os.getenv("IMG_COMPRESSION_QUALITY", "85"))
        
        # Cargar configuración de AWS
        aws_config = get_aws_config()
        self.aws_region = aws_config["region"]
        self.aws_access_key_id = aws_config["access_key_id"]
        self.aws_secret_access_key = aws_config["secret_access_key"]
        self.s3_bucket = aws_config["bucket"]
        self.s3_auto_cleanup_enabled = aws_config["auto_cleanup_enabled"]
        self.s3_auto_cleanup_days = aws_config["auto_cleanup_days"]
        self.s3_reduced_redundancy = aws_config["reduced_redundancy"]
        
        # Configuración de mantenimiento
        self.maintenance_token: str = os.getenv("MAINTENANCE_TOKEN", "cambiar-en-produccion")
    
    @property
    def is_production(self) -> bool:
        """Determina si la aplicación está en modo producción"""
        return self.env_mode.lower() == "production"
    
    def get_model_config(self, model_type: str) -> Dict[str, Union[str, list]]:
        """
        Obtiene la configuración específica para un tipo de modelo
        
        Args:
            model_type: Tipo de modelo (face_detection, age_gender, emotion)
            
        Returns:
            Dict con la configuración del modelo
        """
        if model_type not in MODELS_CONFIG:
            raise ValueError(f"Tipo de modelo desconocido: {model_type}")
        return MODELS_CONFIG[model_type]
    
    def validate_file_extension(self, filename: str) -> bool:
        """
        Valida que la extensión del archivo sea permitida
        
        Args:
            filename: Nombre del archivo a validar
            
        Returns:
            bool: True si la extensión es válida
        """
        if not filename or "." not in filename:
            return False
        ext = filename.rsplit(".", 1)[1].lower()
        return ext in self.allowed_extensions


# Crear una instancia de configuración global
config = AppConfig()

# Para mantener compatibilidad con código existente
AWS_REGION = config.aws_region
AWS_ACCESS_KEY_ID = config.aws_access_key_id
AWS_SECRET_ACCESS_KEY = config.aws_secret_access_key
S3_BUCKET = config.s3_bucket
ALLOWED_EXTENSIONS = config.allowed_extensions