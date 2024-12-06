import importlib.metadata
import subprocess
import socket
import os


UPDATE_FLAG = "/tmp/update_done.flag"  # Caminho para o arquivo de flag de atualização (ajuste para seu sistema)


def update():
    if os.path.exists(UPDATE_FLAG):
        print("Atualização já realizada.")
        return  # Evita que o update seja feito várias vezes na mesma execução

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

        # Cria o arquivo de flag após a atualização
        with open(UPDATE_FLAG, 'w') as f:
            f.write("update completed")
    else:
        print("Sem conexão. Não foi possível verificar atualizações.")


def tem_conexao() -> bool:
    try:
        socket.create_connection(('8.8.8.8', 53), timeout=5)
        return True
    except Exception:
        return False
