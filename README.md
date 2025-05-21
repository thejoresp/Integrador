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
- API RESTful con **FastAPI** 
- Almacenamiento local de imágenes
- Interfaz web moderna y responsiva
- Procesamiento en tiempo real
- Soporte para múltiples formatos de imagen

## Requisitos del Sistema

### Dependencias del Sistema

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev python3.10 python3.10-dev python3.10-venv
```

#### CentOS/RHEL/Fedora
```bash
sudo dnf install -y gcc gcc-c++ cmake make pkgconfig libX11-devel atlas-devel gtk3-devel boost-devel boost-python3-devel python3.10 python3.10-devel
```

#### Arch Linux
```bash
sudo pacman -Syu
sudo pacman -S base-devel cmake pkg-config libx11 atlas gtk3 boost boost-libs python python-pip
```

#### macOS
```bash
# Instalar Homebrew si no está instalado
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias
brew update
brew install cmake pkg-config boost boost-python3
brew install opencv

# Instalar Python 3.10
brew install python@3.10

# Para instalar dlib correctamente
brew install cmake
```

#### Windows
1. Instalar Visual Studio Build Tools (incluye C++ build tools)
   - Descargar desde: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Durante la instalación, seleccionar "Desarrollo para escritorio con C++"

2. Instalar Python 3.10
   - Descargar desde: https://www.python.org/downloads/release/python-31011/
   - Asegurarse de marcar la opción "Add Python to PATH" durante la instalación

3. Instalar CMake
   - Descargar desde: https://cmake.org/download/
   - Asegurarse de agregar CMake al PATH del sistema

4. PowerShell (Administrador):
```powershell
# Instalar chocolatey (opcional pero recomendado)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Con chocolatey instalado:
choco install cmake -y
```

### Python 3.10
El proyecto está optimizado para Python 3.10. Se recomienda usar esta versión específica.

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_DIRECTORIO]
```

2. Crear y activar entorno virtual:

**Ubuntu/Debian:**
```bash
python3.10 -m venv venv
source venv/bin/activate
```

**macOS:**
```bash
python3.10 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
py -3.10 -m venv venv
venv\Scripts\activate
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

### Análisis de Piel

#### Análisis de condición de piel

```python
import requests

url = "http://localhost:8080/skin/analyze/condition"
files = {"file": open("ruta/a/imagen.jpg", "rb")}
response = requests.post(url, files=files)
result = response.json()

print(f"Hidratación: {result['hydration']}")
print(f"Textura: {result['texture']}")
print(f"Poros: {result['pores']}")
print(f"Grasa: {result['oiliness']}")
```

#### Análisis de lunares

```python
import requests

url = "http://localhost:8080/skin/analyze/moles"
files = {"file": open("ruta/a/imagen.jpg", "rb")}
response = requests.post(url, files=files)
result = response.json()

print(f"Total de lunares: {result['total_count']}")
print(f"Lunares benignos: {result['benign_count']}")
print(f"Lunares sospechosos: {result['suspicious_count']}")
```

#### Análisis de tono de piel

```python
import requests

url = "http://localhost:8080/skin/analyze/tone"
files = {"file": open("ruta/a/imagen.jpg", "rb")}
response = requests.post(url, files=files)
result = response.json()

print(f"Tipo Fitzpatrick: {result['fitzpatrick_type']}")
print(f"Tono: {result['tone_name']}")
```

#### Análisis completo

```python
import requests

url = "http://localhost:8080/skin/analyze/complete"
files = {"file": open("ruta/a/imagen.jpg", "rb")}
response = requests.post(url, files=files)
result = response.json()

# Acceder a los diferentes componentes del análisis
skin_condition = result['skin_condition']
mole_analysis = result['mole_analysis']
skin_tone = result['skin_tone']
```

#### Obtener recomendaciones

```python
import requests

url = "http://localhost:8080/skin/recommendations"
params = {
    "hydration": 70,
    "texture": 60,
    "pores": 80,
    "fitzpatrick_type": 3,
    "has_suspicious_moles": True
}
response = requests.get(url, params=params)
recommendations = response.json()

for rec in recommendations:
    print(f"- {rec}")
```