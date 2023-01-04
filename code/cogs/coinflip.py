import discord
from discord.ext import commands
from economy_schema import Database
from discord import app_commands
from reader import InsufficientFundsException
import random

color = 0xc48aff

class CoinFlip(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = Database(bot)

    async def check_bet(
        self,
        interaction: discord.Interaction,
        bet
    ):
        bet = int(bet)
        if bet <= 0:
            raise commands.errors.BadArgument()
        current = (await self.economy.get_entry(interaction.user.id))[1]
        if bet > current:
            raise InsufficientFundsException()


    @app_commands.command()
    @app_commands.checks.cooldown(1, 2)
    @app_commands.describe(bet="The amount of money you want to bet")
    async def coinflip(
        self,
        interaction: discord.Interaction,
        bet: int
    ):
        "Bet money on a coinflip (heads=win, tails=lose)"

        await self.check_bet(interaction, bet)

        if random.randint(0, 3) == 0:
            await self.economy.add_money(interaction.user.id, bet*2)
            embed = discord.Embed(
                title = f"You won ${bet*2:,}!",
                description = "You flipped heads!",
                color = discord.Color.green()
            )
            embed.set_image(url="https://aquabot.info/assets/images/heads.gif")

            return await interaction.response.send_message(embed=embed)

        else:
            await self.economy.add_money(interaction.user.id, bet*-1)
            embed = discord.Embed(
                title = f"You lost ${bet:,}!",
                description = "You flipped tails!",
                color = discord.Color.red()
            )
            embed.set_image(url="https://aquabot.info/assets/images/tails.gif")

            return await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CoinFlip(bot))