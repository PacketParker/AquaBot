import discord
from discord.errors import InteractionResponded
from discord.ext import commands
from discord.ext.commands.errors import *
from utils.helpers import InsufficientFundsException
from datetime import datetime
import traceback
import sys

color = 0xc48aff

class Handlers(commands.Cog, name='handlers'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     error = getattr(error, 'original', error)

    #     if isinstance(error, CommandNotFound):
    #         return

    #     if ctx.command.cog not in [self.bot.get_cog(name) for name in ('Slots', 'Blackjack', "GamblingHelpers", "Coinflip")]:
    #         return traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    #     if isinstance(error, InteractionResponded):
    #         return

    #     if isinstance(error, CommandOnCooldown) and ctx.command.qualified_name != "slots":
    #         s = int(error.retry_after)
    #         s = s % (24 * 3600)
    #         h = s // 3600
    #         s %= 3600
    #         m = s // 60
    #         s %= 60

    #         embed = discord.Embed(
    #             title = "→ Command On Cooldown!",
    #             description = f"• Please wait another {h}hrs {m}min {s}sec before trying that command again.",
    #             colour = color
    #         )
    #         await ctx.send(embed=embed, ephemeral=True)

    #     if isinstance(error, CommandOnCooldown) and ctx.command.qualified_name == "slots":
    #         embed = discord.Embed(
    #             title = "→ Slots Cooldown!",
    #             description = "• To prevent spamming, the slots command in on a 3 second cooldown. Sorry for the inconvenience.",
    #             colour = color
    #         )
    #         await ctx.send(embed=embed, ephemeral=True)

    #     if isinstance(error, (TooManyArguments, BadArgument)):
    #         embed = discord.Embed(
    #             title = "→ Incorrect Syntax!",
    #             description = f"• That is the incorrect way to send that command. In order to see how to use that, use `{ctx.prefix}help` and search for that command.",
    #             colour = color
    #         )
    #         await ctx.send(embed=embed, ephemeral=True)

    #     if isinstance(error, InsufficientFundsException):
    #         embed = discord.Embed(
    #             title = "→ Insufficient Funds!",
    #             description = f"• You do not have enough money to use that command. You can use `{ctx.prefix}add` to add more money. You can also check your current balance with `{ctx.prefix}money`",
    #             colour = color
    #         )
    #         await ctx.send(embed=embed, ephemeral=True)    

    #     if isinstance(error, MissingRequiredArgument):
    #         embed = discord.Embed(
    #             title = "→ Missing Bet!",
    #             description = f"• You must provide the amount of money you would like to bet. Ex: `{ctx.prefix}slots 750`",
    #             colour = color
    #         )
    #         await ctx.send(embed=embed, ephemeral=True)    

    #     if isinstance(error, AttributeError):
    #         return

    #     if isinstance(error, UnboundLocalError):
    #         await ctx.send(f"{ctx.author.mention}, your game timed out, no money was lost or gained.", ephemeral=True)
            
    #     elif not CommandOnCooldown and not TypeError and not AttributeError and not InsufficientFundsException and not MissingRequiredArgument and not TooManyArguments and not BadArgument and not InteractionResponded:
    #         embed = discord.Embed(
    #             colour = color,
    #             title = "→ Error!",
    #             description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
    #         )
    #         embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
    #         await ctx.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Handlers(bot))