# Usa una imagen oficial de Python como base
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencias primero para aprovechar el cache de Docker
COPY backend/requirements.txt ./requirements.txt

# Instala las dependencias del sistema necesarias 
RUN apt-get update && \
    apt-get install -y build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia la carpeta backend al contenedor
COPY backend ./backend

# Expone el puerto que usará Uvicorn
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"] 