import random
import discord
from discord.ext import commands
from utils.economy import Database
from utils.helpers import *
from datetime import datetime
from utils.helpers import DEFAULT_PREFIX, InsufficientFundsException

color = 0xc48aff

class Coinflip(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = Database(bot)
    
    async def check_bet(
        self,
        ctx: commands.Context,
        bet
    ):
        bet = int(bet)
        if bet <= 0:
            raise commands.errors.BadArgument()
        current = (await self.economy.get_entry(ctx.author.id))[1]
        if bet > current:
            raise InsufficientFundsException()


    @commands.command(aliases = ["cf"])
    @commands.cooldown(1, 1.5, commands.BucketType.user)
    async def coinflip(self, 
        ctx: commands.Context, 
        bet: int=commands.Option(description="Amount you would like to bet")
    ):
        "Bet your money on a 50/50 coinflip"
        await self.check_bet(ctx, bet)
        coinsides = ["heads", "tails"]
        outcome = random.choice(coinsides)
        profile = await self.economy.get_entry(ctx.author.id)


        if outcome == "heads":
            await self.economy.add_money(ctx.author.id, bet)
            embed = discord.Embed(
                title = "→ You win!",
                description = f"• You won {bet:,} dollars. \nYou now have " + f'**${(await self.economy.get_entry(ctx.author.id))[1]:,}**'.format(profile[1]),
                color = discord.Color.green()
            )
            file = discord.File("./utils/heads_tails/heads.gif", filename = "heads.gif")
            embed.set_image(url = "attachment://heads.gif")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(file=file, embed=embed)


        elif outcome == "tails":
            await self.economy.add_money(ctx.author.id, bet*-1)
            embed = discord.Embed(
                title = "→ You Lose!",
                description = f"• You lost {bet:,} dollars. \nYou now have " + f'**${(await self.economy.get_entry(ctx.author.id))[1]:,}**'.format(profile[1]),
                color = discord.Color.red()
            )

            file = discord.File("./utils/heads_tails/tails.gif", filename = "tails.gif")
            embed.set_image(url = f"attachment://tails.gif")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(file=file, embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Coinflip(bot))