import discord
from discord.ext import commands
from economy_schema import Database
from reader import B_COOLDOWN, BOT_COLOR, InsufficientFundsException
from discord import app_commands
import random

class GamblingHelpers(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
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


    # This is only here temporarily, because I accidentally deleted the database
    @commands.command()
    @commands.is_owner()
    @commands.dm_only()
    async def refund(
        self,
        ctx: commands.Context,
        id,
        amount: int
    ):
        user = await self.bot.fetch_user(id)
        if user:
            await self.economy.add_money(id, amount)
            await ctx.send(f"Refunded {user} ${amount:,}")
        else:
            await ctx.send("User not found")


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
            title="I've added $10,000 to you balance",
            description=f"Come back again in {B_COOLDOWN} hours.",
            color=BOT_COLOR
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
            title=f"You worked and earned ${num:,}",
            description="Come back again in 2 minutes.",
            color=BOT_COLOR
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
            title="Global Economy Leaderboard:",
            description="",
            color=discord.Color.gold()
        )

        for i, entry in enumerate(entries):
            id = entry[0]
            name = f"<@{id}>"
            embed.description += f"**`{i+1}.` {name}**\n${entry[1]:,}\n\n"

        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    @app_commands.describe(user="The user to give money to")
    @app_commands.describe(amount="The amount of money to give the user")
    async def give(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        amount: app_commands.Range[int, 1, None]
    ):
        "Give money to another user"
        if user == interaction.user:
            embed = discord.Embed(
                title="Self Error",
                description="You cannot give money to yourself, please try again with a different user.",
                color=BOT_COLOR
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            await self.check_bet(interaction, amount)
            await self.economy.add_money(user.id, amount)
            await self.economy.add_money(interaction.user.id, amount*-1)
            embed = discord.Embed(
                title="Gift Success",
                description=f"You have successfully given {user.mention} ${amount:,}!",
                color=discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(GamblingHelpers(bot))