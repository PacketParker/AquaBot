import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError
from utils.economy import Database
from utils.helpers import *

color = 0xc48aff

class GamblingHelpers(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.economy = Database(bot)


    #Give you {DEFAULT_BET * B_MULT} once every {B_COOLDOWN}hrs
    #Usage: add
    @commands.command()
    @commands.cooldown(1, B_COOLDOWN*3600, type=commands.BucketType.user)
    async def add(self, ctx: commands.Context):
        "Add $2,500 to your balance every 2 hours"
        amount = DEFAULT_BET*B_MULT
        await self.economy.add_money(ctx.author.id, amount)
        embed = discord.Embed(
            title = "I've added $2,500 to you balance",
            description = f"Come back again in {B_COOLDOWN} hours."
        )
        await ctx.send(embed=embed)


    @commands.command(slash_command=False)
    @commands.is_owner()
    async def refund(self, ctx: commands.Context, user: int = None, amount: int = None):
        await self.bot.fetch_user(user)
        await self.economy.add_money(user, amount)
        member = self.bot.get_user(user)
        await ctx.send(f"{member.mention} has been compensated with ${amount:,}")


    @refund.error
    async def refund_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ Invalid ID!",
                description = f"• That is not a valid ID of a member, please provide a valid member ID to be refunded."
            )
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                colour = color,
                title = "→ You Are Not The Owner!",
                description = f"• You can not run that command because you are not the bot owner."
            )
            await ctx.send(embed=embed, ephemeral=True)


    @commands.command(slash_command=False)
    @commands.is_owner()
    async def deduct(self, ctx: commands.Context, user: int = None, amount: int = None):
        await self.bot.fetch_user(user)
        await self.economy.add_money(user, amount*-1)
        member = self.bot.get_user(user)
        await ctx.send(f"{member.mention} has had ${amount:,} deducted form their account.")


    @deduct.error
    async def deduct_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ Invalid ID!",
                description = f"• That is not a valid ID of a member, please provide a valid member ID to be refunded."
            )
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                colour = color,
                title = "→ You Are Not The Owner!",
                description = f"• You can not run that command because you are not the bot owner."
            )
            await ctx.send(embed=embed, ephemeral=True)


    @commands.command()
    async def money(self, ctx: commands.Context):
        "Shows the current balance for your account"
        user = ctx.author.id
        user = self.bot.get_user(user)
        profile = await self.economy.get_entry(user.id)
        embed = make_embed(
            title=user.name,
            description=(
                '**${:,}**'.format(profile[1]) + "\nKeep working to get more money!"
            ),
            footer=discord.Embed.Empty
        )
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)


    @money.error
    async def money_error(self, ctx, error):
        embed = discord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
        )
        await ctx.send(embed=embed, ephemeral=True)


    @commands.command()
    async def leaderboard(self, ctx):
        "Show the global currency leaderboard"
        entries = await self.economy.top_entries(5)
        embed = make_embed(title='Global Economy Leaderboard:', color=discord.Color.gold())
        for i, entry in enumerate(entries): 
            id = entry[0]
            name = await self.bot.fetch_user(id)
            embed.add_field(
                name=f"{i+1}. {name}",
                value='${:,}'.format(entry[1]),
                inline=False
            )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(GamblingHelpers(bot))