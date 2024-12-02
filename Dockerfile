# Usa una imagen base de Python 3.11
FROM python:3.11-slim

# Instala las herramientas necesarias para crear entornos virtuales y dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3-venv \
    libmariadb-dev \
    build-essential \
    pkg-config

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Crea el entorno virtual y instala las dependencias
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Copia el resto de los archivos del proyecto al contenedor
COPY . /app/

# Establece la variable de entorno para usar el entorno virtual
ENV PATH="/opt/venv/bin:$PATH"

# Expone el puerto en el que Gunicorn escuchará
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "proyecto.wsgi:application", "--bind", "0.0.0.0:8000"]
