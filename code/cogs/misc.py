import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Misc(bot))
