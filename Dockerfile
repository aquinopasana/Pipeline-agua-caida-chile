# 1. Imagen base ligera de Python 3.11
FROM python:3.11-slim

# 2. Evitar que Python genere archivos .pyc en el contenedor y asegurar logs inmediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiar e instalar las dependencias primero (aprovecha la caché de Docker)
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código del proyecto al directorio de trabajo
COPY . .

# 6. Comando por defecto para ejecutar el pipeline al iniciar el contenedor
CMD ["python", "src/main.py"]