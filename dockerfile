# Usar una imagen base con Python y soporte para Torch
FROM python:3.10

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copiar los archivos del proyecto al contenedor
COPY requirements.txt .
COPY inference.py /app/inference.py
COPY best.pt /app/best.pt


# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Comando de ejecución por defecto
CMD ["python", "inference.py"]
