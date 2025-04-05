import boto3
import os
import logging
from botocore.exceptions import ClientError

from app.config import AWS_REGION, AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# Configurar logging
logger = logging.getLogger(__name__)

def get_s3_client():
    """
    Crea y devuelve un cliente de S3
    
    Returns:
        boto3.client: Cliente S3 configurado
    """
    try:
        s3_client = boto3.client(
            's3',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        return s3_client
    except Exception as e:
        logger.error(f"Error al crear cliente S3: {str(e)}")
        return None

def upload_file_to_s3(file_path, object_name=None):
    """
    Sube un archivo a un bucket de S3
    
    Args:
        file_path: Ruta al archivo a subir
        object_name: Nombre del objeto en S3 (usa file_path si None)
        
    Returns:
        bool: True si la subida fue exitosa, False en caso contrario
    """
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    s3_client = get_s3_client()
    if not s3_client:
        return False
    
    try:
        s3_client.upload_file(file_path, AWS_S3_BUCKET, object_name)
        logger.info(f"Archivo {file_path} subido a S3 como {object_name}")
        return True
    except ClientError as e:
        logger.error(f"Error al subir archivo a S3: {str(e)}")
        return False

def get_s3_file_url(object_name):
    """
    Genera una URL para acceder a un archivo en S3
    
    Args:
        object_name: Nombre del objeto en S3
        
    Returns:
        str: URL del objeto
    """
    s3_client = get_s3_client()
    if not s3_client:
        return None
    
    try:
        # Generar URL prefirmada válida por 1 hora
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': AWS_S3_BUCKET,
                'Key': object_name
            },
            ExpiresIn=3600  # 1 hora
        )
        return url
    except ClientError as e:
        logger.error(f"Error al generar URL para objeto S3: {str(e)}")
        return None
