from .configs.main_hub import main_hub
from .update import update


def run():
    update()
    main_hub()
