#!/bin/bash

# Script para exponer el backend de FastAPI en Docker usando ngrok
# Uso: ./ngrok.sh

# Verifica que el archivo ngrok_token.txt exista
if [ ! -f ngrok_token.txt ]; then
    echo "El archivo ngrok_token.txt no existe. Por favor, crea el archivo con tu authtoken de ngrok."
    exit 1
fi

# Lee el token desde el archivo
NGROK_TOKEN=$(cat ngrok_token.txt)

# Verifica si ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo "ngrok no está instalado. Instalando vía Apt..."
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list \
    && sudo apt update \
    && sudo apt install ngrok -y
else
    echo "ngrok ya está instalado."
fi

# Configura el authtoken si no está configurado
if ! grep -q "$NGROK_TOKEN" ~/.ngrok2/ngrok.yml 2>/dev/null; then
    echo "Configurando authtoken de ngrok..."
    ngrok config add-authtoken $NGROK_TOKEN
fi

# Verifica si el backend está corriendo en Docker
if ! sudo docker ps | grep -q "pielsana-backend"; then
    echo "El backend no está corriendo en Docker. Inícialo antes de usar ngrok."
    exit 1
fi

# Inicia ngrok en el puerto 8080
ngrok http 8080
