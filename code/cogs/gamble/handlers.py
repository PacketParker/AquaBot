import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.errors import *
from modules.helpers import PREFIX, InsufficientFundsException

color = 0xc48aff

class Handlers(commands.Cog, name='handlers'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
'''

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        
        error = getattr(error, 'original', error)

        if isinstance(error, (MissingRequiredArgument, TooManyArguments, BadArgument)):
            embed = nextcord.Embed(
                title = "→ Incorrect Syntax!",
                description = f"• That is the incorrect way to send that command. In order to see how to use that command, use `$help {ctx.command.name}`",
                colour = color
            )
            await ctx.send(embed=embed)

        if isinstance(error, InsufficientFundsException):
            embed = nextcord.Embed(
                title = "→ Insufficient Funds!",
                description = "• You do not have enough money to use that command. You can use `$add` to add more money. You can also check your current balance with `$money`",
                colour = color
            )
            await ctx.send(embed=embed)

        if isinstance(error, CommandOnCooldown):
            embed = nextcord.Embed(
                title = "→ Slots Cooldown!",
                description = "• The slots command is on a 3 second cooldown in order to keep up with the creation of gifs. Sorry for the inconvenience.",
                colour = color
            )
            await ctx.send(embed=embed)
        
        elif not CommandOnCooldown and not InsufficientFundsException and not MissingRequiredArgument and not TooManyArguments and not BadArgument:
            raise error
'''

def setup(bot: commands.Bot):
    bot.add_cog(Handlers(bot))