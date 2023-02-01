import os
from pathlib import Path
import yaml

class InsufficientFundsException(Exception):
    def __init__(self) -> None:
        super().__init__()

os.chdir(Path(__file__).parent.parent)
ABS_PATH = Path(os.getcwd())

with open(os.path.join(ABS_PATH, 'config.yml'),  # type:ignore
            'r', encoding='utf-8') as f:
    config = yaml.safe_load(f.read()).get('bot', {})

TOKEN = config.get('token')
B_COOLDOWN = config.get('bonus_cooldown')
BOT_COLOR = config.get('bot_color')
SERVER_ID = config.get('test_server_id')
BUG_CHANNEL_ID = config.get('bug_channel_id')
FEEDBACK_CHANNEL_ID = config.get('feedback_channel_id')
APIKEY = config.get('apikey')

username = config.get('username')
password = config.get('password')
host = config.get('host')
port = config.get('port')
database = config.get('database')

CONNECTION_STRING = f"postgresql://{username}:{password}@{host}:{port}/{database}"

CLIENT_ID = config.get('spotify_id')
CLIENT_SECRET = config.get('spotify_secret')