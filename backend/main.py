from fastapi import FastAPI
import uvicorn
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from backend.controllers import skin

# Cargar variables de entorno del archivo .env
# Es bueno hacerlo lo antes posible
load_dotenv()

# Opcional: Verificar si el token se cargó (para depuración)
# print(f"HF_TOKEN desde el entorno: {os.getenv('HF_TOKEN')}")

# Crear la instancia de la aplicación FastAPI
app = FastAPI(
    title="PielSana IA",
    description="Sistema de análisis facial para clasificar condiciones cutáneas.",
    version="0.1.0"
)

# Habilitar CORS para el frontend en desarrollo y producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",            # Para desarrollo local
        "http://127.0.0.1:5173",
        "https://pielsana-ia.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.ngrok-free\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de prueba
@app.get("/")
async def read_root():
    # Redirigir a la página de carga de la aplicación de piel
    return RedirectResponse(url="/skin/")

# Registrar routers de los controladores
app.include_router(skin.router, prefix="/skin", tags=["Skin Analysis Frontend"])

if __name__ == "__main__":
    # Esta sección es útil para desarrollo, pero para producción usarás 'run.py'
    uvicorn.run(app, host="0.0.0.0", port=8080) 