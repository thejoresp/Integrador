# PielSana IA

## Resumen
PielSana IA es un sistema de análisis facial que utiliza el modelo Derm Foundation de Google y otros modelos adicionales para analizar imágenes faciales y clasificar condiciones cutáneas. El sistema genera embeddings de 6144 dimensiones a partir de imágenes faciales y captura características densas relevantes para su análisis.

## Descripción
PielSana IA se basa en el modelo Derm Foundation, un modelo de aprendizaje automático pre-entrenado para acelerar el desarrollo de IA en aplicaciones dermatológicas. Además, se incorporarán otros modelos para mejorar la funcionalidad y precisión del análisis. El sistema genera embeddings de 6144 dimensiones a partir de imágenes faciales y captura características densas relevantes para su análisis.

## Características Principales

### Análisis de Imágenes Faciales
- Generación de embeddings de 6144 dimensiones
- Captura de características densas relevantes
- Entrenamiento eficiente de modelos de IA
- Requiere significativamente menos datos y computación

### Aplicaciones
- Clasificación de condiciones cutáneas (psoriasis, melanoma, dermatitis)
- Puntuación de severidad o progresión de condiciones cutáneas
- Identificación de partes del rostro
- Determinación de calidad de imagen para evaluación dermatológica

### Características Técnicas
- Modelos utilizados: Derm Foundation, otros modelos adicionales
- Entrada: Imagen PNG de 448 x 448 píxeles
- Salida: Vector de embedding de 6144 dimensiones
- Entrenado con JAX para aprovechar hardware de última generación
- Backend: FastAPI con arquitectura MVC
- Modularidad: Cada modelo se encapsula en su propio módulo para facilitar el manejo y extensión

## Estructura del Proyecto (MVC)

```
.
├── app/
│   ├── models/              # Capa de Modelo
│   │   ├── __init__.py
│   │   ├── base.py          # Modelo base abstracto
│   │   ├── derm_foundation/ # Módulo para el modelo Derm Foundation
│   │   │   ├── __init__.py
│   │   │   ├── model.py     # Implementación del modelo Derm Foundation
│   │   │   └── config.py    # Configuración específica del modelo
│   │   ├── model1/          # Módulo para otro modelo adicional
│   │   │   ├── __init__.py
│   │   │   ├── model.py     # Implementación del modelo1
│   │   │   └── config.py    # Configuración específica del modelo1
│   │   └── model2/          # Módulo para otro modelo adicional
│   │       ├── __init__.py
│   │       ├── model.py     # Implementación del modelo2
│   │       └── config.py    # Configuración específica del modelo2
│   │
│   ├── views/               # Capa de Vista
│   │   ├── __init__.py
│   │   ├── templates/       # Plantillas HTML
│   │   │   ├── upload.html  # Página para cargar la imagen
│   │   │   └── results.html # Página para mostrar los resultados
│   │   └── static/          # Archivos estáticos
│   │       ├── css/
│   │       │   ├── upload.css # Estilos para la página de carga
│   │       │   └── results.css # Estilos para la página de resultados
│   │       └── js/
│   │           ├── upload.js  # Scripts para la página de carga
│   │           └── results.js # Scripts para la página de resultados
│   │
│   ├── controllers/         # Capa de Controlador
│   │   ├── __init__.py
│   │   ├── skin.py          # Controladores de análisis de piel
│   │   └── base.py          # Controlador base abstracto
│   │
│   ├── services/            # Servicios de negocio
│   │   ├── __init__.py
│   │   ├── skin_service.py  # Lógica de negocio
│   │   └── base.py          # Servicio base abstracto
│   │
│   ├── config/              # Configuración
│   │   ├── __init__.py
│   │   ├── settings.py      # Configuraciones de la aplicación
│   │   └── logging.py       # Configuración de logging
│   │
│   ├── utils/               # Utilidades
│   │   ├── __init__.py
│   │   ├── helpers.py       # Funciones auxiliares
│   │   └── image_utils.py   # Utilidades para procesamiento de imágenes
│   │
│   └── main.py              # Punto de entrada de FastAPI
│
├── tests/                   # Pruebas
│   ├── __init__.py
│   ├── models/              # Pruebas para modelos
│   │   ├── test_derm_foundation.py
│   │   ├── test_model1.py
│   │   └── test_model2.py
│   ├── controllers/         # Pruebas para controladores
│   │   └── test_skin.py
│   ├── services/            # Pruebas para servicios
│   │   └── test_skin_service.py
│   └── utils/               # Pruebas para utilidades
│       └── test_helpers.py
│
├── data/                    # Datos (imágenes de ejemplo, datasets pequeños, etc.)
│   └── sample_images/
├── docs/                    # Documentación adicional
│   └── architecture.md
├── scripts/                 # Scripts de utilidad (ej. preprocesamiento, tareas de mantenimiento)
│   └── preprocess_data.py
│
├── .env                     # Variables de entorno
├── .gitignore               # Archivos ignorados por git
├── requirements.txt         # Dependencias
├── run.py                   # Script para ejecutar la aplicación
├── Dockerfile               # Para construir la imagen Docker de la aplicación
├── docker-compose.yml       # Para orquestación de contenedores Docker (opcional)
├── LICENSE                  # Archivo de licencia del proyecto
└── .github/                 # Configuración de GitHub (ej. workflows para CI/CD)
    └── workflows/
        └── main.yml
```

