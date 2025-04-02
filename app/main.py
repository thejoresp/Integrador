from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import boto3
from botocore.config import Config as BotoConfig
from .config import Config
from .routes import router

# Inicializar configuración
config = Config()

# Crear aplicación FastAPI
app = FastAPI(title="Modelado 3D", description="API para modelado 3D a partir de imágenes")

# Asegurar directorios necesarios
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(config.TEMP_DIR, exist_ok=True)

# Verificar si las credenciales de AWS están configuradas
use_mock_s3 = not all([config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY, config.S3_BUCKET])

if use_mock_s3:
    # Crear cliente S3 simulado para desarrollo local
    print("AVISO: Usando cliente S3 simulado para desarrollo local")
    class MockS3Client:
        def upload_file(self, *args, **kwargs):
            print(f"Mock S3: Simulando carga de archivo")
            return True
    s3_client = MockS3Client()
else:
    # Configuración optimizada para AWS
    boto_config = BotoConfig(
        retries={'max_attempts': 2, 'mode': 'standard'},
        region_name=config.AWS_REGION,
        s3={'addressing_style': 'path'}
    )

    # Inicializar cliente S3 real
    s3_client = boto3.client(
        's3',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION,
        config=boto_config
    )

# Configurar plantillas
templates = Jinja2Templates(directory="app/templates")

# Montar archivos estáticos si existe el directorio
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Middleware para inyectar dependencias en el estado de la app
@app.middleware("http")
async def add_state(request: Request, call_next):
    request.app.state.config = config
    request.app.state.s3 = s3_client
    request.app.state.templates = templates
    request.app.state.dev_mode = use_mock_s3
    response = await call_next(request)
    return response

# Incluir rutas
app.include_router(router)