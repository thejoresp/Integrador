#!/bin/bash
# Script para levantar el backend en entorno de nube/producción
export ENV_FILE=backend/.env.cloud
export $(grep -v '^#' $ENV_FILE | xargs)
uvicorn backend.main:app --host 0.0.0.0 --port 8080 