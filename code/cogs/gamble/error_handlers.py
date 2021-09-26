import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.errors import *
from modules.helpers import PREFIX, InsufficientFundsException


class Handlers(commands.Cog, name='handlers'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    #@commands.Cog.listener()
    #async def on_command_error(self, ctx, error):
        #if isinstance(error, CommandInvokeError):
            #await self.on_command_error(ctx, error.original)
        
        #elif isinstance(error, CommandNotFound):
            #await ctx.invoke(self.bot.get_command('help'))

        #elif isinstance(error, (MissingRequiredArgument, TooManyArguments, BadArgument)):
            #await ctx.invoke(self.bot.get_command('help'), ctx.command.name)

        #elif isinstance(error, InsufficientFundsException):
            #await ctx.invoke(self.bot.get_command('money'))

       # elif isinstance(error, CommandOnCooldown):
           # s = int(error.retry_after)
           # s = s % (24 * 3600)
          #  h = s // 3600
          #  s %= 3600
            #m = s // 60
            #s %= 60
           # embed = nextcord.Embed(
             #   title = "Command currently on cooldown",
             #   description = f"**{h}hrs {m}min {s}sec remaining.**",
            #    colour = nextcord.Colour.blue()
         #   )
          #  await ctx.send(embed=embed)
        
      #  else:
        #    raise error

def setup(bot: commands.Bot):
    bot.add_cog(Handlers(bot))