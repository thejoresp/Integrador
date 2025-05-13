import cv2
import numpy as np
from pathlib import Path
import tensorflow as tf
from app.core.logger import get_logger
from app.models.skin_models import SkinAnalysisResult, MoleAnalysisResult, SkinToneResult
import os
import sys

logger = get_logger(__name__)

class SkinAnalyzer:
    """
    Analizador de piel que proporciona información sobre condición de la piel,
    detección de lunares y clasificación de tono de piel.
    """
    
    def __init__(self, models_path=None):
        """
        Inicializa el analizador de piel cargando los modelos necesarios.
        
        Args:
            models_path: Ruta a los modelos pre-entrenados
        """
        self.models_path = Path(models_path) if models_path else Path("models/pretrained/skin")
        logger.info(f"Inicializando SkinAnalyzer con modelos en: {self.models_path}")
        print(f"Inicializando SkinAnalyzer con modelos en: {self.models_path}", file=sys.stderr)
        self._load_models()
        logger.info("SkinAnalyzer inicializado correctamente")
        print("SkinAnalyzer inicializado correctamente", file=sys.stderr)
    
    def _load_models(self):
        """Carga los modelos necesarios para el análisis de piel"""
        try:
            # Cargar modelo de condición de piel si existe
            skin_condition_model_path = self.models_path / "skin_condition"
            if skin_condition_model_path.exists():
                self.skin_condition_model = tf.keras.models.load_model(str(skin_condition_model_path))
                logger.info("Modelo de condición de piel cargado correctamente")
                print("Modelo de condición de piel cargado correctamente", file=sys.stderr)
            else:
                self.skin_condition_model = None
                logger.warning(f"Modelo de condición de piel no encontrado en {skin_condition_model_path}, se utilizará análisis básico")
                print(f"Modelo de condición de piel no encontrado en {skin_condition_model_path}, se utilizará análisis básico", file=sys.stderr)
            
            # Cargar modelo de detección de lunares si existe
            mole_model_path = self.models_path / "mole_detection"
            if mole_model_path.exists():
                self.mole_model = tf.keras.models.load_model(str(mole_model_path))
                logger.info("Modelo de detección de lunares cargado correctamente")
                print("Modelo de detección de lunares cargado correctamente", file=sys.stderr)
            else:
                self.mole_model = None
                logger.warning(f"Modelo de detección de lunares no encontrado en {mole_model_path}, se utilizará análisis básico")
                print(f"Modelo de detección de lunares no encontrado en {mole_model_path}, se utilizará análisis básico", file=sys.stderr)
                
            logger.info("Carga de modelos completada")
            print("Carga de modelos completada", file=sys.stderr)
        except Exception as e:
            logger.error(f"Error al cargar modelos: {str(e)}")
            print(f"Error al cargar modelos: {str(e)}", file=sys.stderr)
            import traceback
            logger.error(traceback.format_exc())
            print(traceback.format_exc(), file=sys.stderr)
            raise
    
    def analyze_condition(self, image_path):
        """
        Analiza la condición general de la piel (hidratación, textura, poros).
        
        Args:
            image_path: Ruta a la imagen a analizar
            
        Returns:
            SkinAnalysisResult con los resultados del análisis
        """
        try:
            # Verificar que la imagen existe
            if not os.path.exists(image_path):
                logger.error(f"La imagen no existe en la ruta: {image_path}")
                print(f"La imagen no existe en la ruta: {image_path}", file=sys.stderr)
                raise FileNotFoundError(f"No se pudo encontrar la imagen en {image_path}")
                
            # Verificar el tamaño del archivo
            file_size = os.path.getsize(image_path)
            logger.info(f"Tamaño del archivo a analizar: {file_size} bytes")
            print(f"Tamaño del archivo a analizar: {file_size} bytes", file=sys.stderr)
            
            if file_size < 100:  # Menos de 100 bytes no puede ser una imagen válida
                logger.error(f"El archivo es demasiado pequeño para ser una imagen válida: {file_size} bytes")
                print(f"El archivo es demasiado pequeño para ser una imagen válida: {file_size} bytes", file=sys.stderr)
                raise ValueError(f"El archivo es demasiado pequeño para ser una imagen válida: {file_size} bytes")
            
            # Cargar imagen usando NumPy directamente para verificar si es legible
            try:
                with open(image_path, 'rb') as f:
                    img_array = np.frombuffer(f.read(), dtype=np.uint8)
                    if len(img_array) == 0:
                        logger.error(f"El archivo no contiene datos válidos: {image_path}")
                        print(f"El archivo no contiene datos válidos: {image_path}", file=sys.stderr)
                        raise ValueError(f"El archivo no contiene datos válidos: {image_path}")
            except Exception as e:
                logger.error(f"Error al leer los bytes de la imagen: {str(e)}")
                print(f"Error al leer los bytes de la imagen: {str(e)}", file=sys.stderr)
                raise ValueError(f"No se pudo leer el archivo como imagen: {str(e)}")
                
            # Cargar y preprocesar la imagen
            logger.info(f"Cargando imagen desde: {image_path}")
            print(f"Cargando imagen desde: {image_path}", file=sys.stderr)
            image = cv2.imread(str(image_path))
            
            if image is None:
                logger.error(f"Error al cargar la imagen: {image_path}")
                print(f"Error al cargar la imagen: {image_path}", file=sys.stderr)
                # Intentar con PIL como alternativa
                try:
                    from PIL import Image
                    pil_image = Image.open(image_path)
                    # Convertir de PIL a OpenCV
                    image = np.array(pil_image)
                    # Si la imagen está en modo RGB, convertirla a BGR para OpenCV
                    if len(image.shape) == 3 and image.shape[2] == 3:
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    logger.info("Imagen cargada correctamente usando PIL")
                    print("Imagen cargada correctamente usando PIL", file=sys.stderr)
                except Exception as pil_error:
                    logger.error(f"También falló al cargar con PIL: {str(pil_error)}")
                    print(f"También falló al cargar con PIL: {str(pil_error)}", file=sys.stderr)
                    raise ValueError(f"No se pudo cargar la imagen desde {image_path}. OpenCV y PIL fallaron.")
                
            # Verificar que la imagen no esté vacía
            if image.size == 0:
                logger.error(f"La imagen está vacía: {image_path}")
                print(f"La imagen está vacía: {image_path}", file=sys.stderr)
                raise ValueError(f"La imagen cargada está vacía: {image_path}")
                
            # Imprimir información de la imagen para depuración
            logger.info(f"Información de la imagen: forma={image.shape}, tipo={image.dtype}")
            print(f"Información de la imagen: forma={image.shape}, tipo={image.dtype}", file=sys.stderr)
                
            # Convertir a espacio de color adecuado para análisis de piel
            logger.info("Preprocesando imagen para análisis de condición")
            print("Preprocesando imagen para análisis de condición", file=sys.stderr)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Análisis de hidratación (basado en brillo y textura)
            logger.info("Analizando hidratación")
            print("Analizando hidratación", file=sys.stderr)
            hydration_score = self._analyze_hydration(image_rgb)
            
            # Análisis de textura
            logger.info("Analizando textura")
            print("Analizando textura", file=sys.stderr)
            texture_score = self._analyze_texture(image_rgb)
            
            # Análisis de poros
            logger.info("Analizando poros")
            print("Analizando poros", file=sys.stderr)
            pore_score = self._analyze_pores(image_rgb)
            
            # Análisis de grasa/sebo
            logger.info("Analizando nivel de grasa")
            print("Analizando nivel de grasa", file=sys.stderr)
            oiliness_score = self._analyze_oiliness(image_rgb)
            
            logger.info(f"Análisis de condición completado: hidratación={hydration_score}, textura={texture_score}, poros={pore_score}, grasa={oiliness_score}")
            print(f"Análisis de condición completado: hidratación={hydration_score}, textura={texture_score}, poros={pore_score}, grasa={oiliness_score}", file=sys.stderr)
            
            return SkinAnalysisResult(
                hydration=hydration_score,
                texture=texture_score,
                pores=pore_score,
                oiliness=oiliness_score
            )
        except Exception as e:
            logger.error(f"Error al analizar condición de la piel: {str(e)}")
            print(f"Error al analizar condición de la piel: {str(e)}", file=sys.stderr)
            import traceback
            logger.error(traceback.format_exc())
            print(traceback.format_exc(), file=sys.stderr)
            raise
    
    def analyze_moles(self, image_path):
        """
        Detecta y clasifica lunares en la imagen.
        
        Args:
            image_path: Ruta a la imagen a analizar
            
        Returns:
            MoleAnalysisResult con los resultados del análisis
        """
        try:
            # Verificar que la imagen existe
            if not os.path.exists(image_path):
                logger.error(f"La imagen no existe en la ruta: {image_path}")
                raise FileNotFoundError(f"No se pudo encontrar la imagen en {image_path}")
                
            # Cargar y preprocesar la imagen
            logger.info(f"Cargando imagen desde: {image_path}")
            image = cv2.imread(str(image_path))
            
            if image is None:
                logger.error(f"Error al cargar la imagen: {image_path}")
                raise ValueError(f"No se pudo cargar la imagen desde {image_path}")
                
            # Verificar que la imagen no esté vacía
            if image.size == 0:
                logger.error(f"La imagen está vacía: {image_path}")
                raise ValueError(f"La imagen cargada está vacía: {image_path}")
                
            # Detectar regiones de interés (ROI) que podrían ser lunares
            logger.info("Detectando regiones de lunares potenciales")
            roi_list = self._detect_mole_regions(image)
            
            # Clasificar cada ROI como benigno o maligno
            results = []
            for roi in roi_list:
                if self.mole_model:
                    # Usar modelo pre-entrenado para clasificación
                    classification = self._classify_mole_with_model(roi)
                else:
                    # Usar método simplificado basado en características visuales
                    classification = self._classify_mole_basic(roi)
                
                results.append(classification)
            
            # Contar resultados
            benign_count = sum(1 for r in results if r['classification'] == 'benign')
            malignant_count = sum(1 for r in results if r['classification'] == 'malignant')
            suspicious_count = sum(1 for r in results if r['classification'] == 'suspicious')
            
            logger.info(f"Análisis de lunares completado: {len(results)} lunares detectados")
            
            return MoleAnalysisResult(
                total_count=len(results),
                benign_count=benign_count,
                malignant_count=malignant_count,
                suspicious_count=suspicious_count,
                mole_details=results
            )
        except Exception as e:
            logger.error(f"Error al analizar lunares: {str(e)}")
            raise
    
    def detect_tone(self, image_path):
        """
        Determina el tono de piel según la escala Fitzpatrick.
        
        Args:
            image_path: Ruta a la imagen a analizar
            
        Returns:
            SkinToneResult con el tono de piel detectado
        """
        try:
            # Verificar que la imagen existe
            if not os.path.exists(image_path):
                logger.error(f"La imagen no existe en la ruta: {image_path}")
                raise FileNotFoundError(f"No se pudo encontrar la imagen en {image_path}")
                
            # Cargar y preprocesar la imagen
            logger.info(f"Cargando imagen desde: {image_path}")
            image = cv2.imread(str(image_path))
            
            if image is None:
                logger.error(f"Error al cargar la imagen: {image_path}")
                raise ValueError(f"No se pudo cargar la imagen desde {image_path}")
                
            # Verificar que la imagen no esté vacía
            if image.size == 0:
                logger.error(f"La imagen está vacía: {image_path}")
                raise ValueError(f"La imagen cargada está vacía: {image_path}")
            
            # Convertir a espacio de color adecuado
            logger.info("Preprocesando imagen para análisis de tono de piel")
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detectar cara y extraer región de piel
            logger.info("Extrayendo región de piel")
            skin_region = self._extract_skin_region(image_rgb)
            
            # Aplicar K-means para encontrar el color dominante de la piel
            logger.info("Clasificando tono de piel")
            skin_tone = self._classify_skin_tone(skin_region)
            
            logger.info(f"Análisis de tono completado: Tipo {skin_tone['fitzpatrick_type']} - {skin_tone['tone_name']}")
            
            return SkinToneResult(
                fitzpatrick_type=skin_tone['fitzpatrick_type'],
                tone_name=skin_tone['tone_name'],
                rgb_value=skin_tone['rgb_value']
            )
        except Exception as e:
            logger.error(f"Error al detectar tono de piel: {str(e)}")
            raise
    
    # Métodos auxiliares privados
    
    def _analyze_hydration(self, image_rgb):
        """Analiza el nivel de hidratación de la piel basado en brillo y textura"""
        # Implementación simplificada para demostración
        # En un sistema real, se usaría un modelo entrenado con datos reales
        hsv_image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
        
        # Extraer canal V (brillo) que puede indicar hidratación
        v_channel = hsv_image[:,:,2]
        
        # Calcular estadísticas básicas
        mean_brightness = np.mean(v_channel)
        std_brightness = np.std(v_channel)
        
        # Valor normalizado entre 0-100
        # Más brillo uniforme generalmente indica mejor hidratación
        hydration_score = min(100, max(0, (mean_brightness - 10*std_brightness/255) * 100))
        
        return round(hydration_score, 1)
    
    def _analyze_texture(self, image_rgb):
        """Analiza la textura de la piel usando filtros de Gabor o GLCM"""
        # Implementación simplificada para demostración
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        
        # Aplicar filtro Laplaciano para detectar bordes/textura
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        
        # Calcular estadísticas sobre el Laplaciano
        mean_edge = np.mean(np.abs(laplacian))
        
        # Piel más suave tiene menos bordes/texturas
        # Invertimos la escala para que 100 sea piel más suave
        texture_score = max(0, min(100, 100 - (mean_edge * 5)))
        
        return round(texture_score, 1)
    
    def _analyze_pores(self, image_rgb):
        """Analiza el tamaño y visibilidad de los poros"""
        # Implementación simplificada
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        
        # Aplicar ecualización de histograma para mejorar el contraste
        equalized = cv2.equalizeHist(gray)
        
        # Aplicar filtro para detectar estructuras pequeñas (poros)
        kernel = np.ones((3,3), np.uint8)
        tophat = cv2.morphologyEx(equalized, cv2.MORPH_TOPHAT, kernel)
        
        # Calcular estadísticas
        mean_tophat = np.mean(tophat)
        
        # Convertir a puntaje: menos estructuras visible = mejor piel
        pore_score = max(0, min(100, 100 - (mean_tophat * 0.5)))
        
        return round(pore_score, 1)
    
    def _analyze_oiliness(self, image_rgb):
        """Analiza el nivel de grasa/sebo en la piel"""
        hsv_image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
        
        # Las áreas brillantes pueden indicar piel grasa
        s_channel = hsv_image[:,:,1]  # Saturación
        v_channel = hsv_image[:,:,2]  # Brillo
        
        # Áreas brillantes pero poco saturadas indican brillo por grasa
        # Crear una máscara para zonas potencialmente grasas
        potential_oily = ((v_channel > 150) & (s_channel < 70)).astype(np.uint8) * 255
        
        # Calcular porcentaje de píxeles potencialmente grasos
        oily_percent = (np.sum(potential_oily > 0) / potential_oily.size) * 100
        
        # Convertir a score (0-100), donde 0 es muy grasa y 100 es no grasa
        oiliness_score = max(0, min(100, 100 - (oily_percent * 5)))
        
        return round(oiliness_score, 1)
    
    def _detect_mole_regions(self, image):
        """Detecta regiones que podrían ser lunares o manchas en la piel"""
        # Implementación simplificada
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Aplicar umbral adaptativo para detectar áreas oscuras
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Encontrar contornos
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar contornos por tamaño y forma
        mole_regions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if 50 < area < 5000:  # Filtrar por tamaño
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h
                if 0.5 < aspect_ratio < 2.0:  # Filtrar por forma
                    # Extraer ROI
                    roi = image[y:y+h, x:x+w]
                    mole_regions.append({
                        'roi': roi,
                        'position': (x, y, w, h)
                    })
        
        # Limitar a máximo 10 regiones para este ejemplo
        return mole_regions[:10]
    
    def _classify_mole_with_model(self, roi_data):
        """Clasifica un lunar usando el modelo pre-entrenado"""
        roi = roi_data['roi']
        
        # Preprocesar para el modelo
        resized_roi = cv2.resize(roi, (224, 224))
        normalized_roi = resized_roi / 255.0
        input_tensor = np.expand_dims(normalized_roi, axis=0)
        
        # Hacer predicción
        prediction = self.mole_model.predict(input_tensor)[0]
        
        # Interpretar resultado (ejemplo para un modelo con 3 clases)
        if len(prediction) >= 3:
            class_idx = np.argmax(prediction)
            confidence = float(prediction[class_idx])
            
            if class_idx == 0:
                classification = 'benign'
            elif class_idx == 1:
                classification = 'malignant'
            else:
                classification = 'suspicious'
        else:
            # Modelo binario (benigno vs maligno)
            confidence = float(prediction[0])
            if confidence > 0.5:
                classification = 'malignant'
            else:
                classification = 'benign'
        
        return {
            'classification': classification,
            'confidence': round(confidence * 100, 1),
            'position': roi_data['position']
        }
    
    def _classify_mole_basic(self, roi_data):
        """Clasificación básica basada en características visuales simples"""
        roi = roi_data['roi']
        
        # Calcular características básicas
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Variación de color (la irregularidad es una bandera roja)
        color_std = np.std(hsv_roi[:,:,0])
        
        # Asimetría basada en momentos
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        moments = cv2.moments(gray_roi)
        
        # Relación entre momentos puede indicar asimetría
        if moments['m00'] != 0:
            asymmetry = moments['mu11'] / moments['m00']
        else:
            asymmetry = 0
            
        # Tono medio (los lunares muy oscuros podrían ser sospechosos)
        mean_v = np.mean(hsv_roi[:,:,2])
        
        # Clasificación simplificada
        if color_std > 20 and abs(asymmetry) > 0.2 and mean_v < 80:
            classification = 'suspicious'
            confidence = 70.0
        elif color_std > 15 or abs(asymmetry) > 0.15 or mean_v < 60:
            classification = 'suspicious'
            confidence = 60.0
        else:
            classification = 'benign'
            confidence = 75.0
        
        return {
            'classification': classification,
            'confidence': confidence,
            'position': roi_data['position']
        }
    
    def _extract_skin_region(self, image_rgb):
        """Extrae regiones de piel de la imagen para análisis de tono"""
        # Convertir a espacio YCrCb que es bueno para segmentación de piel
        ycrcb = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2YCrCb)
        
        # Definir rango para detección de piel
        lower = np.array([0, 133, 77], dtype=np.uint8)
        upper = np.array([255, 173, 127], dtype=np.uint8)
        
        # Crear máscara
        skin_mask = cv2.inRange(ycrcb, lower, upper)
        
        # Aplicar operaciones morfológicas para mejorar la máscara
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
        
        # Aplicar la máscara a la imagen original
        skin_region = cv2.bitwise_and(image_rgb, image_rgb, mask=skin_mask)
        
        return skin_region
    
    def _classify_skin_tone(self, skin_region):
        """Clasifica el tono de piel basado en el color dominante"""
        # Filtrar píxeles negros (fondo)
        pixels = skin_region.reshape(-1, 3)
        pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]
        
        if len(pixels) == 0:
            return {
                'fitzpatrick_type': 0,
                'tone_name': 'Indeterminado',
                'rgb_value': (0, 0, 0)
            }
        
        # Aplicar K-means para encontrar color dominante
        pixels = np.float32(pixels)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = 1  # Buscamos el color dominante
        _, _, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Convertir a RGB
        center = centers[0].astype(np.uint8)
        
        # Clasificar en escala Fitzpatrick
        return self._fitzpatrick_classifier(center)
    
    def _fitzpatrick_classifier(self, rgb_color):
        """Clasifica un color RGB en un tipo Fitzpatrick"""
        # Valores aproximados para los tipos Fitzpatrick
        fitzpatrick_types = [
            {'type': 1, 'name': 'Tipo I - Muy claro', 'rgb': (255, 236, 210)},
            {'type': 2, 'name': 'Tipo II - Claro', 'rgb': (241, 214, 188)},
            {'type': 3, 'name': 'Tipo III - Medio', 'rgb': (226, 192, 166)},
            {'type': 4, 'name': 'Tipo IV - Moreno moderado', 'rgb': (198, 160, 124)},
            {'type': 5, 'name': 'Tipo V - Moreno oscuro', 'rgb': (162, 120, 88)},
            {'type': 6, 'name': 'Tipo VI - Muy oscuro', 'rgb': (98, 64, 39)}
        ]
        
        # Encontrar la distancia euclidiana mínima
        min_distance = float('inf')
        best_match = None
        
        for ft in fitzpatrick_types:
            dist = np.sqrt(np.sum((np.array(rgb_color) - np.array(ft['rgb']))**2))
            if dist < min_distance:
                min_distance = dist
                best_match = ft
        
        return {
            'fitzpatrick_type': best_match['type'],
            'tone_name': best_match['name'],
            'rgb_value': tuple(rgb_color)
        } 