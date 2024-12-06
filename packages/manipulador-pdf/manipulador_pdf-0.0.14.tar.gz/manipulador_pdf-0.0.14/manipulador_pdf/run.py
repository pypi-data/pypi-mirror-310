from .update import update
from .configs.main_hub import main_hub
from .configs.configure import configure
import subprocess
import sys


def run():
    # Verifica se o script foi chamado com o argumento '--no-update'
    if "--no-update" not in sys.argv:
        update()  # Executa a atualização
        # Reinicia o script com o argumento '--no-update'
        subprocess.check_call([sys.executable, *sys.argv, "--no-update"])
    else:
        main_hub()
