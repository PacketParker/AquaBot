import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

class error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #@commands.Cog.listener()
    #async def on_command_error(self, ctx, error):
    #    if isinstance(error, commands.MissingPermissions):
            #await ctx.send(":x: You do not have the required permissions to run this command.")

def setup(bot):
    bot.add_cog(error(bot))
