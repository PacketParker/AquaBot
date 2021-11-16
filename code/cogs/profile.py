import nextcord
from nextcord.ext import commands
from utils.economy import Database
from utils.helpers import *
from PIL import Image
from utils.helpers import DEFAULT_PREFIX, InsufficientFundsException
import sqlite3

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48af

class Economy:
    def __init__(self, bot):
        self.bot = bot
        self.economy = Database(bot)

    async def check_bet(
        self,
        user_id,
        bet: int=DEFAULT_BET,
    ):
        bet = int(bet)
        if bet <= 0:
            raise commands.errors.BadArgument()
        current = (await self.economy.get_entry(user_id))[1]
        if bet > current:
            raise InsufficientFundsException()


class AfterPurchase(nextcord.ui.View):
    def __init__(self, bot, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.economy = Database(bot)
        self.value = None

    @nextcord.ui.button(label='Main Page', style=nextcord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = interaction.user.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        async with self.bot.db.execute("SELECT rank_name FROM profile WHERE user_id = ? ORDER BY rank_int DESC", (user_id,)) as cursor:
            data = await cursor.fetchall()
            if data:
                names = ', '.join([str(i[0]) for i in data])

            else:
                names = "No ranks"

        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items \n\nBalance: **${balance:,}** \n\nRanks: **{names}**",
            color = nextcord.Color.random()
        )

        view = ShopView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()


class ConfirmPurchase(nextcord.ui.View):
    def __init__(self, bot, bet, rank_value, rank_name, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.bet = bet
        self.rank_int = int(rank_value)
        self.rank_name = str(rank_name)
        self.check = Economy(bot)
        self.economy = Database(bot)
        self.add_item(RankDropdown(bot))


    @nextcord.ui.button(label='Yes', style=nextcord.ButtonStyle.green, row=2)
    async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = interaction.user.id

        async with self.bot.db.execute("SELECT rank_name, rank_int FROM profile WHERE user_id = ?", (user_id,)) as cursor:
            try:
                await self.bot.db.execute("INSERT INTO profile (user_id, rank_name, rank_int) VALUES(?,?,?)", (user_id, self.rank_name, self.rank_int))
                await self.bot.db.commit()
                await self.check.check_bet(user_id, self.bet)
                await self.economy.add_money(user_id, self.bet*-1)

                embed = nextcord.Embed(
                    title = "Purchase Successful",
                    description = f"Your purchase was successful. In order to purchase more items, please click the main page button below.",
                    color = nextcord.Color.random()
                )

                view = AfterPurchase(self.bot)
                await interaction.response.edit_message(embed=embed, view=view)

            except sqlite3.IntegrityError:
                embed = nextcord.Embed(
                    title = "Rank Already Owned",
                    description = f"You already have that rank and therefore cannot buy it again. Try purchasing another rank.",
                    color = nextcord.Color.random()
                )

                view = RankView(self.bot)
                return await interaction.response.edit_message(embed=embed, view=view)


    @nextcord.ui.button(label='No', style=nextcord.ButtonStyle.red, row=2)
    async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Purchase Canceled, Taken Back to Shop",
            description = f"Choose from one of the categories below in order to shop for items.",
            color = nextcord.Color.random()
        )

        view = ShopView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)


class RankDropdown(nextcord.ui.Select):
    def __init__(self, bot):
        self.bot = bot

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

            rank_value = 1
            rank_name = 'Copper III'
            bet = 1000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Copper II':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Copper II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 2
            rank_name = 'Copper II'
            bet = 2000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Copper I':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Copper I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 3
            rank_name = 'Copper I'
            bet = 3000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Bronze III':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Bronze III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 4
            rank_name = 'Bronze III'
            bet = 10000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Bronze II':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Bronze II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 5
            rank_name = 'Bronze II'
            bet = 20000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Bronze I':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Bronze I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 6
            rank_name = 'Bronze I'
            bet = 30000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Silver III':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Silver III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 7
            rank_name = 'Silver III'
            bet = 100000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Silver II':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Silver II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 8
            rank_name = 'Silver II'
            bet = 200000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Silver I':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Silver I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 9
            rank_name = 'Silver I'
            bet = 300000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Gold III':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Gold III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 10
            rank_name = 'Gold III'
            bet = 1000000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Gold II':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Gold II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 11
            rank_name = 'Gold II'
            bet = 2000000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Gold I':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Gold I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 12
            rank_name = 'Gold I'
            bet = 3000000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Platinum III':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Platinum III`rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 13
            rank_name = 'Platinum III'
            bet = 10000000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Platinum II':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Platinum II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 14
            rank_name = 'Platinum II'
            bet = 20000000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Platinum I':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Platinum I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 15
            rank_name = 'Platinum I'
            bet = 30000000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Diamond':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Diamond` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 16
            rank_name = 'Diamond'
            bet = 1000000000000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Champion':
            embed = nextcord.Embed(
                title = "Please Confirm Your Purchase",
                description = "If you are sure you would like to purchase the `Champion`rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                colour = nextcord.Colour.random()
            )

            rank_value = 17
            rank_name = 'Champion'
            bet = 1000000000000000

            view = ConfirmPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)


