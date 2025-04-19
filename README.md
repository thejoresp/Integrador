# Sistema de Análisis Facial y Emocional

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

### Análisis de Accesorios
- Detección de gafas
- Detección de máscaras faciales
- Detección de otros accesorios faciales

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
- Integración con AWS S3 para almacenamiento
- Interfaz web moderna y responsiva
- Procesamiento en tiempo real
- Soporte para múltiples formatos de imagen
- Escalabilidad horizontal

## Requisitos del Sistema

### Requisitos para Desarrollo Local
- CPU: Intel Core i5 o equivalente
- RAM: 8GB mínimo
- Almacenamiento: 20GB de espacio libre
- Conexión a Internet para servicios en la nube

### Requisitos para Producción (AWS)
- **Desarrollo/Pruebas**:
  - EC2 t3.medium (2 vCPU, 4GB RAM)
  - Almacenamiento: 20GB SSD
  - Sin GPU requerida

- **Producción**:
  - EC2 t3.large (2 vCPU, 8GB RAM)
  - Almacenamiento: 50GB SSD
  - Sin GPU requerida (procesamiento distribuido)

- **Alta Demanda**:
  - Auto-scaling entre t3.large y t3.xlarge
  - Load Balancer para distribución de carga
  - CloudFront para CDN

### Dependencias del Sistema

#### Windows 11
```powershell
# 1. Instalar Visual Studio Build Tools 2019 o posterior
# Descargar desde: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Durante la instalación, seleccionar:
#   - "C++ build tools"
#   - "Windows 10 SDK"
#   - "MSVC v142 - VS 2019 C++ x64/x86 build tools"

# 2. Instalar CMake
# Descargar desde: https://cmake.org/download/
# Asegurarse de marcar "Add CMake to the system PATH" durante la instalación

# 3. Instalar Python 3.10 desde python.org
# Asegurarse de marcar "Add Python to PATH" durante la instalación

# 4. Reiniciar el sistema después de la instalación
```

#### Ubuntu/Debian
```bash
# Actualizar repositorios
sudo apt-get update

# Instalar dependencias del sistema
sudo apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libx11-dev \
    libatlas-base-dev \
    libgtk-3-dev \
    libboost-python-dev \
    python3.10 \
    python3.10-dev \
    python3.10-venv
```

#### macOS
```bash
# Instalar Homebrew si no está instalado
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias
brew install cmake pkg-config
brew install python@3.10
```

### Python 3.10
El proyecto ha sido actualizado para usar Python 3.10. Se recomienda usar esta versión específica para garantizar la compatibilidad con todas las dependencias.

## Estructura del Proyecto
```
proyecto/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   └── facial_analysis.py
│   ├── services/
│   │   ├── aws_service.py
│   │   └── facial_service.py
│   └── utils/
│       └── image_processing.py
├── tests/
│   └── test_facial_analysis.py
├── static/
│   └── assets/
├── templates/
│   └── index.html
├── requirements.txt
├── config.yaml
└── README.md
```

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_DIRECTORIO]
```

2. Crear y activar entorno virtual:

#### Windows 11
```powershell
# IMPORTANTE: Asegúrate de tener Python 3.10 instalado
# Si tienes múltiples versiones de Python, usa específicamente:
py -3.10 -m venv venv
.\venv\Scripts\activate
```

#### Ubuntu/Debian
```bash
# Si necesitas instalar Python 3.10:
# sudo apt update
# sudo apt install python3.10 python3.10-venv python3.10-dev

python3.10 -m venv venv
source venv/bin/activate
```

#### macOS
```bash
# Si necesitas instalar Python 3.10 con Homebrew:
# brew install python@3.10

python3.10 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuración

### Configuración de AWS
1. Crear una cuenta en AWS si no existe
2. Crear un usuario IAM con acceso programático
3. Configurar las credenciales:
```bash
aws configure
```
4. Crear un bucket S3 para almacenamiento
5. Actualizar `config.yaml` con las credenciales:
```yaml
aws:
  access_key_id: TU_ACCESS_KEY
  secret_access_key: TU_SECRET_KEY
  region: tu-region
  bucket: nombre-del-bucket
```

### Configuración de la Aplicación
1. Copiar `config.yaml.example` a `config.yaml`
2. Ajustar los parámetros según necesidad:
```yaml
app:
  host: 0.0.0.0
  port: 8000
  debug: false

facial_analysis:
  confidence_threshold: 0.8
  max_faces: 10
  emotion_threshold: 0.6
```

## Uso

### Iniciar el Servidor
```bash
# Desarrollo
uvicorn app.main:app --reload

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

#### Análisis Facial
```bash
POST /api/v1/analyze
Content-Type: multipart/form-data

# Parámetros
- image: archivo de imagen
- options: JSON con opciones de análisis
```

#### Resultados
```json
{
  "faces": [
    {
      "age": 25,
      "gender": "male",
      "emotions": {
        "happy": 0.8,
        "neutral": 0.2
      },
      "accessories": ["glasses"]
    }
  ]
}
```

## Optimización para AWS

### Configuración de EC2
- Tipo de instancia recomendado: t3.large
- AMI: Ubuntu Server 20.04 LTS
- Almacenamiento: 50GB SSD
- Puertos abiertos: 80, 443, 8000

### Auto Scaling
```yaml
AutoScalingGroup:
  MinSize: 2
  MaxSize: 10
  DesiredCapacity: 4
  HealthCheckType: ELB
  HealthCheckGracePeriod: 300
```

### Load Balancer
- Tipo: Application Load Balancer
- Protocolo: HTTPS
- Certificado SSL: ACM
- Health Check Path: /health

### Monitoreo
- CloudWatch Metrics
- Logs centralizados
- Alertas automáticas

## Mantenimiento

### Actualizaciones
```bash
git pull origin main
pip install -r requirements.txt
```

### Backup
- Backup automático diario de la base de datos
- Backup semanal de configuraciones
- Retención de 30 días

### Monitoreo
- Uptime monitoring
- Error tracking
- Performance metrics

## Soporte

### Documentación
- API Documentation: `/docs`
- Swagger UI: `/swagger`
- ReDoc: `/redoc`

### Contacto
- Email: soporte@ejemplo.com
- Issues: GitHub Issues
- Wiki: [Link al Wiki]