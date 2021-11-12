import nextcord
from nextcord.ext import commands
from utils.economy import Database
from utils.helpers import *
from PIL import Image
from utils.helpers import DEFAULT_PREFIX, InsufficientFundsException


log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48af

class ConfirmPurchase(nextcord.ui.View):
    def __init__(self, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        #self.ctx = ctx
        self.value = None
        self.add_item(RankDropdown())

    @nextcord.ui.button(label='Yes', style=nextcord.ButtonStyle.green, row=2)
    async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items.",
            color = nextcord.Color.random()
        )

        await interaction.response.edit_message(embed=embed)

    @nextcord.ui.button(label='No', style=nextcord.ButtonStyle.red, row=2)
    async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items.",
            color = nextcord.Color.random()
        )

        view = ShopView()

        await interaction.response.edit_message(embed=embed, view=view)


class RankDropdown(nextcord.ui.Select):
    def __init__(self):

        options = [
            nextcord.SelectOption(label='Copper III', description="1,000", emoji = "<:copper_3:908535582534299688>"),
            nextcord.SelectOption(label='Copper II', description="2,000", emoji = "<:copper_2:908535594714558524>"),
            nextcord.SelectOption(label='Copper I', description="3,000", emoji = "<:copper_1:908535605644918895>"),

            nextcord.SelectOption(label='Bronze III', description="10,000", emoji = "<:bronze_3:908535616650760222>"),
            nextcord.SelectOption(label='Bronze II', description="20,000", emoji = "<:bronze_2:908535628503863296>"),
            nextcord.SelectOption(label='Bronze I', description="30,000", emoji = "<:bronze_1:908535639606198292>"),

            nextcord.SelectOption(label='Silver III', description="100,000", emoji = "<:silver_3:908535654667911168>"),
            nextcord.SelectOption(label='Silver II', description="200,000", emoji = "<:silver_2:908535667263434782>"),
            nextcord.SelectOption(label='Silver I', description="300,000", emoji = "<:silver_1:908535680064442398>"),

            nextcord.SelectOption(label='Gold III', description="1,000,000", emoji = "<:gold_3:908535691137388554>"),
            nextcord.SelectOption(label='Gold II', description="2,000,000", emoji = "<:gold_2:908535705154764870>"),
            nextcord.SelectOption(label='Gold I', description="3,000,000", emoji = "<:gold_1:908535742224027758>"),

            nextcord.SelectOption(label='Platinum III', description="10,000,000", emoji = "<:platinum_3:908535751900282880>"),
            nextcord.SelectOption(label='Platinum II', description="20,000,000", emoji = "<:platinum_2:908535764629999656>"),
            nextcord.SelectOption(label='Platinum I', description="30,000,000", emoji = "<:platinum_1:908535773689679932>"),

            nextcord.SelectOption(label='Diamond', description="1,000,000,000,000", emoji = "<:diamond:908535791700037702>"),

            nextcord.SelectOption(label='Champion', description="1,000,000,000,000,000,000", emoji = "<:champion:908535801338540042>"),

        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == 'Copper III' or 'Copper II' or 'Copper I' or 'Bronze III' or 'Bronze II' or 'Bronze I' or 'Silver III' or 'Silver II' or 'Silver I' or 'Gold III' or 'Gold II' or 'Gold I' or 'Platinum III' or 'Platinum II' or 'Platinum I' or 'Diamond' or 'Champion':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to make this purchase, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            view = ConfirmPurchase()

            await interaction.response.edit_message(embed=embed, view=view)









class RankView(nextcord.ui.View):
    def __init__(self, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        #self.ctx = ctx
        self.value = None
        self.add_item(RankDropdown())

    @nextcord.ui.button(label='Main Page', style=nextcord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items.",
            color = nextcord.Color.random()
        )

        view = ShopView()

        await interaction.response.edit_message(embed=embed, view=view)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()



class ShopDropdown(nextcord.ui.Select):
    def __init__(self):

        options = [
            nextcord.SelectOption(label='Ranks', description='Buy ranks and show off your wealth'),
        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)



    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == 'Ranks':
            embed = nextcord.Embed(
                title = "💰 - Ranks \nSpend your money in order to get more ranks.",
                description = "**Purchase a rank by clicking on one of the dropdown menus below, and then confirming your purchase.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "Copper III", value = f"1,000", inline=True)
            embed.add_field(name = "Copper II", value = f"2,000", inline=True)
            embed.add_field(name = "Copper I", value = f"3,000", inline=True)

            embed.add_field(name = "Bronze III", value = f"10,000", inline=True)
            embed.add_field(name = "Bronze II", value = f"20,000", inline=True)
            embed.add_field(name = "Bronze I", value = f"30,000", inline=True)

            embed.add_field(name = "Silver III", value = f"100,000", inline=True)
            embed.add_field(name = "Silver II", value = f"200,000", inline=True)
            embed.add_field(name = "Silver I", value = f"300,000", inline=True)

            embed.add_field(name = "Gold III", value = f"1,000,000", inline=True)
            embed.add_field(name = "Gold II", value = f"2,000,000", inline=True)
            embed.add_field(name = "Gold I", value = f"3,000,000", inline=True)

            embed.add_field(name = "Platinum III", value = f"10,000,000", inline=True)
            embed.add_field(name = "Platinum II", value = f"20,000,000", inline=True)
            embed.add_field(name = "Platinum I", value = f"30,000,000", inline=True)
            
            embed.add_field(name = "Diamond", value = f"1,000,000,000,000", inline=True)

            embed.add_field(name = "Champion", value = f"1,000,000,000,000,000,000", inline=True)

            view = RankView()

            await interaction.response.edit_message(embed=embed, view=view)


class ShopView(nextcord.ui.View):
    def __init__(self, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        #self.ctx = ctx
        self.value = None
        self.add_item(ShopDropdown())

    @nextcord.ui.button(label='Main Page', style=nextcord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items.",
            color = nextcord.Color.random()
        )

        await interaction.response.edit_message(embed=embed)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()

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

        view = ShopView()
        await ctx.send(embed=embed, view=view)

        ##TODO: Add a dropdown menu in order for people to choose the category that they want to shop in.
               #Once the category is chosen, figure out a system for how they are going to buy items, e.g. Buttons, Dropdowns, Commands
               #Come up with new ideas to add to the shop in order to make it more interesting for new users, and those with a lot of moneyx


def setup(bot):
    bot.add_cog(Profile(bot))