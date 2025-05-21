"""
Router para las rutas web de la aplicación.
"""

from fastapi import APIRouter, Depends, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional
import os
import logging

from app.config import get_settings
from app.core.logger import get_logger
from app.dependencies import verify_optional_api_key, rate_limit

# Configuración
logger = get_logger(__name__)
settings = get_settings()

# Router
router = APIRouter(
    dependencies=[
        Depends(rate_limit),
        Depends(verify_optional_api_key),
    ]
)

# Rutas web
@router.get("/", response_class=HTMLResponse)
async def web_root(request: Request):
    """Ruta principal de la interfaz web."""
    return request.app.state.templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@router.get("/app", response_class=HTMLResponse)
async def app_page(request: Request):
    """Página principal de la aplicación."""
    return request.app.state.templates.TemplateResponse(
        "index.html", 
        {"request": request}
    )

@router.get("/docs-piel", response_class=HTMLResponse)
async def skin_docs(request: Request):
    """Documentación del API de análisis de piel."""
    return request.app.state.templates.TemplateResponse(
        "docs-skin.html",
        {"request": request}
    )

@router.get("/info", response_class=HTMLResponse)
async def info_page(request: Request):
    """Página de información sobre la aplicación."""
    version = settings.APP_VERSION
    return request.app.state.templates.TemplateResponse(
        "info.html",
        {"request": request, "version": version}
    )