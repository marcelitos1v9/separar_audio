from spleeter.separator import Separator
import os
import time
import sys

class AudioProcessor:
    def __init__(self):
        print("Inicializando AudioProcessor...")
        print("Configurando variável de ambiente MODEL_PATH...")
        os.environ['MODEL_PATH'] = '/model'
        
        print("Iniciando carregamento do Separator...")
        try:
            print("Tentando carregar o modelo...")
            self.separator = Separator('spleeter:4stems-16kHz', multiprocess=False)
            print("Separator inicializado com sucesso!")
        except Exception as e:
            print(f"ERRO CRÍTICO ao inicializar Separator: {str(e)}")
            sys.exit(1)
        
        self.arquivos_processados = set()
    
    def processar_audio(self, arquivo_entrada):
        try:
            if not os.path.exists(arquivo_entrada):
                return
                
            nome_arquivo = os.path.basename(arquivo_entrada)
            diretorio_saida = f"/app/output/{os.path.splitext(nome_arquivo)[0]}"
            
            print(f"\nIniciando processamento de {nome_arquivo}...")
            
            # Aguardar um momento para garantir que o arquivo foi completamente copiado
            time.sleep(2)
            
            tamanho = os.path.getsize(arquivo_entrada)
            print(f"Tamanho do arquivo: {tamanho} bytes")
            
            if tamanho == 0:
                print("Arquivo vazio, ignorando...")
                return
            
            print("Iniciando separação do áudio...")
            self.separator.separate_to_file(arquivo_entrada, diretorio_saida)
            print(f"Áudio processado com sucesso! Arquivos salvos em: {diretorio_saida}")
            
            os.remove(arquivo_entrada)
            print(f"Arquivo de entrada removido: {arquivo_entrada}")
            print("\nAguardando novos arquivos WAV...")
            
        except Exception as e:
            print(f"Erro ao processar {nome_arquivo}: {str(e)}")
    
    def monitorar_pasta(self):
        pasta_entrada = "/app/input"
        
        if not os.path.exists(pasta_entrada):
            os.makedirs(pasta_entrada)
        
        print(f"Monitorando diretório: {pasta_entrada}")
        print("Aguardando por arquivos WAV...")
        
        while True:
            try:
                # Listar todos os arquivos WAV na pasta
                arquivos = [f for f in os.listdir(pasta_entrada) if f.lower().endswith('.wav')]
                
                for arquivo in arquivos:
                    caminho_completo = os.path.join(pasta_entrada, arquivo)
                    
                    # Processar apenas arquivos que ainda não foram processados
                    if caminho_completo not in self.arquivos_processados:
                        print(f"\nNovo arquivo detectado: {arquivo}")
                        self.processar_audio(caminho_completo)
                        self.arquivos_processados.add(caminho_completo)
                
                # Limpar arquivos processados que não existem mais
                self.arquivos_processados = {f for f in self.arquivos_processados if os.path.exists(f)}
                
                # Pequena pausa para não sobrecarregar o CPU
                time.sleep(1)
                
            except Exception as e:
                print(f"Erro durante monitoramento: {str(e)}")
                time.sleep(1)

if __name__ == "__main__":
    print("Iniciando aplicação...")
    processor = AudioProcessor()
    processor.monitorar_pasta()
