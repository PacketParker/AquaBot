import bisect
import os
import random
import datetime
import discord
from discord.ext import commands
from economy_schema import Database
from PIL import Image
from reader import InsufficientFundsException
from discord import app_commands

"""NOTE: This code was found somewhere on GitHub a long time ago. I changed it a bit to work for
discord.py 2.0 and for my needs. If anyone knows who wrote this, please let me know so I can
give them credit."""

class Slots(commands.Cog):
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
    @app_commands.checks.cooldown(1, 4)
    @app_commands.describe(bet='Amount of money to bet')
    async def slots(
        self,
        interaction: discord.Interaction,
        bet: app_commands.Range[int, 1, None]
    ):
        "Bet a specified amount of money on the slot machines"
        await self.check_bet(interaction, bet)

        win_rate = 4/100
        multiplier_dict = {"seven": 80, "diamond": 40, "bar": 25, "clover": 10, "grape": 5, "lemon": 4}

        if random.random() < win_rate:
            # Pick a random word
            word = random.choice(["seven", "diamond", "bar", "clover", "grape", "lemon"])
            multiplier = multiplier_dict[word]
            # Pick one of the 10 images of the winning reel type (seven, diamond, etc.)
            image_path = f"code/utils/winning_reels/{word}_{random.randint(1, 10)}.gif"
            amount = bet * multiplier

        else:
            # Pick a random number 1-5, this will decide which losing folder we pick a reel from
            folder = f"code/utils/losing_reels_{random.randint(1, 5)}"
            # Pick a random image from the folder
            image_path = f"{folder}/{random.choice(os.listdir(folder))}"
            amount = bet * -1

        await self.economy.add_money(interaction.user.id, amount)
        current = (await self.economy.get_entry(interaction.user.id))[1]

        file = discord.File(image_path, "slot_machine.gif")
        embed = discord.Embed(
            title=f"You {'won' if amount > 0 else 'lost'} {abs(amount):,} {'dollar' if abs(amount) == 1 else 'dollars'}!",
            description=f"You now have {current:,} {'dollar' if current == 1 else 'dollars'}",
            color=discord.Color.green() if amount > 0 else discord.Color.red()
        )
        embed.set_image(url="attachment://slot_machine.gif")
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed, file=file)


async def setup(bot: commands.Bot):
    await bot.add_cog(Slots(bot))