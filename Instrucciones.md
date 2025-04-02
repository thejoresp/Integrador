# Modelado 3D desde Imágenes de iPhone

Esta aplicación web permite crear modelos 3D de personas utilizando imágenes capturadas desde un iPhone 14 Pro.

## Características

- Captura de imágenes desde iPhone 14 Pro
- Procesamiento de imágenes en calidad original
- Generación de modelo 3D basado en 4 vistas (frente, atrás, izquierda, derecha)
- Cálculo de dimensiones basado en altura conocida

## Requisitos

- Python 3.8+
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
Crear archivo `.env` con:
```
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_REGION=tu_region
S3_BUCKET=nombre_del_bucket
```

## Uso

1. Iniciar el servidor:
```bash
python run.py
```

2. Acceder a la aplicación web en `http://localhost:5000`
3. Seguir las instrucciones en pantalla para la captura de imágenes

## Estructura del Proyecto

```
app/
├── static/          # Archivos estáticos
├── templates/       # Plantillas HTML
├── utils/          # Utilidades y helpers
├── __init__.py     # Inicialización de la aplicación
├── routes.py       # Rutas de la aplicación
└── config.py       # Configuración
``` 