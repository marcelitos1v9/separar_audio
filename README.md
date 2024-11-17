# Separador de Áudio com Spleeter

Este projeto implementa um sistema automatizado de separação de áudio usando a biblioteca Spleeter, que permite dividir músicas em suas diferentes faixas (vocais, bateria, baixo e outros instrumentos).

## Funcionalidades

- Monitoramento automático de uma pasta de entrada
- Processamento de arquivos WAV
- Separação em 4 stems (faixas):
  - Vocais
  - Bateria
  - Baixo
  - Outros instrumentos
- Remoção automática dos arquivos de entrada após processamento
- Sistema containerizado com Docker
- Processamento em alta qualidade (16kHz)

## Pré-requisitos

- Docker
- Docker Compose

## Instalação e Execução

1. Clone este repositório:
   ```bash
   git clone https://github.com/marcelitos1v9/separar_audio.git
   cd separar_audio
   ```

2. Inicie os containers:
   ```bash
   docker-compose up -d
   ```

3. O sistema estará pronto para uso quando você ver a mensagem "Aguardando por arquivos WAV..."

## Como Usar

1. Coloque seus arquivos WAV na pasta `input/`
2. O sistema detectará automaticamente os novos arquivos
3. O processamento começará imediatamente
4. Os arquivos separados serão salvos na pasta `output/` em uma subpasta com o nome do arquivo original
5. O arquivo original será removido após o processamento

## Fluxo de Processamento

1. **Monitoramento**: O sistema monitora constantemente a pasta `input/` por novos arquivos WAV
2. **Detecção**: Quando um novo arquivo é detectado, o sistema aguarda 2 segundos para garantir que a cópia foi finalizada
3. **Processamento**: O Spleeter processa o arquivo usando o modelo 4stems-16kHz
4. **Separação**: O áudio é dividido em 4 faixas distintas:
   - `vocals.wav`: Contém apenas os vocais
   - `drums.wav`: Contém apenas a bateria
   - `bass.wav`: Contém apenas o baixo
   - `other.wav`: Contém os demais instrumentos
5. **Finalização**: O arquivo original é removido e o sistema volta a monitorar por novos arquivos

## Observações Importantes

- Apenas arquivos WAV são suportados
- O primeiro processamento pode demorar mais devido ao download do modelo
- Os arquivos processados são salvos em alta qualidade (16kHz)
- O sistema reinicia automaticamente em caso de falhas
