import random

import nextcord
from nextcord.ext import commands
from modules.economy import Economy
from modules.helpers import *
from datetime import datetime
from modules.helpers import PREFIX, InsufficientFundsException

color = 0xc48aff

class Coinflip(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = Economy()
    
    def check_bet(
        self,
        ctx: commands.Context,
        bet: int=DEFAULT_BET,
    ):
        bet = int(bet)
        if bet <= 0:
            raise commands.errors.BadArgument()
        current = self.economy.get_entry(ctx.author.id)[1]
        if bet > current:
            raise InsufficientFundsException(current, bet)


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def coinflip(self, ctx: commands.Context, bet: int=DEFAULT_BET):
        self.check_bet(ctx, bet)
        coinsides = ["heads", "tails"]
        outcome = random.choice(coinsides)
        profile = self.economy.get_entry(ctx.author.id)


        if outcome == "heads":
            self.economy.add_money(ctx.author.id, bet)
            embed = nextcord.Embed(
                colour = nextcord.Colour.green(),
                title = "→ You win!",
                description = f"• You won {bet:,} dollars. \nYou now have " + f'**${self.economy.get_entry(ctx.author.id)[1]:,}**'.format(profile[1])
            )
            embed.set_image(url = "attachment://coins/heads.gif")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


        elif outcome == "tails":
            self.economy.add_money(ctx.author.id, bet*-1)
            embed = nextcord.Embed(
                colour = nextcord.Colour.red(),
                title = "→ You Lose!",
                description = f"• You lost {bet:,} dollars. \nYou now have" + f'**${self.economy.get_entry(ctx.author.id)[1]:,}**'.format(profile[1])
            )
            embed.set_image(url = "attachment://coins/tails.gif")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @coinflip.error
    async def coinflip_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = nextcord.Embed(
                title = "→ Coinflip Cooldown!",
                description = "• To prevent spamming, the coinflip command in on a 2 second cooldown. Sorry for the inconvenience.",
                colour = color
            )
            await ctx.send(embed=embed)

        else: 
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `$help coinflip` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Coinflip(bot))