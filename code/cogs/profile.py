import nextcord
from nextcord.ext import commands
from utils.economy import Database
from utils.helpers import *
from PIL import Image
from utils.helpers import DEFAULT_PREFIX, InsufficientFundsException


log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy = Database(bot)


    @commands.command()
    async def shop(self, ctx, user: nextcord.Member=None):
        user = user.id if user else ctx.author.id
        profile = await self.economy.get_entry(user)
        balance = profile[1]


        embed = nextcord.Embed(
            title = "Shop",
            description = "Buy items with the money you've earned, and view everything in your inventory",
            color = nextcord.Color.random()
        )

        embed.add_field(name = f"Balance: {balance}", value = "\u200b")


def setup(bot):
    bot.add_cog(Profile(bot))