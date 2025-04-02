import os
from dotenv import load_dotenv
from typing import Set, Tuple, Any

load_dotenv()

class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID: str = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: str = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION: str = os.getenv('AWS_REGION', 'us-east-1')
    S3_BUCKET: str = os.getenv('S3_BUCKET')
    
    # Optimizaciones para capa gratuita AWS
    S3_AUTO_CLEANUP_ENABLED: bool = os.getenv('S3_AUTO_CLEANUP_ENABLED', 'FALSE').upper() == 'TRUE'
    S3_AUTO_CLEANUP_DAYS: int = int(os.getenv('S3_AUTO_CLEANUP_DAYS', '30'))
    S3_REDUCED_REDUNDANCY: bool = os.getenv('S3_REDUCED_REDUNDANCY', 'TRUE').upper() == 'TRUE'
    IMG_COMPRESSION_QUALITY: int = int(os.getenv('IMG_COMPRESSION_QUALITY', '85'))
    MAINTENANCE_TOKEN: str = os.getenv('MAINTENANCE_TOKEN', 'cambiar-en-produccion')
    
    # App Configuration
    UPLOAD_FOLDER: str = 'uploads'
    MAX_CONTENT_LENGTH: int = 50 * 1024 * 1024  # 50MB max-limit
    ALLOWED_EXTENSIONS: Set[str] = {'jpg', 'jpeg', 'png', 'heic'}
    
    # Processing Configuration
    MIN_IMAGE_RESOLUTION: Tuple[int, int] = (2000, 2000)  # Minimum resolution for good quality
    TEMP_DIR: str = 'temp'
    
    # Modo de bajo consumo (menor resolución en procesamiento)
    LOW_RESOURCE_MODE: bool = os.getenv('LOW_RESOURCE_MODE', 'TRUE').upper() == 'TRUE'
    
    # FastAPI Configuration
    FASTAPI_HOST: str = os.getenv('FASTAPI_HOST', '0.0.0.0')
    FASTAPI_PORT: int = int(os.getenv('FASTAPI_PORT', '8000'))
    WORKERS: int = int(os.getenv('WORKERS', '1'))  # Número de workers, 1 es óptimo para capa gratuita
    
    # Modo de desarrollo o producción (afecta configuraciones de optimización)
    ENV_MODE: str = os.getenv('FASTAPI_ENV', 'development')
    
    @property
    def is_production(self) -> bool:
        return self.ENV_MODE == 'production' 