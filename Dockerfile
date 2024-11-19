FROM python:3.8

# Instalar FFmpeg e dependências necessárias
RUN apt-get update && apt-get install -y ffmpeg

# Instalar Spleeter e watchdog
RUN pip install spleeter watchdog

# Criar diretório para o modelo
RUN mkdir -p /model

# Definir variável de ambiente para o modelo
ENV MODEL_PATH=/model
ENV PYTHONUNBUFFERED=1

# Pré-baixar o modelo de forma explícita
RUN python -c "from spleeter.separator import Separator; \
    import os; \
    os.environ['MODEL_PATH'] = '/model'; \
    print('Iniciando download do modelo...'); \
    separator = Separator('spleeter:4stems-16kHz'); \
    print('Modelo baixado com sucesso!')"

WORKDIR /app

# Criar diretórios para input e output
RUN mkdir -p /app/input /app/output

COPY . .

RUN chmod -R 777 /app/input
RUN chmod -R 777 /app/output

# Adicione um script de inicialização
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"] 