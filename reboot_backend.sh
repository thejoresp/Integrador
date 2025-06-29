#!/bin/bash

# Eliminar cualquier contenedor llamado 'pielsana-backend'
sudo docker rm -f pielsana-backend 2>/dev/null

# Eliminar la imagen 'pielsana-backend' si existe
imagen_id=$(docker images -q pielsana-backend)
if [ -n "$imagen_id" ]; then
  echo "Eliminando la imagen 'pielsana-backend'..."
  sudo docker rmi -f pielsana-backend
fi

echo "Construyendo la imagen Docker del backend..."
sudo docker build -t pielsana-backend -f backend/Dockerfile .

echo "Ejecutando el backend en Docker..."
sudo docker run -d --rm --name pielsana-backend -p 8080:8080 pielsana-backend 