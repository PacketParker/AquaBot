import discord
from discord.ext import commands
from economy_schema import Database
from reader import B_COOLDOWN
from discord import app_commands

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

        "Add $2,500 to your balance every 2 hours"
        amount = 2500
        await self.economy.add_money(interaction.user.id, amount)
        embed = discord.Embed(
            title = "I've added $2,500 to you balance",
            description = f"Come back again in {B_COOLDOWN} hours."
        )
        await interaction.response.send_message(embed=embed)


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


async def setup(bot: commands.Bot):
    await bot.add_cog(GamblingHelpers(bot))