## Requisitos del Sistema

### Dependencias del Sistema

#### Ubuntu
```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev python3.10 python3.10-dev python3.10-venv
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

## Instalación

1. Crear y activar entorno virtual:

**Ubuntu:**
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

2. Instalar dependencias:
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

## Ejemplo de Uso

```python
from PIL import Image
from io import BytesIO
from huggingface_hub import from_pretrained_keras
import tensorflow as tf

# Cargar la imagen
img = Image.open("imagen.png")
buf = BytesIO()
img.convert('RGB').save(buf, 'PNG')
image_bytes = buf.getvalue()

# Formatear entrada
input_tensor = tf.train.Example(features=tf.train.Features(
    feature={'image/encoded': tf.train.Feature(
        bytes_list=tf.train.BytesList(value=[image_bytes]))
    })).SerializeToString()

# Cargar el modelo desde Hugging Face Hub
loaded_model = from_pretrained_keras("google/derm-foundation")

# Realizar inferencia
infer = loaded_model.signatures["serving_default"]
output = infer(inputs=tf.constant([input_tensor]))

# Extraer el vector de embedding
embedding_vector = output['embedding'].numpy().flatten()
```

## Limitaciones

- La calidad puede degradarse en condiciones extremas (fotos muy claras u oscuras)
- Entrenado principalmente con datos de Estados Unidos, Colombia y Australia
- No genera predicciones o diagnósticos por sí mismo
- Requiere validación para aplicaciones específicas

## Variables de Entorno
Configura las siguientes variables de entorno en tu archivo `.env`:

```env
# Ejemplo de variables de entorno
API_KEY=your_api_key_here
MODEL_PATH=path_to_your_model
```

## Configuración de Hugging Face y Token de Acceso

Para descargar modelos desde Hugging Face Hub (por ejemplo, `google/derm-foundation`), es necesario un token de acceso, especialmente si el modelo es privado o si necesitas evitar límites de descarga.

### 1. Obtener tu token de Hugging Face
1. Crea una cuenta (si no tienes) en https://huggingface.co/join
2. Ve a tu perfil y selecciona "Access Tokens" o "Tokens de acceso": https://huggingface.co/settings/tokens
3. Haz clic en "New token" (Nuevo token), asígnale un nombre y selecciona el scope "Read" (lectura).
4. Copia el token generado.

### 2. Configurar el token en el archivo `.env`
Agrega la siguiente línea en tu archivo `.env` (o en `.env.example` para compartir la plantilla):

```env
HF_TOKEN=tu_token_de_huggingface_aqui
```

> **Nota:** No compartas tu token real en repositorios públicos.

### 3. Instalar la librería necesaria
Asegúrate de tener instalada la librería `huggingface_hub`:

```bash
pip install huggingface_hub
```

Si usas `requirements.txt`, puedes agregarla allí:
```
huggingface_hub
```

### 4. ¿Cómo se usa el token en el proyecto?
El token se carga automáticamente desde el archivo `.env` y se utiliza al descargar modelos desde Hugging Face. El archivo `app/config/model_config.py` contiene la lógica para leer la variable `HF_TOKEN` y configurar el entorno.

## Gestión de Imágenes
Las imágenes subidas se procesan y luego se eliminan para garantizar la privacidad y seguridad de los datos.

## Interfaces de Usuario

### Página de Carga de Imagen (`upload.html`)
- **Descripción:** Permite a los usuarios cargar una imagen facial para su análisis.
- **Colores:** Tonos de verde y azul para una apariencia saludable y relajante.
- **Elementos:**
  - Un formulario para subir la imagen.
  - Botón para enviar la imagen.
  - Mensajes de estado (éxito/error).

### Página de Resultados (`results.html`)
- **Descripción:** Muestra los resultados del análisis de la imagen cargada.
- **Colores:** Tonos de verde y azul para una apariencia saludable y relajante.
- **Elementos:**
  - Información sobre el análisis (condiciones detectadas, severidad, etc.).
  - Gráficos o visualizaciones relevantes.
  - Botón para volver a cargar una nueva imagen.

## Modularidad de Modelos
Cada modelo se encapsula en su propio módulo dentro del directorio `models` para facilitar el manejo y extensión del sistema. Esto permite agregar, modificar o eliminar modelos sin afectar el resto del sistema.

### Ejemplo de Estructura de Modelos
```
models/
├── __init__.py
├── base.py         # Modelo base abstracto
├── derm_foundation/ # Módulo para el modelo Derm Foundation
│   ├── __init__.py
│   ├── model.py     # Implementación del modelo Derm Foundation
│   └── config.py    # Configuración específica del modelo
├── model1/          # Módulo para otro modelo adicional
│   ├── __init__.py
│   ├── model.py     # Implementación del modelo1
│   └── config.py    # Configuración específica del modelo1
└── model2/          # Módulo para otro modelo adicional
    ├── __init__.py
    ├── model.py     # Implementación del modelo2
    └── config.py    # Configuración específica del modelo2
