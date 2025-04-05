import cv2
import numpy as np
from typing import Dict, Any
from app.analyzers.base import BaseAnalyzer

class AgeGenderAnalyzer(BaseAnalyzer):
    """Analizador para estimación de edad y género"""
    
    def _load_models(self):
        """
        Carga los modelos para estimación de edad y género
        En producción, aquí cargaríamos modelos preentrenados
        """
        # Simulamos la carga de modelos
        # En un caso real, usaríamos:
        # - DeepFace
        # - InsightFace
        # - Modelos propios de TensorFlow/PyTorch
        pass
    
    def analyze(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Analiza edad y género en una imagen facial
        
        Args:
            image: Imagen como array de numpy (BGR)
            
        Returns:
            Dict: Resultados del análisis de edad y género
        """
        face = self._detect_face(image)
        if face is None:
            return {
                "error": "No se detectó un rostro en la imagen",
                "age": None,
                "gender": None
            }
        
        x, y, w, h = face
        face_img = image[y:y+h, x:x+w]
        
        # En producción, aquí se utilizarían los modelos preentrenados
        # Como ejemplo, usamos valores simulados:
        
        # Edad aparente (simulada)
        # En producción: age_prediction = age_model.predict(face_img)
        age = np.random.normal(35, 5)  # Media 35, desviación 5
        age = max(18, min(80, age))  # Limitar entre 18 y 80
        
        # Género aparente (simulado)
        # En producción: gender_prediction = gender_model.predict(face_img)
        gender_conf = np.random.uniform(0.6, 0.95)
        gender = "masculino" if np.random.random() > 0.5 else "femenino"
        
        # Calcular la simetría facial
        symmetry_score = self._calculate_symmetry(face_img)
        
        return {
            "age": {
                "years": round(age, 1),
                "range": f"{round(age-3)}-{round(age+3)}"
            },
            "gender": {
                "label": gender,
                "confidence": round(gender_conf * 100, 2)
            },
            "symmetry": {
                "score": symmetry_score,
                "level": self._get_symmetry_level(symmetry_score)
            }
        }
    
    def _calculate_symmetry(self, face_img: np.ndarray) -> float:
        """
        Calcula la simetría facial
        
        Args:
            face_img: Imagen recortada del rostro
            
        Returns:
            float: Puntuación de simetría (0-100)
        """
        # En producción, usaríamos landmarks faciales con dlib o MediaPipe
        # Para este ejemplo, usamos un método simplificado:
        
        h, w = face_img.shape[:2]
        mid = w // 2
        
        # Dividir la cara en lado izquierdo y derecho
        left_side = face_img[:, :mid].copy()
        right_side = face_img[:, mid:].copy()
        right_side_flipped = cv2.flip(right_side, 1)
        
        # Redimensionar si es necesario para que coincidan las dimensiones
        if left_side.shape[1] != right_side_flipped.shape[1]:
            min_width = min(left_side.shape[1], right_side_flipped.shape[1])
            left_side = left_side[:, :min_width]
            right_side_flipped = right_side_flipped[:, :min_width]
        
        # Calcular la diferencia entre ambos lados
        diff = cv2.absdiff(left_side, right_side_flipped)
        diff_score = np.sum(diff) / (diff.size * 255)
        
        # Convertir a una puntuación de simetría (0-100)
        symmetry_score = 100 * (1 - diff_score)
        return round(symmetry_score, 2)
    
    def _get_symmetry_level(self, score: float) -> str:
        """Convierte una puntuación de simetría a una etiqueta"""
        if score < 70:
            return "Baja"
        elif score < 85:
            return "Media"
        else:
            return "Alta"
