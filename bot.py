import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

bot = commands.Bot(command_prefix = "!")

log_channel_id = 889293946801516554

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')




bot.run("ODg5MDI3MTI1Mjc1OTIyNDYy.YUbRBw.96QzGKIyYjyIwKNuXG-w2-i73rY")
