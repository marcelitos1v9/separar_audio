FROM python:3.8

# Instalar FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Instalar Spleeter
RUN pip install spleeter

WORKDIR /app

COPY . .

CMD ["python", "app.py"] 