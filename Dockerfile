FROM python:3.8-slim

# Instalar FFmpeg e dependências essenciais
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar Spleeter com suas dependências
RUN pip install --no-cache-dir spleeter==2.3.0

# Criar diretórios necessários
RUN mkdir -p /model /app/input /app/output

# Definir variável de ambiente
ENV MODEL_PATH=/model \
    PYTHONUNBUFFERED=1

# Pré-baixar o modelo com retry
COPY download_model.py /
RUN python /download_model.py

WORKDIR /app
COPY . .

# Verificar ambiente antes de iniciar
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "from spleeter.separator import Separator; Separator('spleeter:4stems-16kHz')" || exit 1

CMD ["python", "app.py"] 