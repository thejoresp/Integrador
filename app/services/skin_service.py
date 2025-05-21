import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import cv2
import numpy as np

from app.analyzers.skin_analyzer import SkinAnalyzer
from app.models.skin_models import (
    SkinAnalysisResult,
    MoleAnalysisResult,
    SkinToneResult,
    CompleteSkinAnalysisResult
)
from app.core.logger import get_logger

logger = get_logger(__name__)

class SkinService:
    """
    Servicio para el análisis de piel que coordina los diferentes tipos de análisis.
    Actúa como una fachada para el SkinAnalyzer.
    """
    
    def __init__(self, models_path: Optional[str] = None, device: str = 'cpu'):
        """
        Inicializa el servicio de análisis de piel.
        
        Args:
            models_path: Ruta opcional a los modelos pre-entrenados
            device: Dispositivo para inferencia ('cpu' o 'cuda')
        """
        try:
            logger.info(f"Inicializando SkinService con modelos en: {models_path}")
            self.analyzer = SkinAnalyzer(models_path)
            logger.info("SkinService inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar SkinAnalyzer: {str(e)}")
            # Inicializar sin modelos específicos
            self.analyzer = SkinAnalyzer()
            logger.warning("SkinAnalyzer inicializado con configuración por defecto debido a un error")
    
    async def analyze_skin_condition(self, image_path: str) -> SkinAnalysisResult:
        """
        Analiza la condición general de la piel (hidratación, textura, poros).
        
        Args:
            image_path: Ruta a la imagen a analizar
            
        Returns:
            SkinAnalysisResult con los resultados del análisis
        """
        logger.info(f"Analizando condición de piel en imagen: {image_path}")
        
        # Verificar que la imagen exista
        if not os.path.exists(image_path):
            logger.error(f"La imagen no existe en la ruta: {image_path}")
            raise FileNotFoundError(f"No se pudo encontrar la imagen en {image_path}")
            
        # Verificar que el archivo es una imagen
        if not self._is_valid_image(image_path):
            logger.error(f"El archivo no es una imagen válida: {image_path}")
            raise ValueError(f"El archivo no es una imagen válida: {image_path}")
            
        try:
            result = self.analyzer.analyze_condition(image_path)
            logger.info(f"Análisis de condición completado: {result.overall_score} ({result.condition_category})")
            return result
        except Exception as e:
            logger.error(f"Error en analyze_skin_condition: {str(e)}")
            raise
    
    async def analyze_moles(self, image_path: str) -> MoleAnalysisResult:
        """
        Detecta y clasifica lunares en la imagen.
        
        Args:
            image_path: Ruta a la imagen a analizar
            
        Returns:
            MoleAnalysisResult con los resultados del análisis
        """
        logger.info(f"Analizando lunares en imagen: {image_path}")
        
        # Verificar que la imagen exista
        if not os.path.exists(image_path):
            logger.error(f"La imagen no existe en la ruta: {image_path}")
            raise FileNotFoundError(f"No se pudo encontrar la imagen en {image_path}")
            
        # Verificar que el archivo es una imagen
        if not self._is_valid_image(image_path):
            logger.error(f"El archivo no es una imagen válida: {image_path}")
            raise ValueError(f"El archivo no es una imagen válida: {image_path}")
            
        try:
            result = self.analyzer.analyze_moles(image_path)
            logger.info(f"Análisis de lunares completado: {result.total_count} lunares detectados")
            return result
        except Exception as e:
            logger.error(f"Error en analyze_moles: {str(e)}")
            raise
    
    async def analyze_skin_tone(self, image_path: str) -> SkinToneResult:
        """
        Determina el tono de piel según la escala Fitzpatrick.
        
        Args:
            image_path: Ruta a la imagen a analizar
            
        Returns:
            SkinToneResult con el tono de piel detectado
        """
        logger.info(f"Analizando tono de piel en imagen: {image_path}")
        
        # Verificar que la imagen exista
        if not os.path.exists(image_path):
            logger.error(f"La imagen no existe en la ruta: {image_path}")
            raise FileNotFoundError(f"No se pudo encontrar la imagen en {image_path}")
            
        # Verificar que el archivo es una imagen
        if not self._is_valid_image(image_path):
            logger.error(f"El archivo no es una imagen válida: {image_path}")
            raise ValueError(f"El archivo no es una imagen válida: {image_path}")
            
        try:
            result = self.analyzer.detect_tone(image_path)
            logger.info(f"Análisis de tono completado: {result.tone_name}")
            return result
        except Exception as e:
            logger.error(f"Error en analyze_skin_tone: {str(e)}")
            raise
    
    async def perform_complete_analysis(self, image_path: str) -> CompleteSkinAnalysisResult:
        """
        Realiza un análisis completo de la piel incluyendo condición, lunares y tono.
        
        Args:
            image_path: Ruta a la imagen a analizar
            
        Returns:
            CompleteSkinAnalysisResult con todos los resultados combinados
        """
        logger.info(f"Iniciando análisis completo de piel en imagen: {image_path}")
        
        try:
            # Verificar que la imagen existe
            if not os.path.exists(image_path):
                logger.error(f"La imagen no existe en la ruta: {image_path}")
                raise FileNotFoundError(f"No se pudo encontrar la imagen en {image_path}")
            
            # Verificar que el archivo es una imagen
            if not self._is_valid_image(image_path):
                logger.error(f"El archivo no es una imagen válida: {image_path}")
                raise ValueError(f"El archivo no es una imagen válida: {image_path}")
            
            # Realizar los diferentes análisis
            logger.info("Ejecutando análisis de condición de piel")
            skin_condition = await self.analyze_skin_condition(image_path)
            
            logger.info("Ejecutando análisis de lunares")
            mole_analysis = await self.analyze_moles(image_path)
            
            logger.info("Ejecutando análisis de tono de piel")
            skin_tone = await self.analyze_skin_tone(image_path)
            
            # Combinar todos los resultados
            complete_result = CompleteSkinAnalysisResult(
                skin_condition=skin_condition,
                mole_analysis=mole_analysis,
                skin_tone=skin_tone
            )
            
            logger.info("Análisis completo finalizado con éxito")
            return complete_result
            
        except Exception as e:
            logger.error(f"Error en perform_complete_analysis: {str(e)}")
            raise
    
    def _is_valid_image(self, image_path: str) -> bool:
        """
        Verifica si un archivo es una imagen válida que puede ser procesada.
        
        Args:
            image_path: Ruta al archivo a verificar
            
        Returns:
            bool: True si es una imagen válida, False en caso contrario
        """
        try:
            # Intentar abrir la imagen con OpenCV
            img = cv2.imread(image_path)
            return img is not None and img.size > 0
        except Exception:
            return False 