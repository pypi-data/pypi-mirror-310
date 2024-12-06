from .update import update
from .configs.main_hub import main_hub
from .configs.configure import configure
import importlib.metadata
import subprocess
import socket


def imprimir_versao():
    """
    Imprime a versão atual da biblioteca manipulador_pdf.
    """
    try:
        # Obtém a versão da biblioteca manipulador_pdf
        versao = importlib.metadata.version('manipulador_pdf')
        print(f'Versão instalada: {versao}')
    except importlib.metadata.PackageNotFoundError:
        print('Biblioteca não instalada.')


def run():
    imprimir_versao()
    print('Verificando atualizações...')

    pacote = "manipulador_pdf"

    if tem_conexao():
        try:
            # Obtém a versão da biblioteca instalada
            versao_instalada = importlib.metadata.version(pacote)
            print(f"Versão atual do pacote: {versao_instalada}")

            # Obtém a versão mais recente disponível no PyPI
            resultado = subprocess.run(
                [subprocess.sys.executable, "-m", "pip", "search", pacote],
                capture_output=True, text=True
            )

            # Verifica se a versão instalada é a mais recente
            if "INSTALLED" in resultado.stdout and versao_instalada not in resultado.stdout:
                print("Atualizando biblioteca...")
                subprocess.check_call([subprocess.sys.executable, "-m", "pip", "install", "--upgrade", pacote])
            else:
                print("Já está com a versão mais recente.")

        except importlib.metadata.PackageNotFoundError:
            print("Biblioteca não encontrada. Instalando recursos...")
            subprocess.check_call([subprocess.sys.executable, "-m", "pip", "install", pacote])

    # Continuar com a execução do processo principal
    main_hub()


def tem_conexao() -> bool:
    try:
        # Estabelece uma conexão com o servidor DNS do Google
        socket.create_connection(('8.8.8.8', 53), timeout=5)
        return True
    except Exception:
        return False
