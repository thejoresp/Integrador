import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener el directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuración de modelos locales (puedes agregar más rutas aquí si tienes más modelos)
LUNARES_MODEL_PATH = os.path.join(BASE_DIR, "backend", "modelos", "cancerham10000", "lunares.keras")

# Configuración de TensorFlow
import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')  # Forzar uso de CPU
tf.config.threading.set_inter_op_parallelism_threads(4)  # Ajustar según tu CPU
tf.config.threading.set_intra_op_parallelism_threads(4)  # Ajustar según tu CPU

# Crear directorios necesarios para modelos locales
os.makedirs(os.path.dirname(LUNARES_MODEL_PATH), exist_ok=True) 