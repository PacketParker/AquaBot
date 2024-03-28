import discord
from discord.ext import commands
import os
import zipfile
import tqdm

from validate_config import create_config
from database import init_database
from global_variables import LOG, BOT_TOKEN


def unpack_reels():
    # For every file that ends in .zip within /code/utils, extract it to /code/utils
    for file in os.listdir("code/utils"):
        # If the winning_reels, losing_reels_1, etc folders are already made, don't unpack the zip files
        if os.path.exists("code/utils/winning_reels") and os.path.exists("code/utils/losing_reels_1") and os.path.exists("code/utils/losing_reels_2") and os.path.exists("code/utils/losing_reels_3") and os.path.exists("code/utils/losing_reels_4") and os.path.exists("code/utils/losing_reels_5"):
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

class InsufficientFundsException(Exception):
    def __init__(self) -> None:
        super().__init__()


if __name__ == '__main__':
    bot.run(BOT_TOKEN)