class RankView(nextcord.ui.View):
    def __init__(self, bot, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.economy = Database(bot)
        self.add_item(RankDropdown(bot))


    @nextcord.ui.button(label='Main Page', style=nextcord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = interaction.user.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        async with self.bot.db.execute("SELECT rank_name FROM profile WHERE user_id = ? ORDER BY rank_int DESC", (user_id,)) as cursor:
            data = await cursor.fetchall()
            if data:
                names = ', '.join([str(i[0]) for i in data])

            else:
                names = "No ranks"
        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items \n\nBalance: **${balance:,}** \n\nRanks: **{names}**",
            color = nextcord.Color.random()
        )

        view = ShopView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()


class ShopDropdown(nextcord.ui.Select):
    def __init__(self, bot):
        self.bot = bot

        options = [
            nextcord.SelectOption(label='Ranks', description='Buy ranks and show off your wealth'),
        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)


    async def callback(self, interaction: nextcord.Interaction):
        user_id = interaction.user.id
        async with self.bot.db.execute("SELECT rank_name FROM profile WHERE user_id = ? ORDER BY rank_int DESC", (user_id,)) as cursor:
            data = await cursor.fetchall()
            if data:
                names = ', '.join([str(i[0]) for i in data])

                if "Copper III," in names:
                    copper_iii = "~~Copper III~~ - OWNED"
                else:
                    copper_iii = "Copper III"

                if "Copper II," in names:
                    copper_ii = "~~Copper II~~ - OWNED"
                else:
                    copper_ii = "Copper II"

                if "Copper I," in names:
                    copper_i = "~~Copper I~~ - OWNED"
                else:
                    copper_i = "Copper I"

                if "Bronze III," in names:
                    bronze_iii = "~~Bronze III~~ - OWNED"
                else:
                    bronze_iii = "Bronze III"

                if "Bronze II," in names:
                    bronze_ii = "~~Bronze II~~ - OWNED"
                else:
                    bronze_ii = "Bronze II"

                if "Bronze I," in names:
                    bronze_i = "~~Bronze I~~ - OWNED"
                else:
                    bronze_i = "Bronze I"

                if "Silver III," in names:
                    silver_iii = "~~Silver III~~ - OWNED"
                else:
                    silver_iii = "Silver III"

                if "Silver II," in names:
                    silver_ii = "~~Silver II~~ - OWNED"
                else:
                    silver_ii = "Silver II"

                if "Silver I," in names:
                    silver_i = "~~Silver I~~ - OWNED"
                else:
                    silver_i = "Silver I"

                if "Gold III," in names:
                    gold_iii = "~~Gold III~~ - OWNED"
                else:
                    gold_iii = "Gold III"

                if "Gold II," in names:
                    gold_ii = "~~Gold II~~ - OWNED"
                else:
                    gold_ii = "Gold II"

                if "Gold I," in names:
                    gold_i = "~~Gold I~~ - OWNED"
                else:
                    gold_i = "Gold I"

                if "Platinum III," in names:
                    platinum_iii = "~~Platinum III~~ - OWNED"
                else:
                    platinum_iii = "Platinum III"

                if "Platinum II," in names:
                    platinum_ii = "~~Platinum II~~ - OWNED"
                else:
                    platinum_ii = "Platinum II"

                if "Platinum I," in names:
                    platinum_i = "~~Platinum I~~ - OWNED"
                else:
                    platinum_i = "Platinum I"

                if "Diamond," in names:
                    diamond = "~~Diamond~~ - OWNED"
                else:
                    diamond = "Diamond"

                if "Champion," in names:
                    champion = "~~Champion~~ - OWNED"
                else:
                    champion = "Champion"
            else:
                return

        if self.values[0] == 'Ranks':
            embed = nextcord.Embed(
                title = "Ranks \nSpend your money in order to get more ranks.",
                description = "**Purchase a rank by clicking on one of the dropdown menus below, and then confirming your purchase.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = f"{copper_iii}", value = f"1,000", inline=True)
            embed.add_field(name = f"{copper_ii}", value = f"2,000", inline=True)
            embed.add_field(name = f"{copper_i}", value = f"3,000", inline=True)

            embed.add_field(name = f"{bronze_iii}", value = f"10,000", inline=True)
            embed.add_field(name = f"{bronze_ii}", value = f"20,000", inline=True)
            embed.add_field(name = f"{bronze_i}", value = f"30,000", inline=True)

            embed.add_field(name = f"{silver_iii}", value = f"100,000", inline=True)
            embed.add_field(name = f"{silver_ii}", value = f"200,000", inline=True)
            embed.add_field(name = f"{silver_i}", value = f"300,000", inline=True)

            embed.add_field(name = f"{gold_iii}", value = f"1,000,000", inline=True)
            embed.add_field(name = f"{gold_ii}", value = f"2,000,000", inline=True)
            embed.add_field(name = f"{gold_i}", value = f"3,000,000", inline=True)

            embed.add_field(name = f"{platinum_iii}", value = f"10,000,000", inline=True)
            embed.add_field(name = f"{platinum_ii}", value = f"20,000,000", inline=True)
            embed.add_field(name = f"{platinum_i}", value = f"30,000,000", inline=True)
            
            embed.add_field(name = f"{diamond}", value = f"1,000,000,000,000", inline=True)

            embed.add_field(name = f"{champion}", value = f"1,000,000,000,000,000", inline=True)

            view = RankView(self.bot)
            await interaction.response.edit_message(embed=embed, view=view)


class ShopView(nextcord.ui.View):
    def __init__(self, bot, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.economy = Database(bot)
        self.bot = bot
        self.add_item(ShopDropdown(bot))


    @nextcord.ui.button(label='Main Page', style=nextcord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user_id = interaction.user.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        async with self.bot.db.execute("SELECT rank_name FROM profile WHERE user_id = ? ORDER BY rank_int DESC", (user_id,)) as cursor:
            data = await cursor.fetchall()
            if data:
                names = ', '.join([str(i[0]) for i in data])

            else:
                names = "No ranks"

        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items \n\nBalance: **${balance:,}** \n\nRanks: **{names}**",
            color = nextcord.Color.random()
        )

        view = ShopView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)


    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy = Database(bot)


    @commands.command()
    async def profile(self, ctx, *, user: nextcord.User=None):
        user_id = user.id if user else ctx.author.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        async with self.bot.db.execute("SELECT rank_name FROM profile WHERE user_id = ? ORDER BY rank_int DESC", (user_id,)) as cursor:
            data = await cursor.fetchall()
            if data:
                names = ', '.join([str(i[0]) for i in data])

            else:
                names = "No ranks"

        embed = nextcord.Embed(
            title = f"Profile For - {await self.bot.fetch_user(user_id)}",
            description = f"Below will show all economy information for this user",
            color = nextcord.Color.random()
        )

        embed.add_field(name = "Money Balance:", value = f"${balance:,}", inline=False)
        embed.add_field(name = "Ranks:", value = f"{names}", inline=False)

        await ctx.send(embed=embed)


    @commands.command()
    async def shop(self, ctx):
        user_id = ctx.author.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        async with self.bot.db.execute("SELECT rank_name FROM profile WHERE user_id = ? ORDER BY rank_int DESC", (user_id,)) as cursor:
            data = await cursor.fetchall()
            if data:
                names = ', '.join([str(i[0]) for i in data])

            else:
                names = "No ranks"

        embed = nextcord.Embed(
            title = "Shop",
            description = f"Choose from one of the categories below in order to shop for items \n\nBalance: **${balance:,}** \n\nRanks: **{names}**",
            color = nextcord.Color.random()
        )

        view = ShopView(self.bot)
        await ctx.send(embed=embed, view=view)

        ##TODO: Add a dropdown menu in order for people to choose the category that they want to shop in.
               #Once the category is chosen, figure out a system for how they are going to buy items, e.g. Buttons, Dropdowns, Commands
               #Come up with new ideas to add to the shop in order to make it more interesting for new users, and those with a lot of moneyx


def setup(bot):
    bot.add_cog(Profile(bot))
