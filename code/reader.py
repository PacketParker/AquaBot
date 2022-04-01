import os
from pathlib import Path
import yaml

class InsufficientFundsException(Exception):
    def __init__(self) -> None:
        super().__init__()

os.chdir(Path(__file__).parent.parent)
ABS_PATH = Path(os.getcwd())
COG_FOLDER = os.path.join(ABS_PATH, 'cogs/')

with open(os.path.join(ABS_PATH, 'config.yml'),  # type:ignore
            'r', encoding='utf-8') as f:
    config = yaml.safe_load(f.read()).get('bot', {})

TOKEN = config.get('token')
DEFAULT_PREFIX = config.get('prefix')
B_COOLDOWN = config.get('bonus_cooldown')