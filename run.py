import uvicorn
from app.config import get_settings

if __name__ == "__main__":
    config = get_settings()
    # Configuración para desarrollo local
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",  # Solo accesible localmente
        port=8000,
        reload=True,
        log_level="info"
    ) 