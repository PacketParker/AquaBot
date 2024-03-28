import os
import random
import datetime
import discord
from discord.ext import commands
from discord import app_commands

from bot import InsufficientFundsException
from database import Database


"""NOTE: The code to create the slot reels was found on GitHub a while ago, same person who
made the blackjack stuff (still don't know who it was). I ended up modifying it quite a lot with my own images, and changed
the code a bit so that I could have it generate the slot reels and put them in the correct folders

I premade the slot reels as it uses less resources to just load them from the folder than to
generate them every time someone uses the command."""

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

        win_rate = 5/100
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