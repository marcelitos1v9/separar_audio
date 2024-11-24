from spleeter.separator import Separator
import os
import time
import sys
import shutil
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self):
        self.setup_environment()
        self.initialize_separator()
        self.arquivos_processados = set()
        self.erros_arquivos = {}
        
    def setup_environment(self):
        """Configurar ambiente e verificar requisitos"""
        try:
            logger.info("Configurando ambiente...")
            
            # Verificar FFmpeg
            if os.system("ffmpeg -version") != 0:
                raise Exception("FFmpeg não encontrado")
                
            # Configurar MODEL_PATH
            os.environ['MODEL_PATH'] = '/model'
            
            # Verificar e criar diretórios
            for path in ['/app/input', '/app/output', '/model']:
                if not os.path.exists(path):
                    os.makedirs(path)
                    
            logger.info("Ambiente configurado com sucesso")
        except Exception as e:
            logger.error(f"Erro na configuração do ambiente: {str(e)}")
            sys.exit(1)
    
    def initialize_separator(self):
        """Inicializar o Separator com retry"""
        max_tentativas = 3
        tentativa = 0
        
        while tentativa < max_tentativas:
            try:
                logger.info(f"Tentativa {tentativa + 1} de inicializar Separator...")
                self.separator = Separator('spleeter:4stems-16kHz', multiprocess=False)
                logger.info("Separator inicializado com sucesso!")
                return
            except Exception as e:
                tentativa += 1
                logger.error(f"Erro ao inicializar Separator: {str(e)}")
                if tentativa == max_tentativas:
                    logger.error("Falha crítica na inicialização do Separator")
                    sys.exit(1)
                time.sleep(5)
    
    def verificar_arquivo_wav(self, arquivo_path):
        """Verificar se o arquivo WAV é válido"""
        try:
            if not os.path.exists(arquivo_path):
                return False
                
            tamanho = os.path.getsize(arquivo_path)
            if tamanho < 44:  # Tamanho mínimo do cabeçalho WAV
                return False
                
            # Verificar cabeçalho WAV
            with open(arquivo_path, 'rb') as f:
                header = f.read(4)
                if header != b'RIFF':
                    return False
                    
            return True
        except Exception:
            return False
    
    def processar_audio(self, arquivo_entrada):
        """Processar um arquivo de áudio"""
        nome_arquivo = os.path.basename(arquivo_entrada)
        
        # Verificar se arquivo já teve muitos erros
        if self.erros_arquivos.get(arquivo_entrada, 0) >= 3:
            logger.error(f"Arquivo {nome_arquivo} ignorado após múltiplas falhas")
            return
            
        try:
            if not self.verificar_arquivo_wav(arquivo_entrada):
                logger.error(f"Arquivo inválido: {nome_arquivo}")
                return
                
            diretorio_saida = f"/app/output/{os.path.splitext(nome_arquivo)[0]}"
            
            logger.info(f"Iniciando processamento: {nome_arquivo}")
            time.sleep(2)  # Aguardar cópia completa
            
            # Criar backup temporário
            backup_path = f"{arquivo_entrada}.bak"
            shutil.copy2(arquivo_entrada, backup_path)
            
            self.separator.separate_to_file(arquivo_entrada, diretorio_saida)
            logger.info(f"Áudio processado com sucesso: {diretorio_saida}")
            
            # Remover arquivos
            os.remove(arquivo_entrada)
            os.remove(backup_path)
            logger.info(f"Arquivo processado e removido: {nome_arquivo}")
            
        except Exception as e:
            logger.error(f"Erro ao processar {nome_arquivo}: {str(e)}")
            # Restaurar backup se existir
            if os.path.exists(backup_path):
                shutil.move(backup_path, arquivo_entrada)
            # Incrementar contador de erros
            self.erros_arquivos[arquivo_entrada] = self.erros_arquivos.get(arquivo_entrada, 0) + 1
    
    def monitorar_pasta(self):
        """Monitorar pasta de entrada continuamente"""
        logger.info("Iniciando monitoramento...")
        
        while True:
            try:
                arquivos = [f for f in os.listdir('/app/input') 
                          if f.lower().endswith('.wav')]
                
                for arquivo in arquivos:
                    caminho_completo = os.path.join('/app/input', arquivo)
                    
                    if caminho_completo not in self.arquivos_processados:
                        logger.info(f"Novo arquivo detectado: {arquivo}")
                        self.processar_audio(caminho_completo)
                        self.arquivos_processados.add(caminho_completo)
                
                # Limpar registros de arquivos processados
                self.arquivos_processados = {f for f in self.arquivos_processados 
                                          if os.path.exists(f)}
                self.erros_arquivos = {k:v for k,v in self.erros_arquivos.items() 
                                     if os.path.exists(k)}
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Erro no monitoramento: {str(e)}")
                time.sleep(5)  # Esperar mais tempo em caso de erro

if __name__ == "__main__":
    try:
        logger.info("Iniciando aplicação...")
        processor = AudioProcessor()
        processor.monitorar_pasta()
    except KeyboardInterrupt:
        logger.info("Aplicação encerrada pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}")
        sys.exit(1)
