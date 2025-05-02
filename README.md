# Sistema de Análisis Facial

## Descripción
Sistema avanzado de análisis facial y emocional que integra múltiples tecnologías para proporcionar análisis detallados de rostros en imágenes. El sistema utiliza técnicas de visión por computadora y aprendizaje profundo para detectar y analizar características faciales, emociones y atributos demográficos en tiempo real.

## Características Principales

### Análisis Facial
- Detección facial de alta precisión
- Análisis de múltiples rostros simultáneos
- Detección de orientación facial
- Estimación de puntos faciales clave

### Análisis Demográfico
- Estimación de edad con alta precisión
- Detección de género
- Análisis de etnia
- Estimación de expresión facial

### Análisis Emocional
- Detección de 7 emociones básicas:
  - Felicidad
  - Tristeza
  - Enojo
  - Sorpresa
  - Miedo
  - Disgusto
  - Neutral
- Análisis de intensidad emocional
- Seguimiento temporal de emociones

### Características Técnicas
- API RESTful con FastAPI
- Almacenamiento local de imágenes
- Interfaz web moderna y responsiva
- Procesamiento en tiempo real
- Soporte para múltiples formatos de imagen

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
│   ├── analyzers/      # Módulos de análisis facial
│   ├── models/         # Modelos de datos
│   ├── routers/        # Rutas de la API
│   ├── schemas/        # Esquemas de datos
│   ├── services/       # Servicios
│   ├── utils/          # Utilidades
│   ├── config.py       # Configuración
│   └── main.py         # Punto de entrada de FastAPI
├── models/
│   └── pretrained/     # Modelos pre-entrenados
├── static/             # Archivos estáticos
│   ├── css/
│   └── js/
├── templates/          # Plantillas HTML
├── uploads/            # Directorio para archivos subidos
├── .gitignore          # Archivos ignorados por git
├── requirements.txt    # Dependencias
└── run.py              # Script para ejecutar la aplicación
```

## Tecnologías Principales

- **FastAPI**: Framework web moderno y rápido
- **TensorFlow**: Motor de inferencia para modelos de ML
- **OpenCV**: Procesamiento de imágenes
- **MediaPipe**: Detección facial y análisis
- **Face Recognition**: Análisis facial de alta precisión
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

## Endpoints API

### Análisis Facial
```
POST /analyze
```
Acepta una imagen y devuelve análisis detallado que incluye:
- Edad y género
- Emociones detectadas
- Estado de la piel
- Indicadores de salud basados en la apariencia facial