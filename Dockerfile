# Usa una imagen base oficial de Python como punto de partida
FROM python:3.8-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requisitos primero para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install safrs
RUN pip install -r requirements.txt

# Copia el resto del código fuente de la aplicación al contenedor
COPY . .

# Expone el puerto que tu aplicación utiliza, ajusta este valor si tu script necesita comunicarse a través de un puerto específico
EXPOSE 8000

# Comando para ejecutar la aplicación. Ajusta según sea necesario.
CMD ["python", "examples/demo_relationship.py", "0.0.0.0", "8000"]