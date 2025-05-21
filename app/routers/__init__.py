"""
Paquete de enrutadores para la aplicación de análisis de piel.
"""

# Importar routers
try:
    from app.routers import skin_router
    from app.routers import web
    from app.routers import api
except ImportError as e:
    print(f"Error al importar routers: {e}") 