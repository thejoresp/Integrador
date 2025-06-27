#!/bin/bash

# Eliminar todos los contenedores (parados y corriendo)
echo "Eliminando todos los contenedores..."
docker rm -f $(docker ps -aq) 2>/dev/null

# Eliminar todas las imágenes
echo "Eliminando todas las imágenes..."
docker rmi -f $(docker images -q) 2>/dev/null

# Construir la imagen del backend
echo "Construyendo la imagen Docker del backend..."
sudo docker build -t pielsana-backend -f backend/Dockerfile .

# Ejecutar el contenedor
echo "Ejecutando el backend en Docker..."
sudo docker run -p 8080:8080 pielsana-backend 