# Registro de cambios (Changelog)

## [2.1.0] - 2023-05-12

### Corregido
- Solucionado el problema de procesamiento de imágenes en el analizador de piel
- Corregido el error "NoneType object has no attribute lower" al procesar imágenes con content-type vacío
- Mejorado el manejo de autenticación para facilitar pruebas de API
- Verificación de existencia y validez de los archivos subidos antes de procesarlos

### Mejorado
- Mejorado el sistema de logs con información detallada para depuración
- Añadido soporte para mayor variedad de tipos MIME, incluyendo 'application/octet-stream'
- Implementada tolerancia a fallos cuando el tipo de contenido no se especifica correctamente
- Añadida validación de archivos más robusta, verificando tamaño y contenido

### Añadido
- Script de prueba `test_skin_api.py` para verificar el funcionamiento de todos los endpoints
- Compatibilidad mejorada para diversas bibliotecas de cliente (como requests en Python)
- Mensajes de error más informativos y específicos
- Sistema de detección de tipos de archivo basado en extensiones como método de respaldo

## [2.0.0] - 2023-05-10

### Añadido
- Implementación de nuevas funcionalidades de análisis de piel
- SkinAnalyzer para analizar condición de piel, lunares y tono
- Modelos de datos para almacenar resultados (SkinAnalysisResult, MoleAnalysisResult, SkinToneResult)
- Servicio SkinService para coordinar los análisis
- Router con endpoints REST para acceder a las funcionalidades
- Configuración y dependencias necesarias para el análisis de piel 