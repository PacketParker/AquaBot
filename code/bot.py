import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
import os
from modules.helpers import *

log_channel_id = 889293946801516554

bot = commands.Bot(
    command_prefix=PREFIX,
    owner_ids=OWNER_IDS,
    intents=nextcord.Intents.all()
)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to nextcord!')


bot.remove_command('help')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

for filename in os.listdir('./cogs/gamble'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.gamble.{filename[:-3]}')

bot.run("ODg5MDI3MTI1Mjc1OTIyNDYy.YUbRBw.96QzGKIyYjyIwKNuXG-w2-i73rY")
