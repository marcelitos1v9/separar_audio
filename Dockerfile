FROM python:3.8-slim

# Instalar dependências essenciais
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar Spleeter com versão específica e dependências
RUN pip install --no-cache-dir spleeter==2.3.0 tensorflow==2.5.0

# Criar diretórios necessários
RUN mkdir -p /model /app/input /app/output /app/temp

# Configurar variáveis de ambiente
ENV MODEL_PATH=/model \
    PYTHONUNBUFFERED=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    CUDA_VISIBLE_DEVICES=-1

# Pré-baixar o modelo
COPY download_model.py /
RUN python /download_model.py

WORKDIR /app
COPY . .

# Script de verificação de saúde
COPY healthcheck.py /
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD python /healthcheck.py

# Entrypoint com retry
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"] 