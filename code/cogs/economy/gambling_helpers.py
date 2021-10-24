import nextcord
from nextcord.ext import commands
from utils.economy import Database
from utils.helpers import *
from datetime import datetime

color = 0xc48aff

class GamblingHelpers(commands.Cog, name='General'):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.economy = Database()


    #Give you ${DEFAULT_BET * B_MULT} once every {B_COOLDOWN}hrs
    #Usage: $add
    @commands.command()
    @commands.cooldown(1, B_COOLDOWN*3600, type=commands.BucketType.user)
    async def add(self, ctx: commands.Context):
        amount = DEFAULT_BET*B_MULT
        self.economy.add_money(ctx.author.id, amount)
        embed = nextcord.Embed(
            title = "I've added $2,500 to you balance",
            description = f"Come back again in {B_COOLDOWN} hours."
        )
        await ctx.send(embed=embed)


    @commands.command(aliases=['profile'])
    async def money(self, ctx: commands.Context, user: nextcord.Member=None):
        user = user.id if user else ctx.author.id
        user = self.bot.get_user(user)
        profile = self.economy.get_entry(user.id)
        embed = make_embed(
            title=user.name,
            description=(
                '**${:,}**'.format(profile[1]) + "\nKeep working to get more money!"
            ),
            footer=nextcord.Embed.Empty
        )
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)


    @money.error
    async def money_error(self, ctx, error):
        if isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
            )
            await ctx.send(embed=embed)

        if isinstance(error, (commands.MissingRequiredArgument, commands.TooManyArguments, commands.BadArgument)):
            await ctx.invoke(self.bot.get_command('help'), ctx.command.name)
            embed = nextcord.Embed(
                colour = color,
                title = "→ Incorrect usage!",
                description = f"• The command you entered used incorrect syntax. Run `$help` to see how to use that command."
            )
            await ctx.send(embed=embed)

        if isinstance(error, InsufficientFundsException):
            await ctx.invoke(self.bot.get_command('money'))

        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            await ctx.send(embed=embed)


    @commands.command(aliases=["top"])
    async def leaderboard(self, ctx):
        entries = self.economy.top_entries(5)
        embed = make_embed(title='Global Economy Leaderboard:', color=nextcord.Color.gold())
        for i, entry in enumerate(entries):
            embed.add_field(
                name=f"{i+1}. {self.bot.get_user(entry[0]).name}",
                value='${:,}'.format(entry[1]),
                inline=False
            )
        await ctx.send(embed=embed)

    
    @leaderboard.error
    async def leaderboard_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(GamblingHelpers(bot))