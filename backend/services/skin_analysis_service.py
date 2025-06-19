from PIL import Image
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from backend.config.model_config import LUNARES_MODEL_PATH

# --- INICIO: Funciones para modelo lunares.keras ---
LUNARES_MODEL = None
LUNARES_CLASS_NAMES = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']
LUNARES_CLASS_LABELS = {
    'akiec': 'Queratosis Actínica',
    'bcc': 'Carcinoma Basocelular',
    'bkl': 'Queratosis Benigna',
    'df': 'Dermatofibroma',
    'mel': 'Melanoma',
    'nv': 'Lúnar Común (Nevus)',
    'vasc': 'Lesión Vascular'
}

def load_lunares_model():
    global LUNARES_MODEL
    if LUNARES_MODEL is None:
        try:
            print(f"Cargando modelo lunares.keras desde {LUNARES_MODEL_PATH}...")
            LUNARES_MODEL = tf.keras.models.load_model(LUNARES_MODEL_PATH)
            print("Modelo lunares.keras cargado exitosamente.")
        except Exception as e:
            print(f"Error cargando el modelo lunares.keras: {e}")
            LUNARES_MODEL = None
    return LUNARES_MODEL

def predict_lunares_class(image_bytes: bytes):
    model = load_lunares_model()
    if model is None:
        print("El modelo lunares.keras no está cargado.")
        return None, None
    try:
        img = Image.open(BytesIO(image_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_resized = img.resize((224, 224))
        img_array = img_to_array(img_resized)
        img_array = img_array / 255.0
        img_array = img_array.reshape((1, 224, 224, 3))
        preds = model.predict(img_array)
        pred_idx = preds.argmax(axis=1)[0]
        pred_class = LUNARES_CLASS_NAMES[pred_idx]
        pred_label = LUNARES_CLASS_LABELS[pred_class]
        probabilities = {LUNARES_CLASS_LABELS[LUNARES_CLASS_NAMES[i]]: float(preds[0][i]) for i in range(len(LUNARES_CLASS_NAMES))}
        return pred_label, probabilities
    except Exception as e:
        print(f"Error al predecir con lunares.keras: {e}")
        return None, None
# --- FIN: Funciones para modelo lunares.keras --- 