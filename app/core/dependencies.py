import boto3
from fastapi import Depends, Request

from app.config import Config, get_settings
from app.core.exceptions import ServiceConnectionError

class DatabaseClient:
    def __init__(self, config: Config):
        self.config = config
        self.client = None
        # Inicializar cliente de base de datos según configuración

    def connect(self):
        # Implementar lógica de conexión
        pass

    def close(self):
        if self.client:
            # Cerrar conexión
            self.client = None

def get_db_client(config: Config = Depends(get_settings)):
    """Proporciona un cliente de base de datos con manejo de errores."""
    client = DatabaseClient(config)
    try:
        client.connect()
        yield client
    except Exception as e:
        raise ServiceConnectionError(f"Error de conexión a base de datos: {str(e)}")
    finally:
        client.close()

def get_templates(request: Request):
    """Proporciona acceso a las plantillas desde el estado de la aplicación."""
    return request.app.state.templates

def get_s3_client(config = Depends(get_settings)):
    """Proporciona un cliente de S3 configurado."""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=config.AWS_ACCESS_KEY,
            aws_secret_access_key=config.AWS_SECRET_KEY,
            region_name=config.AWS_REGION
        )
        return s3_client
    except Exception as e:
        raise Exception(f"Error de conexión a S3: {str(e)}")

def get_upload_path(config = Depends(get_settings)):
    """Proporciona la ruta de carga configurada."""
    return config.UPLOAD_FOLDER
