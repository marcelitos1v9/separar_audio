from spleeter.separator import Separator
import os
import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def print_debug(message):
    """Função auxiliar para garantir que as mensagens sejam impressas"""
    print(message, flush=True)

class AudioFileHandler(FileSystemEventHandler):
    def __init__(self, processor):
        self.processor = processor
        
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.wav'):
            print_debug(f"\nNovo arquivo detectado: {event.src_path}")
            self.processor.processar_audio(event.src_path)

class AudioProcessor:
    def __init__(self):
        print_debug("Iniciando AudioProcessor...")
        print_debug("Configurando variável de ambiente MODEL_PATH...")
        os.environ['MODEL_PATH'] = '/model'
        
        print_debug("Iniciando carregamento do Separator...")
        try:
            print_debug("Tentando carregar o modelo...")
            self.separator = Separator('spleeter:4stems-16kHz', multiprocess=False)
            print_debug("Separator inicializado com sucesso!")
        except Exception as e:
            print_debug(f"ERRO CRÍTICO ao inicializar Separator: {str(e)}")
            sys.exit(1)
        
        self.arquivos_processados = set()
    
    def processar_audio(self, arquivo_entrada):
        try:
            # Aguarda um momento para garantir que o arquivo foi completamente copiado
            time.sleep(2)
            
            if not os.path.exists(arquivo_entrada):
                print_debug(f"Arquivo não encontrado: {arquivo_entrada}")
                return
                
            nome_arquivo = os.path.basename(arquivo_entrada)
            diretorio_saida = f"/app/output/{os.path.splitext(nome_arquivo)[0]}"
            
            print_debug(f"\nIniciando processamento de {nome_arquivo}...")
            
            tamanho = os.path.getsize(arquivo_entrada)
            print_debug(f"Tamanho do arquivo: {tamanho} bytes")
            
            if tamanho == 0:
                print_debug("Arquivo vazio, ignorando...")
                return
            
            print_debug("Iniciando separação do áudio...")
            self.separator.separate_to_file(arquivo_entrada, diretorio_saida)
            print_debug(f"Áudio processado com sucesso! Arquivos salvos em: {diretorio_saida}")
            
            os.remove(arquivo_entrada)
            print_debug(f"Arquivo de entrada removido: {arquivo_entrada}")
            print_debug("\nAguardando novos arquivos WAV...")
            
        except Exception as e:
            print_debug(f"Erro ao processar {nome_arquivo}: {str(e)}")
    
    def processar_arquivos_existentes(self, pasta_entrada):
        """Processa arquivos que já existem na pasta de entrada"""
        try:
            arquivos = [f for f in os.listdir(pasta_entrada) if f.lower().endswith('.wav')]
            if arquivos:
                print_debug(f"Encontrados {len(arquivos)} arquivos existentes para processar")
                for arquivo in arquivos:
                    caminho_completo = os.path.join(pasta_entrada, arquivo)
                    if caminho_completo not in self.arquivos_processados:
                        self.processar_audio(caminho_completo)
                        self.arquivos_processados.add(caminho_completo)
        except Exception as e:
            print_debug(f"Erro ao processar arquivos existentes: {str(e)}")
    
    def monitorar_pasta(self):
        pasta_entrada = "/app/input"
        
        print_debug(f"\nVerificando pasta de entrada: {pasta_entrada}")
        print_debug(f"A pasta existe? {os.path.exists(pasta_entrada)}")
        print_debug(f"É um diretório? {os.path.isdir(pasta_entrada)}")
        
        # Processa arquivos existentes primeiro
        self.processar_arquivos_existentes(pasta_entrada)
        
        # Configura o observador de arquivos
        event_handler = AudioFileHandler(self)
        observer = Observer()
        observer.schedule(event_handler, pasta_entrada, recursive=False)
        observer.start()
        
        print_debug("\nMonitoramento iniciado. Aguardando por novos arquivos...")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print_debug("\nMonitoramento interrompido pelo usuário")
        
        observer.join()

if __name__ == "__main__":
    print_debug("Iniciando aplicação...")
    processor = AudioProcessor()
    
    try:
        processor.monitorar_pasta()
    except KeyboardInterrupt:
        print_debug("\nAplicação encerrada pelo usuário.")
    except Exception as e:
        print_debug(f"Erro fatal: {str(e)}")
        sys.exit(1)
