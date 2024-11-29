#!/bin/bash
set -e

# Função para verificar requisitos
check_requirements() {
    # Verificar FFmpeg
    if ! command -v ffmpeg &> /dev/null; then
        echo "FFmpeg não encontrado. Tentando instalar..."
        apt-get update && apt-get install -y ffmpeg
    fi

    # Verificar modelo
    if [ ! -d "/model" ] || [ -z "$(ls -A /model)" ]; then
        echo "Modelo não encontrado. Baixando..."
        python /download_model.py
    fi
}

# Função para tentar iniciar a aplicação
start_application() {
    local max_attempts=5
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        echo "Tentativa $attempt de iniciar a aplicação..."
        
        if python app.py; then
            return 0
        fi

        echo "Falha na tentativa $attempt. Aguardando antes de tentar novamente..."
        sleep 5
        attempt=$((attempt + 1))
    done

    return 1
}

# Principal
main() {
    echo "Verificando requisitos..."
    check_requirements

    echo "Iniciando aplicação..."
    if ! start_application; then
        echo "Falha ao iniciar aplicação após várias tentativas"
        exit 1
    fi
}

main 