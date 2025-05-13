import logging
import sys
import os
from pathlib import Path
from typing import Optional

# Configuración de formato del logger
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Niveles de log
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

# Directorio para logs
LOG_DIR = Path("logs")


def get_logger(name: str, level: int = logging.INFO, log_file: Optional[str] = None) -> logging.Logger:
    """
    Configura y devuelve un logger con el nombre especificado.
    
    Args:
        name: Nombre del logger (normalmente __name__)
        level: Nivel de logging
        log_file: Nombre del archivo de log (opcional)
        
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicación de handlers si el logger ya está configurado
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Formateo de logs
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    
    # Configurar handler para stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Configurar handler para archivo si se especificó
    if log_file:
        # Crear directorio si no existe
        if not LOG_DIR.exists():
            LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(LOG_DIR / log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def setup_global_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """
    Configura la logging global de la aplicación.
    
    Args:
        level: Nivel de logging
        log_file: Nombre del archivo de log (opcional)
    """
    # Configurar root logger
    root_logger = get_logger("root", level, log_file)
    
    # Silenciar loggers muy verbosos
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    root_logger.info("Logging global configurado") 