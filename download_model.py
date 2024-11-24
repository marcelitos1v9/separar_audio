import os
import sys
import time
from spleeter.separator import Separator

def download_model():
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        try:
            print(f"Tentativa {attempt + 1} de download do modelo...")
            os.environ['MODEL_PATH'] = '/model'
            separator = Separator('spleeter:4stems-16kHz')
            print("Modelo baixado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro no download: {str(e)}")
            attempt += 1
            if attempt < max_attempts:
                print("Tentando novamente em 5 segundos...")
                time.sleep(5)
    
    print("Falha no download do modelo após várias tentativas")
    return False

if __name__ == "__main__":
    if not download_model():
        sys.exit(1)