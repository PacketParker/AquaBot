import discord
import datetime
from discord.ext import commands
from economy_schema import Database
import psycopg2
from discord import app_commands
from reader import InsufficientFundsException, BOT_COLOR
from bot import CONNECTION

color = 0xc48af

class Economy:
    def __init__(self, bot):
        self.bot = bot
        self.economy = Database(bot)

    async def check_bet(
        self,
        user_id,
        bet,
    ):
        bet = int(bet)
        if bet <= 0:
            raise commands.errors.BadArgument()
        current = (await self.economy.get_entry(user_id))[1]
        if bet > current:
            raise InsufficientFundsException()

#BEGIN CODE FOR RANK PURCHASING

class AfterRankPurchase(discord.ui.View):
    def __init__(self, bot, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.economy = Database(bot)
        self.value = None

    @discord.ui.button(label='Main Page', style=discord.ButtonStyle.blurple, row=2)
    async def main_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        cur = CONNECTION.cursor()
        cur.execute("SELECT rank_name FROM profile WHERE user_id = %s ORDER BY rank_int DESC", (user_id,))
        data = cur.fetchall()
        if data:
            names = ', '.join([str(i[0]) for i in data])

        else:
            names = "No ranks"

        embed = discord.Embed(
            title="Shop",
            description=f"Choose from one of the categories below in order to shop for items \n\nBalance: **${balance:,}** \n\nRanks: **{names}**",
            color=BOT_COLOR
        )
        view = ShopView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)


class ConfirmRankPurchase(discord.ui.View):
    def __init__(self, bot, bet, rank_value, rank_name, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.bet = bet
        self.rank_int = int(rank_value)
        self.rank_name = str(rank_name)
        self.check = Economy(bot)
        self.economy = Database(bot)
        self.add_item(RankDropdown(bot))


    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green, row=2)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id

        cur = CONNECTION.cursor()
        try:
            await self.check.check_bet(user_id, self.bet)
            cur.execute("INSERT INTO profile (user_id, rank_name, rank_int) VALUES(%s,%s,%s)", (user_id, self.rank_name, self.rank_int))
            CONNECTION.commit()
            await self.economy.add_money(user_id, self.bet*-1)

            embed = discord.Embed(
                title="Purchase Successful",
                description=f"Your purchase was successful. In order to purchase more items, please click the main page button below.",
                color=BOT_COLOR
            )
            view = AfterRankPurchase(self.bot)
            await interaction.response.edit_message(embed=embed, view=view)

        except psycopg2.errors.UniqueViolation:
            embed = discord.Embed(
                title="Rank Already Owned",
                description=f"You already have that rank and therefore cannot buy it again. Try purchasing another rank.",
                color=BOT_COLOR
            )
            view = RankView(self.bot)
            return await interaction.response.edit_message(embed=embed, view=view)

        except InsufficientFundsException:
            embed = discord.Embed(
                title="Not Enough Money",
                description=f"You do not have enough money to make that purchase, come back once you've earned some more money.",
                color=BOT_COLOR
            )
            view = RankView(self.bot)
            return await interaction.response.edit_message(embed=embed, view=view)


    @discord.ui.button(label='No', style=discord.ButtonStyle.red, row=2)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Purchase Cancelled, Taken Back to Shop",
            description=f"Choose from one of the categories below in order to shop for items.",
            color=BOT_COLOR
        )
        view = ShopView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)


