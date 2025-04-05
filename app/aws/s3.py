import logging
import boto3
from botocore.exceptions import ClientError
from app.config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET

def get_s3_client():
    """Retorna un cliente de S3"""
    return boto3.client(
        's3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

def upload_file(file_path, s3_key):
    """
    Sube un archivo a S3
    
    Args:
        file_path: Ruta local del archivo
        s3_key: Ruta donde se guardará en S3
    
    Returns:
        bool: True si se subió correctamente, False en caso contrario
    """
    try:
        s3_client = get_s3_client()
        s3_client.upload_file(file_path, S3_BUCKET, s3_key)
        return True
    except ClientError as e:
        logging.error(f"Error subiendo archivo a S3: {str(e)}")
        return False

def get_file_url(s3_key, expiration=3600):
    """
    Genera una URL prefirmada para un objeto en S3
    
    Args:
        s3_key: Clave del objeto en S3
        expiration: Tiempo de expiración en segundos
    
    Returns:
        str: URL prefirmada
    """
    try:
        s3_client = get_s3_client()
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': s3_key},
            ExpiresIn=expiration
        )
        return url
    except ClientError as e:
        logging.error(f"Error generando URL para {s3_key}: {str(e)}")
        return None
