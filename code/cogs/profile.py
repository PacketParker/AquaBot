import nextcord
from nextcord.ext import commands
from utils.economy import Database
from utils.helpers import *
from PIL import Image
from utils.helpers import DEFAULT_PREFIX, InsufficientFundsException


log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48af

class Economy:
    def __init__(self, bot):
        self.bot = bot
        self.economy = Database(bot)

    async def check_bet(
        self,
        ctx: commands.Context,
        bet: int=DEFAULT_BET,
    ):
        bet = int(bet)
        if bet <= 0:
            raise commands.errors.BadArgument()
        current = (await self.economy.get_entry(ctx.author.id))[1]
        if bet > current:
            raise InsufficientFundsException()


class AfterPurchase(nextcord.ui.View):
    def __init__(self, bot, ctx, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.bot = bot
        self.economy = Database(bot)
        self.value = None

        1 == 'Copper III'
        2 == 'Coppper II'
        3 == 'Copper I'
        
        4 == 'Bronze III'
        5 == 'Bronze II'
        6 == 'Bronze I'

        7 == 'Silver III'
        8 == 'Silver II'
        9 == 'Silver I'

        10 == 'Gold III'
        11 == 'Gold II'
        12 == 'Gold I'

        13 == 'Platinum III'
        14 == 'Platinum II'
        15 == 'Platinum I'

        16 == 'Diamond'

        17 == 'Champion'

    @nextcord.ui.button(label='Main Page', style=nextcord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = self.ctx.user.id if self.ctx.user else self.ctx.author.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        async with self.bot.db.execute("SELECT rank FROM profile WHERE user_id = ? ORDER BY rank DESC", (user_id,)) as cursor:
            data = await cursor.fetchall()
            if data:
                rank = data[0]
            else:
                rank = "No ranks"

        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items \n\nBalance: {balance:,} \nRanks: {rank}",
            color = nextcord.Color.random()
        )

        await interaction.response.edit_message(embed=embed)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()


class ConfirmPurchase(nextcord.ui.View):
    def __init__(self, bot, ctx, bet, rank_value, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.bot = bot
        self.bet = bet
        self.rank_value = rank_value
        self.check = Economy(bot)
        self.economy = Database(bot)
        self.value = None
        self.add_item(RankDropdown(bot, ctx))

        'Copper III' == 1
        'Coppper II' == 2
        'Copper I' == 3
        
        'Bronze III' == 4
        'Bronze II' == 5
        'Bronze I' == 6

        'Silver III' == 7
        'Silver II' == 8
        'Silver I' == 9

        'Gold III' == 10
        'Gold II' == 11
        'Gold I' == 12

        'Platinum III' == 13
        'Platinum II' == 14
        'Platinum I' == 15

        'Diamond' == 16

        'Champion' == 17

    @nextcord.ui.button(label='Yes', style=nextcord.ButtonStyle.green, row=2)
    async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = self.ctx.author.id
        await self.check.check_bet(self.ctx, self.bet)
        await self.economy.add_money(user_id, self.bet*-1)

        async with self.bot.db.execute("SELECT rank FROM profile WHERE user_id = ?", (user_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                rank = data[0]
                await self.bot.db.execute("UPDATE profile SET rank = ? WHERE user_id = ?", (rank + ", " + self.rank_value, user_id))
                await self.bot.db.commit()

            else:
                await self.bot.db.execute("INSERT INTO profile (user_id, rank) VALUES(?, ?)", (user_id, self.rank_value))
                await self.bot.db.commit()

        embed = nextcord.Embed(
            title = "Purchase Successful",
            description = f"Your purchase was successful. In order to purchase more items, please click the main page button below.",
            color = nextcord.Color.random()
        )

        view = AfterPurchase(self.ctx, self.bot)

        await interaction.response.edit_message(embed=embed, view=view)

    @nextcord.ui.button(label='No', style=nextcord.ButtonStyle.red, row=2)
    async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items.",
            color = nextcord.Color.random()
        )

        view = ShopView(self.bot, self.ctx)

        await interaction.response.edit_message(embed=embed, view=view)


class RankDropdown(nextcord.ui.Select):
    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx

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

            nextcord.SelectOption(label='Champion', description="1,000,000,000,000,000", emoji = "<:champion:908535801338540042>"),

        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == 'Copper III':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Copper III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '1'
            bet = 1000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Copper II':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Copper II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )


            rank_value = '2'
            bet = 2000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Copper I':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Copper I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '3'
            bet = 3000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Bronze III':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Bronze III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '4'
            bet = 10000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Bronze II':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Bronze II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )


            rank_value = '5'
            bet = 20000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Bronze I':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Bronze I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '6'
            bet = 30000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Silver III':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Silver III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '7'
            bet = 100000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Silver II':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Silver II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '8'
            bet = 200000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Silver I':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Silver I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '9'
            bet = 300000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Gold III':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Gold III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '10'
            bet = 1000000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Gold II':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Gold II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '11'
            bet = 2000000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Gold I':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Gold I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '12'
            bet = 3000000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Platinum III':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Platinum III`rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '13'
            bet = 10000000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Platinum II':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Platinum II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '14'
            bet = 20000000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Platinum I':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Platinum I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '15'
            bet = 30000000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Diamond':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Diamond` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '16'
            bet = 1000000000000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Champion':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Champion`rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = '17'
            bet = 1000000000000000
            view = ConfirmPurchase(self.bot, self.ctx, bet, rank_value)

            await interaction.response.edit_message(embed=embed, view=view)













class RankView(nextcord.ui.View):
    def __init__(self, bot, ctx, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.ctx = ctx
        self.value = None
        self.add_item(RankDropdown(bot, ctx))

    @nextcord.ui.button(label='Main Page', style=nextcord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items.",
            color = nextcord.Color.random()
        )

        view = ShopView(self.bot, self.ctx)

        await interaction.response.edit_message(embed=embed, view=view)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()



class ShopDropdown(nextcord.ui.Select):
    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx

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

            embed.add_field(name = "Champion", value = f"1,000,000,000,000,000", inline=True)

            view = RankView(self.bot, self.ctx)

            await interaction.response.edit_message(embed=embed, view=view)


class ShopView(nextcord.ui.View):
    def __init__(self, bot, ctx, user, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.economy = Database(bot)
        self.bot = bot
        self.ctx = ctx
        self.user = user
        self.value = None
        self.add_item(ShopDropdown(bot, ctx))

    @nextcord.ui.button(label='Main Page', style=nextcord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = self.user.id if self.user else self.ctx.author.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        async with self.bot.db.execute("SELECT rank FROM profile WHERE user_id = ? ORDER BY rank DESC", (user_id,)) as cursor:
            data = await cursor.fetchall()
            if data:
                rank = data[0]
            else:
                rank = "No ranks"

        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items \n\nBalance: {balance:,} \nRanks: {rank}",
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
        user_id = user.id if user else ctx.author.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        async with self.bot.db.execute("SELECT rank FROM profile WHERE user_id = ? ORDER BY rank DESC", (user_id,)) as cursor:
            data = await cursor.fetchall()
            if data:
                rank = data[0]
            else:
                rank = "No ranks"

        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items \n\nBalance: {balance:,} \nRanks: {rank}",
            color = nextcord.Color.random()
        )

        view = ShopView(self.bot, ctx, user)
        await ctx.send(embed=embed, view=view)

        ##TODO: Add a dropdown menu in order for people to choose the category that they want to shop in.
               #Once the category is chosen, figure out a system for how they are going to buy items, e.g. Buttons, Dropdowns, Commands
               #Come up with new ideas to add to the shop in order to make it more interesting for new users, and those with a lot of moneyx


def setup(bot):
    bot.add_cog(Profile(bot))