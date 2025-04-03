# Modelado 3D desde Imágenes de iPhone

Esta aplicación web permite crear modelos 3D de personas utilizando imágenes capturadas desde un iPhone 14 Pro.

## Características

- Captura de imágenes desde iPhone 14 Pro
- Procesamiento de imágenes en calidad original
- Generación de modelo 3D basado en 4 vistas (frente, atrás, izquierda, derecha)
<<<<<<< Updated upstream
- Cálculo de dimensiones basado en altura conocida
- Optimizaciones para aprovechar al máximo la capa gratuita de AWS
=======
- Cálculo de dimensiones basado en altura conocida.
>>>>>>> Stashed changes

## Requisitos

- Python 3.12+ (recomendado)
- Cuenta AWS
- iPhone 14 Pro para captura de imágenes

## Configuración

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
Crear archivo `.env` basado en `.env.example` con:
```
# Credenciales de AWS (reemplazar con tus propias credenciales)
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_REGION=us-east-1
S3_BUCKET=nombre_del_bucket

# Configuración de seguridad
SECRET_KEY=clave_secreta_segura_para_produccion
MAINTENANCE_TOKEN=token_seguro_para_tareas_mantenimiento

# Configuración de FastAPI
FASTAPI_ENV=development
FASTAPI_APP=app.main:app
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8080

# Optimizaciones para capa gratuita de AWS
IMG_COMPRESSION_QUALITY=85
S3_AUTO_CLEANUP_ENABLED=TRUE
S3_AUTO_CLEANUP_DAYS=30
S3_REDUCED_REDUNDANCY=TRUE

# Modo de bajo consumo de recursos
LOW_RESOURCE_MODE=TRUE
```

## Uso

1. Iniciar el servidor:
```bash
python run.py
```

2. Acceder a la aplicación web en `http://localhost:8080`
3. Seguir las instrucciones en pantalla para la captura de imágenes

## Estructura del Proyecto

```
app/
├── static/          # Archivos estáticos
├── templates/       # Plantillas HTML
├── __init__.py     # Archivo de inicialización del paquete
├── main.py         # Punto de entrada de la aplicación FastAPI
├── routes.py       # Rutas y endpoints de la API
└── config.py       # Configuración de la aplicación
```

## Optimizaciones para AWS (Capa Gratuita)

La aplicación incluye varias optimizaciones para aprovechar al máximo la capa gratuita de AWS:

1. **Compresión de imágenes**: Las imágenes JPEG se comprimen antes de subirse a S3, manteniendo la resolución pero reduciendo el tamaño de archivo.

2. **Estructura organizada**: Organización por sesiones y procesos para facilitar la limpieza.

3. **Metadatos**: Añadimos metadatos con fechas para controlar la antigüedad de los archivos.

4. **Limpieza automática**: Opción para eliminar archivos antiguos automáticamente, configurable por días.

5. **Clase de almacenamiento**: Uso de `REDUCED_REDUNDANCY` para archivos temporales.

6. **Modo de bajo consumo**: Opción para procesar imágenes a menor resolución.

## Documentación de la API

FastAPI genera automáticamente documentación interactiva de la API:

- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc` 