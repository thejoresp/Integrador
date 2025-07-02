#!/bin/bash

# Forzar la eliminación del contenedor llamado 'pielsana-backend' (si existe)
sudo docker rm -f pielsana-backend 2>/dev/null

# Forzar la eliminación de la imagen 'pielsana-backend' (si existe)
sudo docker rmi -f pielsana-backend 2>/dev/null

echo "Construyendo la imagen Docker del backend..."
sudo docker build -t pielsana-backend -f backend/Dockerfile .

echo "Ejecutando el backend en Docker..."
# sudo docker run -d --rm --name pielsana-backend -p 8080:8080 pielsana-backend 
sudo docker run -d --name pielsana-backend -p 8080:8080 pielsana-backend 