"""
Utilidades de seguridad para la aplicación
"""
import secrets
import hashlib
import logging
import base64
import hmac
import time
from typing import Dict, Optional, Tuple, Union
from fastapi import Request, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader

# Configurar logger
logger = logging.getLogger(__name__)

# Definir dependencia para API key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def generate_secure_token(length: int = 32) -> str:
    """
    Genera un token seguro de longitud especificada
    
    Args:
        length: Longitud deseada del token
        
    Returns:
        str: Token generado
    """
    return secrets.token_hex(length // 2)

def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """
    Genera un hash seguro para una contraseña
    
    Args:
        password: Contraseña a hashear
        salt: Sal para el hash (generada si es None)
        
    Returns:
        Tuple[str, str]: (hash, salt)
    """
    if not salt:
        salt = secrets.token_hex(16)
        
    # Usar una función de derivación de clave
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # Iteraciones
    )
    
    # Convertir a hexadecimal
    key_hex = key.hex()
    
    return key_hex, salt

def verify_password(stored_hash: str, salt: str, provided_password: str) -> bool:
    """
    Verifica si una contraseña coincide con el hash almacenado
    
    Args:
        stored_hash: Hash almacenado
        salt: Sal usada en el hash
        provided_password: Contraseña proporcionada a verificar
        
    Returns:
        bool: True si coincide, False en caso contrario
    """
    # Generar hash con la misma sal
    new_hash, _ = hash_password(provided_password, salt)
    
    # Comparación resistente a timing attacks
    return hmac.compare_digest(stored_hash, new_hash)

def generate_timed_token(data: Dict, secret_key: str, expiration_minutes: int = 30) -> str:
    """
    Genera un token temporal con datos codificados
    
    Args:
        data: Datos a codificar en el token
        secret_key: Clave secreta para firmar
        expiration_minutes: Tiempo de validez en minutos
        
    Returns:
        str: Token firmado y codificado
    """
    # Añadir timestamp de expiración
    expiration_time = int(time.time()) + (expiration_minutes * 60)
    payload = {**data, "exp": expiration_time}
    
    # Serializar y codificar
    import json
    payload_bytes = json.dumps(payload).encode('utf-8')
    payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode('utf-8').rstrip('=')
    
    # Firmar
    signature = hmac.new(
        secret_key.encode('utf-8'),
        payload_b64.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
    
    # Combinar
    return f"{payload_b64}.{signature_b64}"

def verify_timed_token(token: str, secret_key: str) -> Optional[Dict]:
    """
    Verifica y decodifica un token temporal
    
    Args:
        token: Token a verificar
        secret_key: Clave secreta para verificar firma
        
    Returns:
        Optional[Dict]: Datos decodificados si el token es válido, None si no
    """
    try:
        # Separar payload y firma
        payload_b64, signature_b64 = token.split('.')
        
        # Reconstruir padding
        payload_b64_padded = payload_b64 + '=' * (4 - len(payload_b64) % 4)
        signature_b64_padded = signature_b64 + '=' * (4 - len(signature_b64) % 4)
        
        # Verificar firma
        expected_signature = hmac.new(
            secret_key.encode('utf-8'),
            payload_b64.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        
        actual_signature = base64.urlsafe_b64decode(signature_b64_padded)
        
        if not hmac.compare_digest(expected_signature, actual_signature):
            logger.warning("Firma de token inválida")
            return None
        
        # Decodificar payload
        import json
        payload_bytes = base64.urlsafe_b64decode(payload_b64_padded)
        payload = json.loads(payload_bytes)
        
        # Verificar expiración
        if time.time() > payload.get('exp', 0):
            logger.warning("Token expirado")
            return None
            
        # Eliminar campo exp
        if 'exp' in payload:
            del payload['exp']
            
        return payload
    except Exception as e:
        logger.error(f"Error al verificar token: {str(e)}")
        return None

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verifica una API key para autorizar acceso a endpoints protegidos
    
    Args:
        api_key: API key del header
        
    Returns:
        str: API key verificada
        
    Raises:
        HTTPException: Si la API key es inválida o está ausente
    """
    from app.config import Config
    config = Config()
    
    # Verificar que se proporcionó una API key
    if not api_key:
        logger.warning("Intento de acceso sin API key")
        raise HTTPException(
            status_code=401,
            detail="API key requerida",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    # En un entorno real, verificaríamos contra una BD
    # Aquí solo verificamos contra config (para demo)
    valid_keys = [
        config.MAIN_API_KEY,
        config.SECONDARY_API_KEY
    ]
    
    if api_key not in valid_keys:
        logger.warning("Intento de acceso con API key inválida")
        raise HTTPException(
            status_code=403,
            detail="API key inválida",
            headers={"WWW-Authenticate": "ApiKey"},
        )
        
    return api_key

async def get_request_client_info(request: Request) -> Dict[str, str]:
    """
    Obtiene información del cliente que realizó la solicitud
    
    Args:
        request: Objeto de solicitud HTTP
        
    Returns:
        Dict: Información del cliente
    """
    headers = dict(request.headers)
    client_info = {
        "ip": request.client.host if request.client else "unknown",
        "user_agent": headers.get("user-agent", "unknown"),
        "referer": headers.get("referer", "direct"),
        "forwarded_for": headers.get("x-forwarded-for", None)
    }
    
    return client_info
