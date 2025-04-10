# Sistema de Análisis Facial y Emocional

Sistema de análisis facial y emocional que integra múltiples tecnologías para proporcionar análisis detallados de rostros en imágenes.

## Características

- Detección facial avanzada
- Análisis de edad y género
- Análisis de emociones
- Detección de accesorios (gafas, máscaras)
- Integración con AWS S3
- API RESTful con FastAPI
- Interfaz web moderna

## Requisitos del Sistema

### Dependencias del Sistema
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y build-essential cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev
```

### Python 3.9
El proyecto está optimizado para Python 3.9. Se recomienda usar esta versión específica.

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_DIRECTORIO]
```

2. Crear y activar entorno virtual:
```bash
python3.9 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuración

1. Crear archivo `.env` en la raíz del proyecto:
```bash
cp .env.example .env
```

2. Configurar las variables de entorno en `.env`:
```env
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_REGION=tu_region
S3_BUCKET=nombre_del_bucket
```

## Ejecución

1. Iniciar el servidor:
```bash
python run.py
```

El servidor estará disponible en:
- API: http://localhost:8080
- Documentación API: http://localhost:8080/docs

## Estructura del Proyecto

```
.
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── run.py
```

## Notas Importantes

- El sistema utiliza CPU para el procesamiento de TensorFlow. Los mensajes sobre CUDA son normales si no tienes una GPU NVIDIA.
- DeepFace se ha reemplazado por alternativas más robustas para el análisis de edad, género y emociones.
- La aplicación está optimizada para ejecutarse en modo desarrollo con recarga automática.

## Tecnologías Principales

- FastAPI: Framework web moderno y rápido
- TensorFlow: Motor de inferencia para modelos de ML
- OpenCV: Procesamiento de imágenes
- MediaPipe: Detección facial y análisis
- Boto3: Integración con AWS S3
- Pydantic: Validación de datos
- Uvicorn: Servidor ASGI

## Desarrollo

Para desarrollo local:
```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest
```

## Licencia

[Especificar la licencia]