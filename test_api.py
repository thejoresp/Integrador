import requests
import sys
import os
from pathlib import Path
import mimetypes

def test_api():
    """Prueba la API de análisis de piel con una imagen local"""
    
    # URL de la API
    base_url = "http://localhost:8000"
    test_endpoint = f"{base_url}/skin/analyze/condition"
    
    # Buscar una imagen para probar
    uploads_dir = Path("uploads")
    
    if not uploads_dir.exists():
        print(f"Error: Directorio de uploads no encontrado: {uploads_dir}")
        return
    
    # Encontrar la primera imagen jpg en el directorio
    image_file = None
    for f in uploads_dir.glob("*.jpg"):
        image_file = f
        break
    
    if not image_file:
        print("Error: No se encontró ninguna imagen jpg en el directorio uploads")
        return
    
    print(f"Probando API con imagen: {image_file}")
    print(f"Tamaño de archivo: {os.path.getsize(image_file)} bytes")
    
    try:
        # Preparar el archivo
        mime_type, _ = mimetypes.guess_type(str(image_file))
        
        with open(image_file, 'rb') as f:
            files = {'file': (image_file.name, f, mime_type)}
            
            # Hacer la petición
            print(f"Enviando petición a: {test_endpoint}")
            response = requests.post(test_endpoint, files=files)
            
            # Mostrar resultados
            print(f"Código de estado: {response.status_code}")
            if response.status_code == 200:
                print("Respuesta exitosa:")
                print(response.json())
            else:
                print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"Error al probar la API: {str(e)}")

if __name__ == "__main__":
    test_api() 