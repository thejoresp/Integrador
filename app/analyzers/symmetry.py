import cv2
import numpy as np
from typing import Dict, Any
from app.analyzers.base import BaseAnalyzer

# Cambiamos la importación para manejar tanto dlib como dlib-bin
try:
    import dlib
    DLIB_AVAILABLE = True
except ImportError:
    try:
        # Intentar importar desde dlib-bin si está disponible
        import dlib_bin as dlib
        DLIB_AVAILABLE = True
    except ImportError:
        DLIB_AVAILABLE = False
        print("Ni dlib ni dlib-bin están disponibles. Usando método alternativo para análisis de simetría.")

# Variable global para cargar el predictor de landmarks una sola vez
face_landmark_predictor = None

class SymmetryAnalyzer(BaseAnalyzer):
    """Analizador de simetría facial"""
    
    def _load_models(self):
        """Carga los modelos necesarios para el análisis de simetría"""
        global face_landmark_predictor
        
        if DLIB_AVAILABLE and face_landmark_predictor is None:
            try:
                # Intentar cargar el detector de puntos faciales
                predictor_path = "shape_predictor_68_face_landmarks.dat"
                face_landmark_predictor = dlib.shape_predictor(predictor_path)
            except Exception as e:
                print(f"Error al cargar el predictor de landmarks: {str(e)}")
    
    def analyze(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Analiza la simetría facial en una imagen
        
        Args:
            image: Imagen como array de numpy
            
        Returns:
            Dict con resultados del análisis de simetría
        """
        try:
            # Detectar el rostro
            face_location = self._detect_face(image)
            if face_location is None:
                return self._get_default_results()
            
            x, y, w, h = face_location
            face_img = image[y:y+h, x:x+w]
            
            # Si dlib está disponible, intentar detectar landmarks
            if DLIB_AVAILABLE and face_landmark_predictor is not None:
                try:
                    # Detectar puntos faciales
                    detector = dlib.get_frontal_face_detector()
                    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                    rects = detector(gray, 1)
                    
                    if len(rects) > 0:
                        landmarks = face_landmark_predictor(gray, rects[0])
                        landmarks_dict = self._landmarks_to_dict(landmarks)
                        return self._analyze_symmetry_from_landmarks(face_img, landmarks_dict)
                except Exception as e:
                    print(f"Error al usar dlib/dlib-bin: {str(e)}")
            
            # Si no se pueden detectar landmarks, usar método alternativo basado en imagen
            return self._analyze_symmetry_basic(face_img)
        except Exception as e:
            print(f"Error en análisis de simetría: {str(e)}")
            return self._get_default_results()
    
    def _analyze_symmetry_from_landmarks(self, face_image, landmarks):
        """Analiza simetría basándose en puntos de referencia faciales"""
        try:
            # Obtener dimensiones de la imagen
            height, width = face_image.shape[:2]
            midline_x = width / 2
            
            # Extraer puntos clave de ambos lados
            left_eye = landmarks.get("left_eye", {"x": width * 0.35, "y": height * 0.35})
            right_eye = landmarks.get("right_eye", {"x": width * 0.65, "y": height * 0.35})
            
            # Calcular distancias al eje central
            left_dist = abs(left_eye["x"] - midline_x)
            right_dist = abs(right_eye["x"] - midline_x)
            
            # Calcular ratio de distancias (1.0 = perfectamente simétrico)
            if min(left_dist, right_dist) == 0:
                eyes_ratio = 0.5
            else:
                eyes_ratio = min(left_dist, right_dist) / max(left_dist, right_dist)
            
            # Calcular alineación vertical (misma altura)
            vertical_alignment = 1.0 - abs(left_eye["y"] - right_eye["y"]) / height
            
            # Combinar métricas
            symmetry_score = 0.7 * eyes_ratio + 0.3 * vertical_alignment
            
            # Limitar entre 0 y 1
            symmetry_score = max(0, min(symmetry_score, 1))
            
            # Generar análisis textual
            analysis_text = self._get_symmetry_analysis(symmetry_score)
            
            return {
                "score": round(symmetry_score, 2),
                "analysis": analysis_text,
                "details": {
                    "left_right_ratio": round(eyes_ratio, 2),
                    "vertical_alignment": round(vertical_alignment, 2)
                }
            }
        except Exception as e:
            print(f"Error en análisis desde landmarks: {str(e)}")
            return self._analyze_symmetry_basic(face_image)
    
    def _analyze_symmetry_basic(self, face_image):
        """
        Analiza la simetría facial sin landmarks, usando propiedades de la imagen
        """
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            
            # Voltear la imagen horizontalmente
            flipped = cv2.flip(gray, 1)
            
            # Calcular la diferencia entre la imagen original y espejada
            diff = cv2.absdiff(gray, flipped)
            
            # Calcular el valor medio de la diferencia
            mean_diff = np.mean(diff)
            
            # Normalizar (0 = perfecta simetría, 255 = completa asimetría)
            symmetry_score = 1.0 - (mean_diff / 255.0)
            
            # Ajustar escala para ser más realista (pocos rostros son perfectamente simétricos)
            symmetry_score = 0.5 + (symmetry_score - 0.5) * 0.5
            
            # Generar análisis textual
            analysis_text = self._get_symmetry_analysis(symmetry_score)
            
            return {
                "score": round(symmetry_score, 2),
                "analysis": analysis_text,
                "details": {
                    "pixel_diff": round(mean_diff, 2),
                }
            }
        except Exception as e:
            print(f"Error en análisis básico: {str(e)}")
            return self._get_default_results()
    
    def _landmarks_to_dict(self, landmarks):
        """Convierte landmarks de dlib a diccionario"""
        points = {}
        
        # Mapeo de índices a nombres de points
        landmark_map = {
            36: "right_eye",  # Ojo derecho (desde perspectiva de la imagen)
            45: "left_eye",   # Ojo izquierdo (desde perspectiva de la imagen)
            30: "nose_tip",
            48: "mouth_left",
            54: "mouth_right"
        }
        
        for i in range(68):
            if i in landmark_map:
                points[landmark_map[i]] = {
                    "x": landmarks.part(i).x,
                    "y": landmarks.part(i).y
                }
        
        return points
    
    def _get_symmetry_analysis(self, score):
        """Genera texto de análisis basado en puntuación de simetría"""
        if score >= 0.9:
            return "Rostro con alta simetría"
        elif score >= 0.8:
            return "Rostro con buena simetría"
        elif score >= 0.7:
            return "Rostro con simetría normal"
        elif score >= 0.6:
            return "Rostro con ligera asimetría"
        else:
            return "Rostro con notable asimetría"
    
    def _get_default_results(self):
        """Devuelve resultados predeterminados cuando no se puede analizar"""
        return {
            "score": 0.75,
            "analysis": "No se pudo completar el análisis de simetría",
            "details": {
                "left_right_ratio": 1.0,
                "key_points_alignment": 0.75
            }
        }