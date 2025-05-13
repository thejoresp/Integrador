import uvicorn
from app.config import get_settings

if __name__ == "__main__":
    config = get_settings()
    
    # Ejecutar la aplicación con uvicorn directamente como string
    # Esto permite que reload y workers funcionen correctamente
    uvicorn.run(
        "app.main:app",  # Referencia a la aplicación como string de importación
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD,
        log_level=config.LOG_LEVEL.lower(),
        workers=1  # Definimos workers=1 para evitar problemas en desarrollo
    ) 