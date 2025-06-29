#!/bin/bash

# Verificar si existe la imagen 'pielsana-backend'
imagen_id=$(docker images -q pielsana-backend)

construir_imagen=true

if [ -n "$imagen_id" ]; then
  read -p "¿Quieres eliminar la imagen 'pielsana-backend'? (s/N): " respuesta
  if [[ "$respuesta" =~ ^[sS]$ ]]; then
    echo "Eliminando la imagen 'pielsana-backend'..."
    sudo docker rmi -f pielsana-backend
  else
    construir_imagen=false
  fi
fi

if [ "$construir_imagen" = true ]; then
  echo "Construyendo la imagen Docker del backend..."
  sudo docker build -t pielsana-backend -f backend/Dockerfile .
fi

# Ejecutar el contenedor
echo "Ejecutando el backend en Docker..."
sudo docker run -d --rm --name pielsana-backend -p 8080:8080 pielsana-backend 