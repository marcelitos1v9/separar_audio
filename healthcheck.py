import os
import sys
from spleeter.separator import Separator

def check_health():
    try:
        # Verificar diretórios
        for path in ['/app/input', '/app/output', '/model']:
            if not os.path.exists(path):
                return False

        # Verificar modelo
        if not os.listdir('/model'):
            return False

        # Verificar FFmpeg
        if os.system("ffmpeg -version > /dev/null 2>&1") != 0:
            return False

        # Testar Separator
        separator = Separator('spleeter:4stems-16kHz')
        return True

    except Exception:
        return False

if __name__ == "__main__":
    sys.exit(0 if check_health() else 1) 