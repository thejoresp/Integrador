from PIL import Image
from io import BytesIO
import tensorflow as tf
import keras
from app.config.model_config import MODEL_CONFIG

MODEL_NAME = MODEL_CONFIG["name"]
MODEL_PATH = MODEL_CONFIG["model_path"]
LOADED_MODEL = None

def load_skin_model():
    """Carga el modelo SavedModel como TFSMLayer para inferencia en Keras 3+ (opción 1)."""
    global LOADED_MODEL
    if LOADED_MODEL is None:
        try:
            print(f"Cargando modelo SavedModel desde {MODEL_PATH}...")
            LOADED_MODEL = keras.layers.TFSMLayer(
                MODEL_PATH,
                call_endpoint="serving_default"  # Cambia si tu endpoint es diferente
            )
            print("Modelo cargado exitosamente como TFSMLayer.")
        except Exception as e:
            print(f"Error cargando el modelo SavedModel: {e}")
            LOADED_MODEL = None
    return LOADED_MODEL

def get_image_embeddings(image_bytes: bytes):
    """
    Procesa una imagen y devuelve los embeddings generados por el modelo Derm Foundation.

    Args:
        image_bytes: Los bytes de la imagen a procesar.

    Returns:
        Un array de numpy con los embeddings, o None si ocurre un error.
    """
    model = load_skin_model()
    if model is None:
        print("El modelo no está cargado. No se pueden generar embeddings.")
        return None

    try:
        img = Image.open(BytesIO(image_bytes))
        
        # Convertir a RGB si tiene canal alfa (ej. PNG)
        if img.mode == 'RGBA' or img.mode == 'P': # P es para paletas, común en GIF
            img = img.convert('RGB')

        # Redimensionar a 448x448 pixels (asegurándose que es RGB primero)
        img_resized = img.resize((448, 448))
        
        # Convertir la imagen redimensionada a bytes PNG para el modelo
        # (El modelo espera bytes de una imagen PNG)
        buf = BytesIO()
        img_resized.save(buf, format='PNG')
        formatted_image_bytes = buf.getvalue()

        # Formatear la entrada como tf.train.Example
        input_tensor_example = tf.train.Example(features=tf.train.Features(
            feature={'image/encoded': tf.train.Feature(
                bytes_list=tf.train.BytesList(value=[formatted_image_bytes]))
            })).SerializeToString()

        # Inferencia usando TFSMLayer
        output = model(tf.constant([input_tensor_example]))
        
        # Extraer el vector de embeddings
        # La salida es un diccionario, y el embedding está bajo la clave 'embedding'
        embedding_vector = output['embedding'].numpy().flatten()
        return embedding_vector
    except Exception as e:
        print(f"Error al procesar la imagen o generar embeddings: {e}")
        return None

# Opcional: Cargar el modelo al iniciar el módulo si se desea
# load_skin_model() 