class RankDropdown(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot

        options = [
            discord.SelectOption(label='Copper III', description="100,000", emoji = "<:copper_3:908535582534299688>"),
            discord.SelectOption(label='Copper II', description="200,000", emoji = "<:copper_2:908535594714558524>"),
            discord.SelectOption(label='Copper I', description="300,000", emoji = "<:copper_1:908535605644918895>"),

            discord.SelectOption(label='Bronze III', description="100,000,000", emoji = "<:bronze_3:908535616650760222>"),
            discord.SelectOption(label='Bronze II', description="200,000,000", emoji = "<:bronze_2:908535628503863296>"),
            discord.SelectOption(label='Bronze I', description="300,000,000", emoji = "<:bronze_1:908535639606198292>"),

            discord.SelectOption(label='Silver III', description="100,000,000,000", emoji = "<:silver_3:908535654667911168>"),
            discord.SelectOption(label='Silver II', description="200,000,000,000", emoji = "<:silver_2:908535667263434782>"),
            discord.SelectOption(label='Silver I', description="300,000,000,000", emoji = "<:silver_1:908535680064442398>"),

            discord.SelectOption(label='Gold III', description="100,000,000,000,000", emoji = "<:gold_3:908535691137388554>"),
            discord.SelectOption(label='Gold II', description="200,000,000,000,000", emoji = "<:gold_2:908535705154764870>"),
            discord.SelectOption(label='Gold I', description="300,000,000,000,000", emoji = "<:gold_1:908535742224027758>"),

            discord.SelectOption(label='Platinum III', description="100,000,000,000,000,000", emoji = "<:platinum_3:908535751900282880>"),
            discord.SelectOption(label='Platinum II', description="200,000,000,000,000,000", emoji = "<:platinum_2:908535764629999656>"),
            discord.SelectOption(label='Platinum I', description="300,000,000,000,000,000", emoji = "<:platinum_1:908535773689679932>"),

            discord.SelectOption(label='Diamond', description="123,456,789,000,000,000,000", emoji = "<:diamond:908535791700037702>"),

            discord.SelectOption(label='Champion', description="999,999,999,999,999,999,999,999,999", emoji = "<:champion:908535801338540042>"),

        ]

        super().__init__(placeholder='Choose a rank...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'Copper III':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Copper III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 1
            rank_name = 'Copper III'
            bet = 100000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Copper II':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Copper II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 2
            rank_name = 'Copper II'
            bet = 200000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Copper I':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Copper I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 3
            rank_name = 'Copper I'
            bet = 300000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Bronze III':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Bronze III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 4
            rank_name = 'Bronze III'
            bet = 100000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Bronze II':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Bronze II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 5
            rank_name = 'Bronze II'
            bet = 200000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Bronze I':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Bronze I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 6
            rank_name = 'Bronze I'
            bet = 300000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Silver III':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Silver III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 7
            rank_name = 'Silver III'
            bet = 100000000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Silver II':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Silver II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 8
            rank_name = 'Silver II'
            bet = 200000000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Silver I':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Silver I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 9
            rank_name = 'Silver I'
            bet = 300000000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Gold III':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Gold III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 10
            rank_name = 'Gold III'
            bet = 100000000000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Gold II':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Gold II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 11
            rank_name = 'Gold II'
            bet = 200000000000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Gold I':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Gold I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 12
            rank_name = 'Gold I'
            bet = 300000000000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Platinum III':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Platinum III` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 13
            rank_name = 'Platinum III'
            bet = 100000000000000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Platinum II':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Platinum II` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 14
            rank_name = 'Platinum II'
            bet = 200000000000000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Platinum I':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Platinum I` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 15
            rank_name = 'Platinum I'
            bet = 300000000000000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Diamond':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Diamond` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 16
            rank_name = 'Diamond'
            bet = 123456789000000000000

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)

        if self.values[0] == 'Champion':
            embed = discord.Embed(
                title="Please Confirm Your Purchase",
                description="If you are sure you would like to purchase the `Champion` rank, please click the 'Yes' button below, otherwise click the 'No' button.",
                color=BOT_COLOR
            )

            rank_value = 17
            rank_name = 'Champion'
            bet = 999999999999999999999999999

            view = ConfirmRankPurchase(self.bot, bet, rank_value, rank_name)
            await interaction.response.edit_message(embed=embed, view=view)


class RankView(discord.ui.View):
    def __init__(self, bot, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.economy = Database(bot)
        self.add_item(RankDropdown(bot))


    @discord.ui.button(label='Main Page', style=discord.ButtonStyle.blurple, row=2)
    async def main_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        cur = CONNECTION.cursor()
        cur.execute("SELECT rank_name FROM profile WHERE user_id = %s ORDER BY rank_int DESC", (user_id,))
        data = cur.fetchall()
        if data:
            names = ', '.join([str(i[0]) for i in data])

        else:
            names = "No ranks"

        embed = discord.Embed(
            title="Shop",
            description=f"Choose from one of the categories below in order to shop for items \n\nBalance: **${balance:,}** \n\nRanks: **{names}**",
            color=BOT_COLOR
        )
        view = ShopView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)


##END RANK AND BEGIN PROFILE AND OTHER MAIN SHOP VIEWING


class ShopDropdown(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot

        options = [
            discord.SelectOption(label='Ranks', description='Buy ranks and show off your wealth'),
        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        cur = CONNECTION.cursor()
        cur.execute("SELECT rank_name FROM profile WHERE user_id = %s ORDER BY rank_int DESC", (user_id,))
        data = cur.fetchall()
        if data:
            names = ([str(i[0]) for i in data])

            if "Copper III" in names:
                copper_iii = "~~Copper III~~ - OWNED"
            else:
                copper_iii = "Copper III"

            if "Copper II" in names:
                copper_ii = "~~Copper II~~ - OWNED"
            else:
                copper_ii = "Copper II"

            if "Copper I" in names:
                copper_i = "~~Copper I~~ - OWNED"
            else:
                copper_i = "Copper I"

            if "Bronze III" in names:
                bronze_iii = "~~Bronze III~~ - OWNED"
            else:
                bronze_iii = "Bronze III"

            if "Bronze II" in names:
                bronze_ii = "~~Bronze II~~ - OWNED"
            else:
                bronze_ii = "Bronze II"

            if "Bronze I" in names:
                bronze_i = "~~Bronze I~~ - OWNED"
            else:
                bronze_i = "Bronze I"

            if "Silver III" in names:
                silver_iii = "~~Silver III~~ - OWNED"
            else:
                silver_iii = "Silver III"

            if "Silver II" in names:
                silver_ii = "~~Silver II~~ - OWNED"
            else:
                silver_ii = "Silver II"

            if "Silver I" in names:
                silver_i = "~~Silver I~~ - OWNED"
            else:
                silver_i = "Silver I"

            if "Gold III" in names:
                gold_iii = "~~Gold III~~ - OWNED"
            else:
                gold_iii = "Gold III"

            if "Gold II" in names:
                gold_ii = "~~Gold II~~ - OWNED"
            else:
                gold_ii = "Gold II"

            if "Gold I" in names:
                gold_i = "~~Gold I~~ - OWNED"
            else:
                gold_i = "Gold I"

            if "Platinum III" in names:
                platinum_iii = "~~Platinum III~~ - OWNED"
            else:
                platinum_iii = "Platinum III"

            if "Platinum II" in names:
                platinum_ii = "~~Platinum II~~ - OWNED"
            else:
                platinum_ii = "Platinum II"

            if "Platinum I" in names:
                platinum_i = "~~Platinum I~~ - OWNED"
            else:
                platinum_i = "Platinum I"

            if "Diamond" in names:
                diamond = "~~Diamond~~ - OWNED"
            else:
                diamond = "Diamond"

            if "Champion" in names:
                champion = "~~Champion~~ - OWNED"
            else:
                champion = "Champion"
        else:
            copper_iii = "Copper III"
            copper_ii = "Copper II"
            copper_i = "Copper I"
            bronze_iii = "Bronze III"
            bronze_ii = "Bronze II"
            bronze_i = "Bronze I"
            silver_iii = "Silver III"
            silver_ii = "Silver II"
            silver_i = "Silver I"
            gold_iii = "Gold III"
            gold_ii = "Gold II"
            gold_i = "Gold I"
            platinum_iii = "Platinum III"
            platinum_ii = "Platinum II"
            platinum_i = "Platinum I"
            diamond = "Diamond"
            champion = "Champion"

        if self.values[0] == 'Ranks':
            embed = discord.Embed(
                title="Ranks \nSpend your money in order to get more ranks.",
                description="**Purchase a rank by clicking on one of the dropdown menus below, and then confirming your purchase.**",
                color=BOT_COLOR
            )

            embed.add_field(name=f"{copper_iii}", value=f"```100,000```", inline=True)
            embed.add_field(name=f"{copper_ii}", value=f"```200,000```", inline=True)
            embed.add_field(name=f"{copper_i}", value=f"```300,000```", inline=True)

            embed.add_field(name=f"{bronze_iii}", value=f"```100,000,000```", inline=True)
            embed.add_field(name=f"{bronze_ii}", value=f"```200,000,000```", inline=True)
            embed.add_field(name=f"{bronze_i}", value=f"```300,000,000```", inline=True)

            embed.add_field(name=f"{silver_iii}", value=f"```100,000,000,000\n(100 bil.)```", inline=True)
            embed.add_field(name=f"{silver_ii}", value=f"```200,000,000,000\n(200 bil.)```", inline=True)
            embed.add_field(name=f"{silver_i}", value=f"```300,000,000,000\n(300 bil.)```", inline=True)

            embed.add_field(name=f"{gold_iii}", value=f"```100,000,000,000,\n000  (100 tril.)```", inline=True)
            embed.add_field(name=f"{gold_ii}", value=f"```200,000,000,000,\n000  (200 tril.)```", inline=True)
            embed.add_field(name=f"{gold_i}", value=f"```300,000,000,000,\n000  (300 tril.)```", inline=True)

            embed.add_field(name=f"{platinum_iii}", value=f"```100,000,000,000,000,000  (100 quad.)```", inline=True)
            embed.add_field(name=f"{platinum_ii}", value=f"```200,000,000,000,000,000  (200 quad.)```", inline=True)
            embed.add_field(name=f"{platinum_i}", value=f"```300,000,000,000,000,000  (300 quad.)```", inline=True)

            embed.add_field(name=f"{diamond}", value=f"```123,456,789,000,000,000,000\n(<123 quint.)```", inline=True)

            embed.add_field(name=f"{champion}", value=f"```999,999,999,999,999,999,999,\n999,999 (<999 sept.)```", inline=True)

            view = RankView(self.bot)
            await interaction.response.edit_message(embed=embed, view=view)


class ShopView(discord.ui.View):
    def __init__(self, bot, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.economy = Database(bot)
        self.bot = bot
        self.add_item(ShopDropdown(bot))


    @discord.ui.button(label='Main Page', style=discord.ButtonStyle.blurple, row=2)
    async def main_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        cur = CONNECTION.cursor()
        cur.execute("SELECT rank_name FROM profile WHERE user_id = %s ORDER BY rank_int DESC", (user_id,))
        data = cur.fetchall()
        if data:
            names = ', '.join([str(i[0]) for i in data])

        else:
            names = "No ranks"

        embed = discord.Embed(
            title="Shop",
            description=f"Choose from one of the categories below in order to shop for items \n\nBalance: **${balance:,}** \n\nRanks: **{names}**",
            color=BOT_COLOR
        )
        view = ShopView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)


#BEGIN CODE FOR PROFILE VIEWING


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy = Database(bot)


    @app_commands.command()
    @app_commands.describe(user='User whose profile you would like to view')
    async def profile(
        self,
        interaction: discord.Interaction,
        user: discord.Member
    ):
        "Show the profile for the given user"
        user_id = user.id if user else interaction.user.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        cur = CONNECTION.cursor()
        cur.execute("SELECT rank_name FROM profile WHERE user_id = %s ORDER BY rank_int DESC", (user_id,))
        data = cur.fetchall()
        if data:
            names = ', '.join([str(i[0]) for i in data])

        else:
            names = "No ranks"

        embed = discord.Embed(
            title=f"Profile For - {await self.bot.fetch_user(user_id)}",
            description=f"Below will show all economy information for this user",
            color=BOT_COLOR
        )

        embed.add_field(name="Money Balance:", value=f"${balance:,}", inline=False)
        embed.add_field(name="Ranks:", value=f"{names}", inline=False)
        embed.set_thumbnail(url = user.avatar.url)
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def shop(
        self,
        interaction: discord.Interaction
    ):
        "Shows the shop so that you can buy items"
        user_id = interaction.user.id
        profile = await self.economy.get_entry(user_id)
        balance = profile[1]

        cur = CONNECTION.cursor()
        cur.execute("SELECT rank_name FROM profile WHERE user_id = %s ORDER BY rank_int DESC", (user_id,))
        data = cur.fetchall()
        if data:
            names = ', '.join([str(i[0]) for i in data])

        else:
            names = "No ranks"

        embed = discord.Embed(
            title="Shop",
            description=f"Choose from one of the categories below in order to shop for items \n\nBalance: **${balance:,}** \n\nRanks: **{names}**",
            color=BOT_COLOR
        )
        view = ShopView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Profile(bot))