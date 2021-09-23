import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

log_channel_id = 889293946801516554

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
                
bot.run("ODg5MDI3MTI1Mjc1OTIyNDYy.YUbRBw.96QzGKIyYjyIwKNuXG-w2-i73rY")
