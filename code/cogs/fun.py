import discord
from discord.ext import commands
from datetime import datetime
import requests
import json

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(Fun(bot))