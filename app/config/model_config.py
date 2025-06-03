import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener el directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar el caché de Hugging Face para que use el directorio del proyecto
os.environ["HF_HOME"] = os.path.join(BASE_DIR, "models", "cache")
os.environ["TRANSFORMERS_CACHE"] = os.path.join(BASE_DIR, "models", "cache")
os.environ["HF_DATASETS_CACHE"] = os.path.join(BASE_DIR, "models", "cache")

# Configuración del modelo
MODEL_CONFIG = {
    "name": "google/derm-foundation",
    "image_size": (448, 448),
    "batch_size": 1,
    "cache_dir": os.path.join(BASE_DIR, "models", "cache"),  # Directorio absoluto para cachear los modelos
    "model_path": os.path.join(BASE_DIR, "models", "cache", "models--google--derm-foundation", "snapshots", "a16a6ab4f87888948fe248136e697ed28146a1c6")  # Ruta específica para el modelo
}

# Token de Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")

# Configuración de TensorFlow
import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')  # Forzar uso de CPU
tf.config.threading.set_inter_op_parallelism_threads(4)  # Ajustar según tu CPU
tf.config.threading.set_intra_op_parallelism_threads(4)  # Ajustar según tu CPU

# Crear directorios necesarios
os.makedirs(MODEL_CONFIG["cache_dir"], exist_ok=True)
os.makedirs(MODEL_CONFIG["model_path"], exist_ok=True) 