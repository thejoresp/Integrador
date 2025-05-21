"""
Analizador de piel utilizando el modelo Derm Foundation de Google.
"""

import os
import tensorflow as tf
from PIL import Image
import numpy as np
from huggingface_hub import from_pretrained_keras
from app.config import get_settings
import io
import keras
from keras import ops

class DermAnalyzer:
    """Analizador de piel utilizando Derm Foundation."""
    
    def __init__(self):
        """Inicializa el analizador de piel."""
        self.config = get_settings()
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Carga el modelo Derm Foundation."""
        try:
            # Obtener el token de la variable de entorno
            token = os.getenv("HUGGING_FACE_HUB_TOKEN")
            if not token:
                raise ValueError("La variable de entorno HUGGING_FACE_HUB_TOKEN no está configurada")
            
            os.environ["HUGGING_FACE_HUB_TOKEN"] = token
            
            print("Cargando modelo Derm Foundation...")
            model_path = "./models/models--google--derm-foundation/snapshots/a16a6ab4f87888948fe248136e697ed28146a1c6"
            self.model = keras.layers.TFSMLayer(
                model_path,
                call_endpoint='serving_default'
            )
            print("Modelo Derm Foundation cargado exitosamente")
        except Exception as e:
            print(f"Error al cargar el modelo Derm Foundation: {str(e)}")
            raise
    
    def _preprocess_image(self, image):
        """Preprocesa la imagen para el modelo."""
        # Convertir a PIL Image si es necesario
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        # Redimensionar a 448x448 (requerido por Derm Foundation)
        image = image.resize((448, 448), Image.Resampling.LANCZOS)
        
        # Convertir a RGB si es necesario
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Guardar la imagen en un buffer en memoria como JPEG con alta calidad
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=95)
        buf = buffer.getvalue()
        
        # Crear tensor de ejemplo usando tf.train.Example
        input_tensor = tf.train.Example(features=tf.train.Features(
            feature={'image/encoded': tf.train.Feature(
                bytes_list=tf.train.BytesList(value=[buf]))
            })).SerializeToString()
        
        return input_tensor
    
    def analyze(self, image):
        """
        Analiza una imagen de piel.
        
        Args:
            image: Imagen a analizar (numpy array)
            
        Returns:
            dict: Resultados del análisis
        """
        try:
            print("Preprocesando imagen...")
            input_tensor = self._preprocess_image(image)
            print("Input tensor generado correctamente:", type(input_tensor), len(input_tensor) if hasattr(input_tensor, '__len__') else 'no len')

            print("Realizando inferencia...")
            # Convertir el tensor a formato compatible con TFSMLayer
            input_tensor = tf.constant([input_tensor], dtype=tf.string)
            output = self.model(inputs=input_tensor)
            print("Inferencia realizada correctamente.")

            # Convertir el output a numpy
            embedding_vector = output['embedding'].numpy().flatten()
            print("Embedding extraído correctamente.")

            skin_features = self._analyze_skin_features(embedding_vector)
            print("Análisis de piel realizado correctamente.")

            return {
                "status": "success",
                "embedding_dimensions": len(embedding_vector),
                "skin_features": skin_features
            }
            
        except Exception as e:
            import traceback
            print("ERROR DETALLADO EN analyze:")
            traceback.print_exc()
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _analyze_skin_features(self, embedding):
        """
        Analiza características de la piel basadas en el embedding.
        
        Args:
            embedding: Vector de embedding del modelo
            
        Returns:
            dict: Características de la piel analizadas
        """
        # Usar ops.mean para mejor compatibilidad con Keras 3
        texture_score = ops.mean(embedding[:100])
        texture = "normal" if texture_score > 0 else "irregular"
        
        tone_score = ops.mean(embedding[100:200])
        tone = "uniforme" if tone_score > 0 else "irregular"
        
        # Análisis de condiciones con umbrales más precisos
        conditions = []
        if texture_score < -0.5:
            conditions.append("Textura irregular")
        if tone_score < -0.5:
            conditions.append("Tono irregular")
            
        # Análisis de características específicas con umbrales ajustados
        if ops.mean(embedding[200:300]) < -0.3:
            conditions.append("Posible sequedad")
        if ops.mean(embedding[300:400]) < -0.3:
            conditions.append("Posible enrojecimiento")
        if ops.mean(embedding[400:500]) < -0.3:
            conditions.append("Posible inflamación")
        
        return {
            "texture": texture,
            "tone": tone,
            "conditions": conditions
        } 