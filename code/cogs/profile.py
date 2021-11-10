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
            description = f"Choose from one of the categories below in order to shop for items \n\nBalance: {balance:,}",
            color = nextcord.Color.random()
        )

        await ctx.send(embed=embed)

        ##TODO: Add a dropdown menu in order for people to choose the category that they want to shop in.
               #Once the category is chosen, figure out a system for how they are going to buy items, e.g. Buttons, Dropdowns, Commands
               #Come up with new ideas to add to the shop in order to make it more interesting for new users, and those with a lot of moneyx


def setup(bot):
    bot.add_cog(Profile(bot))