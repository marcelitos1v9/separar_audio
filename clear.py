import os
import shutil
import time

print("Limpando pastas input e output...")

# Verificar se as pastas existem
if not os.path.exists("input"):
    os.makedirs("input")
if not os.path.exists("output"):
    os.makedirs("output")

# Limpar pasta input
print("Limpando pasta input...")
try:
    for item in os.listdir("input"):
        item_path = os.path.join("input", item)
        if os.path.isfile(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    # Limpar pasta output
    print("Limpando pasta output...")
    for item in os.listdir("output"):
        item_path = os.path.join("output", item)
        if os.path.isfile(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    print("\nPastas limpas com sucesso!")
    print("\nInput: 0 arquivos")
    print("Output: 0 arquivos\n")
    time.sleep(3)

except Exception as e:
    print("Erro ao limpar as pastas.")
    print(f"Erro: {str(e)}")
    print("Verifique se nenhum arquivo está em uso.")
    input("Pressione Enter para continuar...")
    exit(1)
