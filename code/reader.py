import os
from pathlib import Path
import yaml
import discord

class InsufficientFundsException(Exception):
    def __init__(self) -> None:
        super().__init__()

os.chdir(Path(__file__).parent.parent)
ABS_PATH = Path(os.getcwd())

with open(os.path.join(ABS_PATH, 'config.yml'),  # type:ignore
            'r', encoding='utf-8') as f:
    config = yaml.safe_load(f.read()).get('bot', {})

TOKEN = config.get('token')
DEFAULT_PREFIX = config.get('prefix')
B_COOLDOWN = config.get('bonus_cooldown')
SERVER_ID = config.get('test_server_id')
TEST_SERVER_ID = discord.Object(id=SERVER_ID)
BUG_CHANNEL_ID = config.get('bug_channel_id')
FEEDBACK_CHANNEL_ID = config.get('feedback_channel_id')