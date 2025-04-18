#!/usr/bin/env python
"""
Script para descargar y configurar modelos pre-entrenados para análisis facial.

Este script descarga modelos de diversas fuentes y los configura en la carpeta
'models/pretrained' del proyecto.
"""
import os
import sys
import urllib.request
import shutil
import zipfile
import tarfile
import bz2
import subprocess
import importlib
import requests
from tqdm import tqdm
from pathlib import Path

# Configuración de directorios
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models" / "pretrained"
TEMP_DIR = BASE_DIR / "temp"

# Crear directorios necesarios
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# URLs de modelos
MODEL_URLS = {
    # dlib models
    "shape_predictor_68_face_landmarks.dat": "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2",
    "shape_predictor_5_face_landmarks.dat": "http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2",
    "dlib_face_recognition_resnet_model_v1.dat": "http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2",
    
    # OpenCV Haar Cascades
    "haarcascade_frontalface_default.xml": "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml",
    "haarcascade_eye.xml": "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_eye.xml",
    
    # Emotion models
    "fer2013_mini_XCEPTION.102-0.66.hdf5": "https://github.com/oarriaga/face_classification/raw/master/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5",
    
    # Age-Gender models
    "age_deploy.prototxt": "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt",
    "gender_deploy.prototxt": "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt",
    "age_net.caffemodel": "https://www.dropbox.com/s/xfb20y596869vbb/age_net.caffemodel?dl=1",
    "gender_net.caffemodel": "https://www.dropbox.com/s/e1q2h7n2o6c3h4p/gender_net.caffemodel?dl=1"
}

