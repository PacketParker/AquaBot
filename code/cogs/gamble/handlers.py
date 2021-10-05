import nextcord
from nextcord.errors import InteractionResponded
from nextcord.ext import commands
from nextcord.ext.commands.errors import *
from modules.helpers import PREFIX, InsufficientFundsException
from datetime import datetime
color = 0xc48aff

class Handlers(commands.Cog, name='handlers'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        
        error = getattr(error, 'original', error)

        if isinstance(error, InteractionResponded):
            return

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
        
        elif not CommandOnCooldown and not InsufficientFundsException and not MissingRequiredArgument and not TooManyArguments and not BadArgument and not InteractionResponded:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Handlers(bot))