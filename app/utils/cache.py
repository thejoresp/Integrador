"""
Sistema de caché simple para resultados de análisis y operaciones costosas
"""
import time
import logging
import threading
from typing import Dict, Any, Optional, Callable, TypeVar, Tuple

# Configurar logger
logger = logging.getLogger(__name__)

# Tipos genéricos para caché
T = TypeVar('T')
CacheKey = str
CacheValue = Tuple[T, float]  # (valor, timestamp)

class SimpleCache:
    """Implementación sencilla de caché en memoria con TTL"""
    
    def __init__(self, ttl_seconds: int = 300):
        """
        Inicializa un nuevo caché
        
        Args:
            ttl_seconds: Tiempo de vida para entradas del caché en segundos
        """
        self._cache: Dict[CacheKey, CacheValue] = {}
        self._ttl_seconds = ttl_seconds
        self._lock = threading.RLock()
        
        # Iniciar limpieza periódica
        self._start_cleanup_thread()
    
    def get(self, key: CacheKey) -> Optional[T]:
        """
        Obtiene un valor del caché si existe y no ha expirado
        
        Args:
            key: Clave a buscar
            
        Returns:
            El valor almacenado o None si no existe o expiró
        """
        with self._lock:
            if key not in self._cache:
                return None
                
            value, timestamp = self._cache[key]
            
            # Verificar si ha expirado
            if time.time() - timestamp > self._ttl_seconds:
                # Expirado, eliminar
                del self._cache[key]
                return None
                
            return value
    
    def set(self, key: CacheKey, value: T) -> None:
        """
        Almacena un valor en caché
        
        Args:
            key: Clave para almacenar
            value: Valor a almacenar
        """
        with self._lock:
            self._cache[key] = (value, time.time())
    
    def invalidate(self, key: CacheKey) -> bool:
        """
        Invalida una entrada del caché
        
        Args:
            key: Clave a invalidar
            
        Returns:
            bool: True si la clave existía, False si no
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Limpia todo el caché"""
        with self._lock:
            self._cache.clear()
    
    def _cleanup_expired(self) -> int:
        """
        Elimina entradas expiradas del caché
        
        Returns:
            int: Número de entradas eliminadas
        """
        now = time.time()
        expired_keys = []
        
        with self._lock:
            # Identificar claves expiradas
            for key, (_, timestamp) in self._cache.items():
                if now - timestamp > self._ttl_seconds:
                    expired_keys.append(key)
            
            # Eliminar claves expiradas
            for key in expired_keys:
                del self._cache[key]
                
        return len(expired_keys)
    
    def _start_cleanup_thread(self) -> None:
        """Inicia un thread para limpieza periódica"""
        def cleanup_job():
            while True:
                time.sleep(self._ttl_seconds / 2)  # Ejecutar cada mitad del TTL
                try:
                    removed = self._cleanup_expired()
                    if removed > 0:
                        logger.debug(f"Caché: {removed} entradas expiradas eliminadas")
                except Exception as e:
                    logger.error(f"Error en limpieza de caché: {str(e)}")
        
        # Iniciar thread de limpieza como daemon
        cleanup_thread = threading.Thread(target=cleanup_job, daemon=True)
        cleanup_thread.start()

# Instancia global del caché para análisis faciales
analysis_cache = SimpleCache(ttl_seconds=600)  # 10 minutos

def cached(ttl_seconds: int = 300):
    """
    Decorador para cachear resultados de funciones costosas
    
    Args:
        ttl_seconds: Tiempo de vida en segundos para la entrada en caché
        
    Returns:
        Callable: Decorador configurado
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        # Crear caché específico para esta función
        func_cache = SimpleCache(ttl_seconds=ttl_seconds)
        
        def wrapper(*args, **kwargs):
            # Generar clave de caché única basada en argumentos
            cache_key = f"{func.__name__}:{hash(str(args))}-{hash(str(kwargs))}"
            
            # Intentar obtener del caché
            cached_result = func_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
                
            # Ejecutar función original
            result = func(*args, **kwargs)
            
            # Almacenar en caché
            func_cache.set(cache_key, result)
            
            return result
        
        return wrapper
    
    return decorator

async def get_cached_analysis(image_hash: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene resultados de análisis facial cacheados por hash de imagen
    
    Args:
        image_hash: Hash único de la imagen
        
    Returns:
        Dict o None: Resultados del análisis si existen en caché
    """
    return analysis_cache.get(f"analysis:{image_hash}")

async def cache_analysis_results(image_hash: str, results: Dict[str, Any]) -> None:
    """
    Almacena resultados de análisis facial en caché
    
    Args:
        image_hash: Hash único de la imagen
        results: Resultados del análisis
    """
    analysis_cache.set(f"analysis:{image_hash}", results)
