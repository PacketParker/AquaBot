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


    @commands.command(aliases = ["cf"])
    @commands.cooldown(1, 1.5, commands.BucketType.user)
    async def coinflip(self, ctx: commands.Context, bet: int=DEFAULT_BET):
        self.check_bet(ctx, bet)
        coinsides = ["heads", "tails"]
        outcome = random.choice(coinsides)
        profile = self.economy.get_entry(ctx.author.id)


        if outcome == "heads":
            self.economy.add_money(ctx.author.id, bet)
            embed = make_embed(
                title = "→ You win!",
                description = f"• You won {bet:,} dollars. \nYou now have " + f'**${self.economy.get_entry(ctx.author.id)[1]:,}**'.format(profile[1]),
                color = nextcord.Color.green()
            )
            fp = f'heads.gif'
            file = nextcord.File(fp, filename = fp)
            embed.set_image(url = f"attachment://{fp}")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(file=file, embed=embed)


        elif outcome == "tails":
            self.economy.add_money(ctx.author.id, bet*-1)
            embed = make_embed(
                title = "→ You Lose!",
                description = f"• You lost {bet:,} dollars. \nYou now have " + f'**${self.economy.get_entry(ctx.author.id)[1]:,}**'.format(profile[1]),
                color = nextcord.Color.red()
            )

            fp = f'tails.gif'
            file = nextcord.File(fp, filename = fp)
            embed.set_image(url = f"attachment://{fp}")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(file=file, embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Coinflip(bot))