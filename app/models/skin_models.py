from pydantic import BaseModel, Field
from typing import List, Tuple, Optional

class SkinAnalysisResult(BaseModel):
    """Modelo de resultado para el análisis de condición de la piel."""
    hydration: float = Field(..., description="Nivel de hidratación de la piel (0-100)")
    texture: float = Field(..., description="Suavidad de la textura de la piel (0-100)")
    pores: float = Field(..., description="Visibilidad de poros (0-100, donde 100 es menos visible)")
    oiliness: float = Field(..., description="Nivel de grasa en la piel (0-100, donde 100 es menos grasa)")
    
    @property
    def overall_score(self) -> float:
        """Calcula la puntuación general de la piel."""
        return round((self.hydration + self.texture + self.pores + self.oiliness) / 4, 1)
    
    @property
    def condition_category(self) -> str:
        """Clasifica la condición general de la piel."""
        score = self.overall_score
        if score >= 85:
            return "Excelente"
        elif score >= 70:
            return "Buena"
        elif score >= 50:
            return "Regular"
        else:
            return "Necesita atención"
    
    def get_recommendations(self) -> List[str]:
        """Genera recomendaciones basadas en los resultados."""
        recommendations = []
        
        if self.hydration < 60:
            recommendations.append("Aumentar la hidratación de la piel con productos hidratantes")
            
        if self.texture < 60:
            recommendations.append("Usar exfoliantes suaves para mejorar la textura de la piel")
            
        if self.pores < 60:
            recommendations.append("Utilizar productos astringentes para reducir la apariencia de los poros")
            
        if self.oiliness < 60:
            recommendations.append("Controlar el exceso de grasa con productos matificantes")
            
        return recommendations


class MoleDetail(BaseModel):
    """Detalle de un lunar individual."""
    classification: str = Field(..., description="Clasificación del lunar: 'benign', 'malignant', 'suspicious'")
    confidence: float = Field(..., description="Confianza de la clasificación (0-100)")
    position: Tuple[int, int, int, int] = Field(..., description="Posición del lunar (x, y, width, height)")


class MoleAnalysisResult(BaseModel):
    """Modelo de resultado para el análisis de lunares."""
    total_count: int = Field(..., description="Total de lunares detectados")
    benign_count: int = Field(..., description="Cantidad de lunares benignos")
    malignant_count: int = Field(..., description="Cantidad de lunares potencialmente malignos")
    suspicious_count: int = Field(..., description="Cantidad de lunares sospechosos")
    mole_details: List[dict] = Field(..., description="Detalles de cada lunar detectado")
    
    @property
    def has_risk(self) -> bool:
        """Indica si hay algún riesgo potencial en los lunares."""
        return self.malignant_count > 0 or self.suspicious_count > 0
    
    def get_recommendations(self) -> List[str]:
        """Genera recomendaciones basadas en los resultados."""
        recommendations = []
        
        if self.malignant_count > 0:
            recommendations.append("Consultar a un dermatólogo inmediatamente para evaluar los lunares potencialmente malignos")
        
        if self.suspicious_count > 0:
            recommendations.append("Programar una revisión con un especialista para evaluar los lunares sospechosos")
            
        if self.total_count > 10:
            recommendations.append("Realizar chequeos regulares debido a la cantidad de lunares")
            
        recommendations.append("Proteger la piel del sol con protector solar diariamente")
        
        return recommendations


class SkinToneResult(BaseModel):
    """Modelo de resultado para el análisis de tono de piel."""
    fitzpatrick_type: int = Field(..., description="Tipo de piel según escala Fitzpatrick (1-6)")
    tone_name: str = Field(..., description="Nombre descriptivo del tono de piel")
    rgb_value: Tuple[int, int, int] = Field(..., description="Valor RGB del tono de piel dominante")
    
    def get_recommendations(self) -> List[str]:
        """Genera recomendaciones basadas en el tipo de piel."""
        recommendations = []
        
        if self.fitzpatrick_type <= 2:
            recommendations.append("Usar protector solar de amplio espectro SPF 50+")
            recommendations.append("Evitar exposición solar prolongada, especialmente entre 10am-4pm")
            recommendations.append("Usar ropa protectora y sombreros cuando esté al aire libre")
        elif self.fitzpatrick_type <= 4:
            recommendations.append("Usar protector solar de amplio espectro SPF 30+")
            recommendations.append("Limitar la exposición solar directa durante períodos prolongados")
        else:
            recommendations.append("Usar protector solar de amplio espectro SPF 15+")
            recommendations.append("Proteger la piel del daño solar, aunque sea más resistente")
            
        return recommendations


class CompleteSkinAnalysisResult(BaseModel):
    """Modelo completo para todos los análisis de piel combinados."""
    skin_condition: Optional[SkinAnalysisResult] = Field(None, description="Resultados del análisis de condición de la piel")
    mole_analysis: Optional[MoleAnalysisResult] = Field(None, description="Resultados del análisis de lunares")
    skin_tone: Optional[SkinToneResult] = Field(None, description="Resultados del análisis de tono de piel")
    
    def get_all_recommendations(self) -> List[str]:
        """Recopila todas las recomendaciones de los diferentes análisis."""
        recommendations = []
        
        if self.skin_condition:
            recommendations.extend(self.skin_condition.get_recommendations())
            
        if self.mole_analysis:
            recommendations.extend(self.mole_analysis.get_recommendations())
            
        if self.skin_tone:
            recommendations.extend(self.skin_tone.get_recommendations())
            
        # Eliminar duplicados manteniendo el orden
        unique_recommendations = []
        for rec in recommendations:
            if rec not in unique_recommendations:
                unique_recommendations.append(rec)
                
        return unique_recommendations 