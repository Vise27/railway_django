# Usa una imagen base de Python 3.11
FROM python:3.11-slim

# Instala las herramientas necesarias para crear entornos virtuales y dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3-venv \
    libmysqlclient-dev \
    build-essential \
    pkg-config

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia el resto de los archivos del proyecto al contenedor
COPY . /app/

# Expone el puerto en el que Gunicorn escuchará
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "proyecto.wsgi:application", "--bind", "0.0.0.0:8000"]
