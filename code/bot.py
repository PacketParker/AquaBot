import nextcord
from nextcord.ext import commands
import os
from modules.helpers import *

log_channel_id = 889293946801516554
intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=PREFIX,
    owner_ids=OWNER_IDS,
    intents=intents
)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to nextcord!')
    await bot.change_presence(activity = nextcord.Game("$help"))


bot.remove_command('help')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

for filename in os.listdir('./cogs/gamble'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.gamble.{filename[:-3]}')

bot.run("ODg5MDI3MTI1Mjc1OTIyNDYy.YUbRBw.nevr90Fl-spt10q72mj6Q185iFc")
