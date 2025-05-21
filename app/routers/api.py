"""
Router para las rutas de API de la aplicación.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from app.dependencies import verify_optional_api_key, rate_limit
from app.core.logger import get_logger

# Configuración
logger = get_logger(__name__)

# Router
router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
    dependencies=[
        Depends(rate_limit),
        Depends(verify_optional_api_key),
    ]
)

# Rutas de API
@router.get("/status")
async def api_status() -> Dict[str, Any]:
    """Estado de la API."""
    return {
        "status": "operational",
        "message": "Sistema de análisis de piel operativo"
    }