import discord
from discord.ext import commands
from economy_schema import Database
from reader import B_COOLDOWN
from discord import app_commands
import random

color = 0xc48aff

class GamblingHelpers(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.economy = Database(bot)


    @app_commands.command()
    @app_commands.checks.cooldown(1, B_COOLDOWN*3600)
    async def add(
        self, 
        interaction: discord.Interaction
    ):
        "Add $10,000 to your balance every 2 hours"
        
        amount = 10000
        await self.economy.add_money(interaction.user.id, amount)
        embed = discord.Embed(
            title = "I've added $10,000 to you balance",
            description = f"Come back again in {B_COOLDOWN} hours."
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command()
    @app_commands.checks.cooldown(1, 120)
    async def work(
        self,
        interaction: discord.Interaction
    ):
        "Work for a randomized amount of money every 2 minutes"

        a = random.randint(500, 2500)
        b = random.randint(500, 2500)
        if a == b:
            num = 50000000
        else:
            num = a + b

        await self.economy.add_money(interaction.user.id, num)
        embed = discord.Embed(
            title = f"You worked and earned ${num:,}",
            description = "Come back again in 2 minutes."
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command()
    async def leaderboard(
        self, 
        interaction: discord.Interaction
    ):
        "Show the global currency leaderboard"

        entries = await self.economy.top_entries(5)
        embed = discord.Embed(
            title='Global Economy Leaderboard:', 
            color=discord.Color.gold()
        )
        
        for i, entry in enumerate(entries): 
            id = entry[0]
            try:
                name = await self.bot.fetch_user(id)
            except TypeError:
                name = id
            embed.add_field(
                name=f"{i+1}. {name}",
                value='${:,}'.format(entry[1]),
                inline=False
            )
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    @app_commands.describe(user="The user to give money to")
    @app_commands.describe(amount="The amount of money to give the user")
    async def give(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        amount: int
    ):
        "Give money to another user"
        color = 0xc48aff

        if amount <= 0:
            embed = discord.Embed(
                title = "→ Negative or no money error!",
                description = "• You cannot give negative or no money to another user, please try again.",
                colour = color
            )
            return await interaction.response.send_message(embed=embed)
        
        elif user == interaction.user:
            embed = discord.Embed(
                title = "→ Self error!",
                description = "• You cannot give money to yourself, please try again.",
                colour = color
            )
            return await interaction.response.send_message(embed=embed)

        else:
            await self.economy.add_money(user.id, amount)
            await self.economy.add_money(interaction.user.id, amount*-1)
            embed = discord.Embed(
                title = "Gift Success!",
                description = f"You have successfully given {user.mention} ${amount:,}!",
                colour = discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(GamblingHelpers(bot))