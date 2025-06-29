#!/bin/bash

# Verificar si existe la imagen 'pielsana-backend'
imagen_id=$(docker images -q pielsana-backend)

if [ -n "$imagen_id" ]; then
  read -p "¿Quieres eliminar la imagen 'pielsana-backend'? (s/N): " respuesta
  if [[ "$respuesta" =~ ^[sS]$ ]]; then
    echo "Eliminando la imagen 'pielsana-backend'..."
    sudo docker rmi -f pielsana-backend
    echo "Construyendo la imagen Docker del backend..."
    sudo docker build -t pielsana-backend -f backend/Dockerfile .
  else
    echo "Usando la imagen existente 'pielsana-backend' para crear el contenedor."
  fi
else
  echo "No existe la imagen 'pielsana-backend'. Construyendo..."
  sudo docker build -t pielsana-backend -f backend/Dockerfile .
fi

# Ejecutar el contenedor
echo "Ejecutando el backend en Docker..."
sudo docker run -d --rm --name pielsana-backend -p 8080:8080 pielsana-backend 