# Usar Python 3.11 slim como imagen base
FROM python:3.11-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación
COPY . .

# Copiar y dar permisos de ejecución al script de entrada
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Puerto expuesto (Railway usa la variable PORT, pero 8000 es el default)
EXPOSE 8000

# Comando para ejecutar la aplicación a través del script
CMD ["./entrypoint.sh"]
