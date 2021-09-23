import os
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions

class error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #@commands.Cog.listener()
    #async def on_command_error(self, ctx, error):
    #    if isinstance(error, commands.MissingPermissions):
    #        await ctx.send(":x: You do not have the required permissions to run this command.")
    #    if isinstance(error, commands.BadArgument):
    #        await ctx.send("Incorrect usage. Please refer to the help menu to find out how to use that command.")

def setup(bot):
    bot.add_cog(error(bot))
