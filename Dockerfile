# 1. Imagen base estable
FROM python:3.11-slim

# 2. Instalamos dependencias del sistema
# git: necesario para setuptools_scm / PyScaffold
# build-essential: por si alguna dependencia de pip necesita compilar C
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Directorio de trabajo
WORKDIR /app

# 4. Copiamos archivos de configuración base
COPY setup.cfg pyproject.toml requirements.txt ./
COPY README.rst* LICENSE.txt* ./

# 5. Copiamos el código fuente (importante para que el modo editable -e funcione)
COPY src ./src

# 6. Evita que setuptools-scm falle al no encontrar el historial de Git
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0.1
# Asegura que los logs de Python se vean en tiempo real en la terminal
ENV PYTHONUNBUFFERED=1

# 7. Instalamos dependencias + Herramientas de Test
# Forzamos la instalación de pytest para asegurar que el binario esté en /usr/local/bin
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt pytest pytest-cov

# 8. Copiamos el resto del proyecto
COPY . .

# 9. Instalación final del SDK en el contenedor
# Esto registra el comando 'apimarket' basándose en tu setup.cfg
RUN pip install --no-cache-dir -e .

# 10. Comando por defecto
# Usamos el binario instalado por el SDK
CMD ["apimarket"]