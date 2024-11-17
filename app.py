from spleeter.separator import Separator
import os

def separar_audio(arquivo_entrada, diretorio_saida):
    # Criar diretório de saída se não existir
    os.makedirs(diretorio_saida, exist_ok=True)
    
    # Inicializar o separador
    separator = Separator('spleeter:4stems', multiprocess=False)
    
    # Realizar a separação
    separator.separate_to_file(arquivo_entrada, diretorio_saida)
    
    print(f"Áudio separado com sucesso! Arquivos salvos em: {diretorio_saida}")

if __name__ == "__main__":
    # Caminhos adaptados para Docker
    arquivo_entrada = "/app/input/audio.wav"
    diretorio_saida = "/app/output"
    
    separar_audio(arquivo_entrada, diretorio_saida)