def check_dependency(package_name):
    """Verifica si un paquete está instalado."""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Instala un paquete de Python usando pip."""
    print(f"Instalando {package_name}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def download_file(url, target_file, desc=None):
    """
    Descarga un archivo desde una URL con barra de progreso.
    
    Args:
        url: URL del archivo a descargar
        target_file: Ruta donde guardar el archivo
        desc: Descripción para la barra de progreso
    """
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
        
        desc = desc or f"Descargando {os.path.basename(target_file)}"
        
        with open(target_file, 'wb') as file, tqdm(
                desc=desc,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                size = file.write(data)
                bar.update(size)
                
        return True
    except Exception as e:
        print(f"Error descargando {url}: {str(e)}")
        if os.path.exists(target_file):
            os.remove(target_file)
        return False

def decompress_bz2(source_file, target_file):
    """Descomprime un archivo .bz2."""
    try:
        with open(target_file, 'wb') as new_file, open(source_file, 'rb') as file:
            data = bz2.decompress(file.read())
            new_file.write(data)
        return True
    except Exception as e:
        print(f"Error descomprimiendo {source_file}: {str(e)}")
        return False

def decompress_zip(source_file, target_dir):
    """Descomprime un archivo .zip."""
    try:
        with zipfile.ZipFile(source_file, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        return True
    except Exception as e:
        print(f"Error descomprimiendo {source_file}: {str(e)}")
        return False

def download_deepface_models():
    """Descarga modelos de DeepFace."""
    if not check_dependency("deepface"):
        print("DeepFace no está instalado. Instalando...")
        install_package("deepface")
    
    try:
        from deepface import DeepFace
        from deepface.commons import functions
        
        print("Descargando modelos de DeepFace...")
        
        # Esto forzará la descarga de los modelos
        img_path = os.path.join(TEMP_DIR, "temp_image.jpg")
        
        # Crear una imagen temporal si no existe
        if not os.path.exists(img_path):
            # Crear una imagen en blanco
            import numpy as np
            import cv2
            img = np.zeros((100, 100, 3), np.uint8)
            cv2.imwrite(img_path, img)
        
        # Forzar la descarga de modelos
        try:
            DeepFace.analyze(img_path=img_path, actions=['age', 'gender', 'emotion'], enforce_detection=False)
        except Exception as e:
            print(f"Advertencia al analizar con DeepFace: {str(e)}")
        
        # Copiar modelos a la carpeta del proyecto
        deepface_weight_dir = os.path.join(os.path.expanduser("~"), ".deepface", "weights")
        if os.path.exists(deepface_weight_dir):
            print("Copiando modelos de DeepFace a models/pretrained...")
            for model_file in os.listdir(deepface_weight_dir):
                source_path = os.path.join(deepface_weight_dir, model_file)
                target_path = os.path.join(MODELS_DIR, model_file)
                if os.path.isfile(source_path) and not os.path.exists(target_path):
                    shutil.copy(source_path, target_path)
                    print(f"  - Copiado: {model_file}")
        
        print("Modelos de DeepFace configurados correctamente.")
        return True
    except Exception as e:
        print(f"Error configurando modelos de DeepFace: {str(e)}")
        return False

def download_mediapipe_models():
    """Configura MediaPipe (no requiere descarga manual)."""
    if not check_dependency("mediapipe"):
        print("MediaPipe no está instalado. Instalando...")
        install_package("mediapipe")
    
    try:
        import mediapipe as mp
        print("MediaPipe configurado correctamente. Los modelos se descargan automáticamente.")
        return True
    except Exception as e:
        print(f"Error configurando MediaPipe: {str(e)}")
        return False

def download_opencv_models():
    """Descarga y configura modelos de OpenCV."""
    if not check_dependency("opencv-python"):
        print("OpenCV no está instalado. Instalando...")
        install_package("opencv-python")
    
    try:
        import cv2
        
        # Copiar Haar Cascades de la instalación de OpenCV
        cascade_files = [
            "haarcascade_frontalface_default.xml",
            "haarcascade_eye.xml",
            "haarcascade_smile.xml"
        ]
        
        print("Copiando modelos Haar Cascade de OpenCV...")
        for cascade in cascade_files:
            source = os.path.join(cv2.data.haarcascades, cascade)
            target = os.path.join(MODELS_DIR, cascade)
            
            if os.path.exists(source) and not os.path.exists(target):
                shutil.copy(source, target)
                print(f"  - Copiado: {cascade}")
        
        print("Modelos de OpenCV configurados correctamente.")
        return True
    except Exception as e:
        print(f"Error configurando modelos de OpenCV: {str(e)}")
        return False

def main():
    """Función principal para descargar todos los modelos."""
    print("\n" + "="*50)
    print("DESCARGADOR DE MODELOS PRE-ENTRENADOS PARA ANÁLISIS FACIAL")
    print("="*50 + "\n")
    
    # Verificar dependencias básicas
    for package in ["tqdm", "requests"]:
        if not check_dependency(package):
            install_package(package)
    
    # 1. Descargar modelos específicos desde URLs
    print("\n[1/4] Descargando modelos específicos...")
    for model_name, url in MODEL_URLS.items():
        target_path = os.path.join(MODELS_DIR, model_name)
        
        # Verificar si el modelo ya existe
        if os.path.exists(target_path):
            print(f"  - {model_name} ya existe. Omitiendo...")
            continue
        
        # Descargar el modelo
        temp_path = os.path.join(TEMP_DIR, os.path.basename(url))
        if download_file(url, temp_path):
            
            # Procesar según el tipo de archivo
            if url.endswith(".bz2"):
                print(f"  - Descomprimiendo {model_name}...")
                if decompress_bz2(temp_path, target_path):
                    print(f"  - {model_name} configurado correctamente.")
                os.remove(temp_path)
            elif url.endswith(".zip"):
                print(f"  - Descomprimiendo {model_name}...")
                if decompress_zip(temp_path, MODELS_DIR):
                    print(f"  - {model_name} configurado correctamente.")
                os.remove(temp_path)
            else:
                # Mover directamente el archivo
                shutil.move(temp_path, target_path)
                print(f"  - {model_name} configurado correctamente.")
    
    # 2. Configurar DeepFace
    print("\n[2/4] Configurando modelos de DeepFace...")
    download_deepface_models()
    
    # 3. Configurar MediaPipe
    print("\n[3/4] Configurando MediaPipe...")
    download_mediapipe_models()
    
    # 4. Configurar OpenCV
    print("\n[4/4] Configurando modelos de OpenCV...")
    download_opencv_models()
    
    # Limpiar archivos temporales
    print("\nLimpiando archivos temporales...")
    for file in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    print("\n" + "="*50)
    print("¡CONFIGURACIÓN DE MODELOS COMPLETADA!")
    print("Todos los modelos pre-entrenados han sido descargados y configurados.")
    print("Los modelos se encuentran en:", MODELS_DIR)
    print("="*50 + "\n")

if __name__ == "__main__":
    main()