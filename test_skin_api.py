import requests
import os
import sys
import json
from pathlib import Path

def test_skin_endpoint(endpoint, image_path):
    """Prueba un endpoint de análisis de piel con una imagen"""
    
    print(f"Probando endpoint {endpoint} con la imagen: {image_path}")
    
    # Verificar que la imagen existe
    if not os.path.exists(image_path):
        print(f"ERROR: La imagen no existe en: {image_path}")
        return False
        
    # Verificar tamaño del archivo
    file_size = os.path.getsize(image_path)
    print(f"Tamaño del archivo: {file_size} bytes")
    
    if file_size == 0:
        print(f"ERROR: El archivo está vacío: {image_path}")
        return False
    
    # Realizar petición
    try:
        base_url = "http://localhost:8000"
        
        # Si el endpoint es "legacy", usamos la ruta /analyze (compatibilidad)
        if endpoint == "legacy":
            url = f"{base_url}/analyze"
            endpoint_name = "/analyze (endpoint de compatibilidad)"
        else:
            url = f"{base_url}/skin/analyze/{endpoint}"
            endpoint_name = f"/skin/analyze/{endpoint}"
            
        print(f"Enviando petición a: {url}")
        
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
        
        print(f"Código de estado: {response.status_code}")
        
        if response.status_code == 200:
            # Petición exitosa
            try:
                result = response.json()
                print("Respuesta exitosa:")
                print(json.dumps(result, indent=2))
                return True
            except json.JSONDecodeError:
                print(f"ERROR: No se pudo decodificar la respuesta JSON: {response.text}")
                return False
        else:
            # Error en la petición
            print(f"ERROR ({response.status_code}): {response.text}")
            try:
                error_data = response.json()
                print(f"Detalle del error: {error_data.get('detail', 'No hay detalles adicionales')}")
            except Exception:
                print(f"Respuesta de error: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"ERROR de conexión: {str(e)}")
        return False
    except Exception as e:
        print(f"ERROR inesperado: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

def run_test(image_path):
    """Ejecuta todas las pruebas para una sola imagen"""
    
    print(f"\n{'=' * 50}")
    print(f"Probando con la imagen: {image_path}")
    print(f"{'=' * 50}")
    
    endpoints = [
        "condition",
        "moles",
        "tone",
        "complete",
        "legacy"  # Prueba para el endpoint /analyze (compatibilidad)
    ]
    
    results = {}
    for endpoint in endpoints:
        print(f"\n{'-' * 30}")
        print(f"Endpoint: {endpoint}")
        print(f"{'-' * 30}")
        
        success = test_skin_endpoint(endpoint, image_path)
        results[endpoint] = success
        print(f"Resultado: {'ÉXITO' if success else 'FALLO'}")
    
    # Mostrar resumen
    print(f"\n{'-' * 30}")
    print("RESUMEN DE PRUEBAS:")
    print(f"{'-' * 30}")
    for endpoint, success in results.items():
        print(f"{endpoint}: {'✓' if success else '✗'}")
    
    return all(results.values())

if __name__ == "__main__":
    # Usar una imagen de prueba
    test_images = [
        "uploads/f92cf379-f462-4af0-8eb3-c041f6243912.jpg",
        "uploads/8e32f54a-a47c-4956-9be0-7fee4e46d546.jpg",
    ]
    
    all_success = True
    for img_path in test_images:
        success = run_test(img_path)
        all_success = all_success and success
    
    print(f"\n{'=' * 50}")
    print(f"RESULTADO FINAL: {'ÉXITO' if all_success else 'AL MENOS UN FALLO'}")
    print(f"{'=' * 50}") 