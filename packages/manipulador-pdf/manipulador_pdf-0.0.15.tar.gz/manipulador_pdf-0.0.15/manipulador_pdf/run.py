from .update import update
from .configs.main_hub import main_hub
from .configs.configure import configure
import importlib.metadata
import subprocess
import socket


def run():
    print('update')
    pacote = "manipulador_pdf"

    if tem_conexao():
        try:
            importlib.metadata.version(pacote)
            print("Verificando atualizações...")
            subprocess.check_call([subprocess.sys.executable, "-m", "pip", "install", "--upgrade", pacote])
        except importlib.metadata.PackageNotFoundError:
            print("Instalando recursos...")
            subprocess.check_call([subprocess.sys.executable, "-m", "pip", "install", pacote])

    #update()
    main_hub()



def tem_conexao() -> bool:
    try:
        socket.create_connection(('8.8.8.8', 53), timeout=5)
        return True
    except Exception:
        return False
