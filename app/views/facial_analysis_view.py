"""
Componente de presentación para resultados de análisis facial.

Este módulo implementa la capa de Vista del patrón MVC, 
proporcionando renderizado de templates y presentación de datos.
"""
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.config import TEMPLATE_DIR
from app.models.dto.api_models import AnalysisResultDTO


class FacialAnalysisView:
    """
    Vista para la presentación de resultados de análisis facial.
    
    Esta clase maneja la presentación de los datos a los usuarios,
    siguiendo el patrón MVC.
    """
    
    def __init__(self):
        """Inicializa la vista con las plantillas necesarias."""
        self.templates = Jinja2Templates(directory=TEMPLATE_DIR)
    
    def render_result_page(
        self, 
        request: Request, 
        analysis_result: AnalysisResultDTO, 
        image_url: str
    ) -> HTMLResponse:
        """
        Renderiza la página de resultados del análisis facial.
        
        Args:
            request: Objeto Request de FastAPI
            analysis_result: DTO con los resultados del análisis
            image_url: URL de la imagen analizada
            
        Returns:
            Respuesta HTML con la página renderizada
        """
        return self.templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "results": analysis_result.dict(),
                "image_url": image_url
            }
        )
    
    def render_index_page(self, request: Request) -> HTMLResponse:
        """
        Renderiza la página principal de la aplicación.
        
        Args:
            request: Objeto Request de FastAPI
            
        Returns:
            Respuesta HTML con la página principal
        """
        return self.templates.TemplateResponse("index.html", {"request": request})
    
    def generate_metrics_view(self, analysis_result: AnalysisResultDTO) -> dict:
        """
        Genera datos para visualización de métricas en gráficos.
        
        Args:
            analysis_result: DTO con los resultados del análisis
            
        Returns:
            Diccionario con datos formateados para visualización
        """
        # Extraer emociones para gráficos si están disponibles
        emotions_data = {}
        if "emotion" in analysis_result.analyses:
            emotions = analysis_result.analyses["emotion"].get("emotions", {})
            emotions_data = {
                "labels": list(emotions.keys()),
                "values": list(emotions.values()),
                "colors": self._get_emotion_colors(emotions.keys())
            }
        
        # Extraer datos de simetría si están disponibles
        symmetry_data = {}
        if "symmetry" in analysis_result.analyses:
            sym = analysis_result.analyses["symmetry"]
            score = sym.get("score", 0)
            symmetry_data = {
                "score": score,
                "percentage": int(score * 100),
                "color": self._get_symmetry_color(score)
            }
        
        return {
            "emotions": emotions_data,
            "symmetry": symmetry_data
        }
    
    def _get_emotion_colors(self, emotions):
        """Devuelve colores para cada emoción."""
        color_map = {
            "happy": "#4CAF50",  # Verde
            "neutral": "#2196F3",  # Azul
            "sad": "#9E9E9E",  # Gris
            "angry": "#F44336",  # Rojo
            "surprise": "#FF9800",  # Naranja
            "fear": "#673AB7",  # Púrpura
            "disgust": "#795548"  # Marrón
        }
        return [color_map.get(emotion, "#000000") for emotion in emotions]
    
    def _get_symmetry_color(self, score):
        """Devuelve color basado en la puntuación de simetría."""
        if score >= 0.8:
            return "#4CAF50"  # Verde - buena simetría
        elif score >= 0.6:
            return "#FF9800"  # Naranja - simetría media
        else:
            return "#F44336"  # Rojo - baja simetría