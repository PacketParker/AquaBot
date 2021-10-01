import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from datetime import datetime
import time
import asyncio

log_channel_id = 889293946801516554

yellow = 0xffc400
color = 0xc48aff

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
#TODO have the bot dm a member when they have been muted, unmuted, banned, softbanned, kicked, etc.

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def createmute(self, ctx):
        server = ctx.message.guild
        perms = nextcord.Permissions(send_messages=False, read_messages=True)
        await self.bot.create_role(server, name='Muted', permissions=perms)

   
    #@commands.command()
    #@commands.has_permissions(kick_members=True)
    #async def mute(self, ctx, member: nextcord.Member, *, reason=None):
#Give user the muted role 


    #@commands.command()
    #@commands.has_permissions(kick_members=True)
    #async def unmute(self, ctx, member: nextcord.Member, *, reason=None):
#Takes muted role away from user


def setup(bot):
    bot.add_cog(Mute(bot))