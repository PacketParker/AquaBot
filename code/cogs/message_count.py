import nextcord
from nextcord import Color
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request
from database.database import Database
from utils.helpers import *
from utils.helpers import PREFIX, InsufficientFundsException

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff

class messageCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.level = Database()
        self.economy = Database()


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        self.level.add_message(user_id)




    @commands.command()
    async def level(self, ctx: commands.Context, user: nextcord.Member=None):
        user = user.id if user else ctx.author.id
        user = self.bot.get_user(user)
        profile = self.level.message_get_entry(user.id)
        embed = make_embed(
            title=user.name + " - Total Messages",
            description=(
                '**{:,}**'.format(profile[1]) + "\n\n NOTE: This is all of your messages you have sent in servers that have this bot."
            ),
            footer=nextcord.Embed.Empty
        )
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)


    @level.error
    async def level_error(self, ctx, error):
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
            await ctx.invoke(self.bot.get_command('level'))

        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            await ctx.send(embed=embed)


    #Shows the user with the most money
    #Usage: $leaderboard
    @commands.command()
    async def leaderboard(self, ctx):
        embed = nextcord.Embed(
            title = "Economy and Message Count Leaderboard",
            description = "These numbers go across all servers, and are not exclusive to just this server.",
            color = color if color else Color.random()
        )

        entries = self.economy.top_entries(5)
        for i, entry in enumerate(entries):
            embed.add_field(name = "Money Leaderboard", value = f"**\n{i+1}. {self.bot.get_user(entry[0]).name}** \n ${format(entry[1])}", inline=False)
        
        messageentries = self.level.message_top_entries(5)
        for i, entry in enumerate(messageentries):
            embed.add_field(name = "Message Leaderboard", value = f"**\n{i+1}. {self.bot.get_user(entry[0]).name}** \n{format(entry[1])}", inline=False)

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(messageCount(bot))
