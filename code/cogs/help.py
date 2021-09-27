import asyncio
import os
import random
from typing import List, Tuple, Union

import nextcord
from nextcord.ext import commands
from modules.card import Card
from modules.economy import Economy
from modules.helpers import *
from PIL import Image

color = 0xc48aff

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


#    @commands.group(invoke_without_command=True)
#    async def help(self, ctx):
#        embed = nextcord.Embed(
#            title = "Help",
#            description = "Use `$help <command> for extended information on that command",
#            colour = ctx.author.colour    
#        )

#        embed.add_field(name = "Moderation", value = "kick, ban, softban, mute, unmute")
#        embed.add_field(name = "Fun", value = "")






def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))