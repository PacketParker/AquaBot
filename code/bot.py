import discord
from discord.ext import commands, tasks
import os
import zipfile
import tqdm
import requests

from validate_config import create_config
from database import init_database
from global_variables import LOG, BOT_TOKEN, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


def unpack_reels():
    # Files ending in .zip within /code/utils, extract it to /code/utils
    for file in os.listdir("code/utils"):
        # If folders exist, don't unpack
        if (os.path.exists("code/utils/winning_reels") and
                os.path.exists("code/utils/losing_reels_1") and
                os.path.exists("code/utils/losing_reels_2") and
                os.path.exists("code/utils/losing_reels_3") and
                os.path.exists("code/utils/losing_reels_4") and
                os.path.exists("code/utils/losing_reels_5")):
            break
        if file.endswith(".zip"):
            with zipfile.ZipFile(f"code/utils/{file}", 'r') as zip_ref:
                for member in tqdm.tqdm(iterable=zip_ref.namelist(), total=len(zip_ref.namelist()), desc=f"Unpacking {file}..."):
                    zip_ref.extract(member, "code/utils")


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='***',
            activity = discord.Game(name="Ping Me For Help!"),
            intents = discord.Intents.default()
        )
    async def setup_hook(self):
        unpack_reels()
        create_config()
        get_access_token.start()
        await init_database()
        for ext in os.listdir('./code/cogs'):
            if ext.endswith('.py'):
                await self.load_extension(f'cogs.{ext[:-3]}')


bot = MyBot()
bot.count_hold = 0
bot.remove_command('help')


@bot.event
async def on_ready():
    LOG.info(f"{bot.user} has connected to Discord.")


@tasks.loop(minutes=45)
async def get_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }
    response = requests.post(auth_url, data=data)
    access_token = response.json()['access_token']
    bot.access_token = access_token

class InsufficientFundsException(Exception):
    def __init__(self) -> None:
        super().__init__()


if __name__ == '__main__':
    bot.run(BOT_TOKEN)