```

### Recomendación de Modelos Adicionales
Se recomienda agregar 2 o 3 modelos adicionales para mejorar la funcionalidad y precisión del sistema. Algunas opciones podrían ser:
- **Modelo para la detección de acné:** Para identificar y clasificar diferentes tipos de acné.
- **Modelo para la detección de arrugas:** Para evaluar la edad y el estado de la piel.
- **Modelo para la detección de manchas oscuras:** Para identificar y clasificar manchas oscuras en la piel.

Estos modelos adicionales pueden proporcionar una visión más completa y precisa del estado de la piel del usuario.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto
Para cualquier consulta o colaboración, contacta a:
- Nombre: [Tu Nombre]
- Email: [tu.email@example.com]
- GitHub: [github.com/tu_usuario]

## Contribución
Para contribuir a este proyecto, sigue estos pasos:
1. Haz un fork del repositorio
2. Crea tu rama (`git checkout -b feature/AmazingFeature`)
3. Haz tus cambios (`git commit -m 'Añadir alguna característica AmazingFeature'`)
4. Empuja a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

> **Nota sobre TensorFlow y Torch:**
> Este proyecto está pensado para ejecutarse en CPU. Por defecto, los paquetes `tensorflow` y `torch` que se instalan desde PyPI son compatibles con CPU. No es necesario instalar versiones específicas para GPU. Si tu entorno tiene una GPU y deseas forzar el uso de CPU, asegúrate de instalar:
>
> - Para TensorFlow:
>   ```bash
>   pip install tensorflow
>   ```
>   (No instales `tensorflow-gpu`)
>
> - Para PyTorch:
>   ```bash
>   pip install torch
>   ```
>   (No instales versiones con soporte CUDA a menos que lo requieras explícitamente)
>
> El código del proyecto fuerza el uso de CPU en la configuración (`app/config/model_config.py`).

> **Nota:** Cuando ejecutes la aplicación por primera vez, el modelo de Hugging Face se descargará automáticamente y se guardará en la carpeta local del proyecto (`models/cache`). Si el modelo ya existe en esa carpeta, no se volverá a descargar. No es necesario realizar ninguna descarga manual.

> **Nota sobre la versión de Keras:**
> Este proyecto utiliza `keras==2.13.1` porque es la última versión que permite cargar modelos en formato SavedModel (como el modelo `google/derm-foundation` de Hugging Face) usando `load_model()`. Keras 3 **ya no soporta** cargar modelos SavedModel directamente, solo permite cargar modelos en formato `.keras` o `.h5`. Si en el futuro los modelos de Hugging Face se publican en formato `.keras` o `.h5`, o si migras tu propio flujo de trabajo a estos formatos, podrás actualizar a Keras 3. Por ahora, para compatibilidad y funcionamiento correcto, se recomienda mantener la versión 2.13.1.