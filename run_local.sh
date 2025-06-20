#!/bin/bash
# Script para levantar el backend en entorno local
export ENV_FILE=backend/.env.local
export $(grep -v '^#' $ENV_FILE | xargs)
uvicorn backend.main:app --host 0.0.0.0 --port 8080 --reload 