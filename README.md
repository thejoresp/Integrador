# Analizador Facial con FastAPI

PrompCara es una aplicación web que utiliza FastAPI para analizar rostros mediante técnicas de visión por computadora y deep learning. Proporciona información detallada sobre diversos aspectos faciales como piel, emociones, edad aparente, y más.

## Características

- Análisis de estado de la piel (hidratación, textura, poros)
- Detección de emociones faciales
- Estimación de edad y género aparente
- Análisis de simetría facial
- Detección de fatiga ocular
- Análisis de salud basado en características faciales
- Interfaz web sencilla para subir imágenes y visualizar resultados

## Requisitos

- Python 3.8+
- FastAPI
- OpenCV
- NumPy
- Boto3 (para integración con AWS S3)
- Otras dependencias listadas en `requirements.txt`

## Configuración

1. Clona este repositorio:
```bash
git clone <repo-url>
cd PrompCara
```

2. Crea un entorno virtual y actívalo:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno para AWS (opcional si usas S3):
```bash
export AWS_ACCESS_KEY_ID=tu_access_key
export AWS_SECRET_ACCESS_KEY=tu_secret_key
export S3_BUCKET=nombre_de_tu_bucket
```

## Ejecución

Para iniciar la aplicación en modo desarrollo:

```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en `http://localhost:8000`

## Estructura del Proyecto

- `app/` - Código principal de la aplicación
  - `main.py` - Punto de entrada de FastAPI
  - `analyzers/` - Módulos para análisis facial
  - `aws/` - Integración con servicios AWS
  - `schemas/` - Modelos Pydantic
  - `utils/` - Utilidades para procesamiento
- `static/` - Archivos estáticos (CSS, JS)
- `templates/` - Plantillas HTML
- `uploads/` - Directorio temporal para imágenes subidas

## Despliegue

Para desplegar en AWS:

1. Crea una instancia EC2 t2.micro (capa gratuita)
2. Configura un bucket S3 para almacenamiento
3. Configura las variables de entorno necesarias
4. Instala las dependencias y ejecuta la aplicación con Gunicorn:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## Desarrollo Futuro

- Implementación de modelos más avanzados para detección de características
- Soporte para análisis en tiempo real con cámara web
- Generación de reportes descargables en PDF
- Personalización de análisis según preferencias del usuario