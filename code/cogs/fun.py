import nextcord
from nextcord.ext import commands
from datetime import datetime
import requests
import json

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def reverse(self, ctx, text):
        text_reverse = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        embed = nextcord.Embed(
            color=nextcord.Colour.orange(),
            title=f"→ Reversed Text",
            description=f"• {text_reverse}"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @reverse.error
    async def reverse_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = nextcord.Embed(
                color=color,
                title="→ Invalid Argument!",
                description=f"• Please provide some text for the bot to reverse. Example: `{ctx.prefix}reverse <text>`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(
                color=color,
                title="→ Invalid Argument!",
                description=f"• Please provide some text for the bot to reverse. Example: `{ctx.prefix}reverse <text>`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @commands.command(aliases=['trump'])
    async def donald(self, ctx):
        response = requests.get('https://api.whatdoestrumpthink.com/api/v1/quotes/random')
        quote = json.loads(response.text)

        embed = nextcord.Embed(
            title = "Donald Trump Quote -",
            description = f"'{quote['message']}'",
            colour = nextcord.Colour.random()
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def kanye(self, ctx):
        response = requests.get('https://api.kanye.rest/')
        quote = json.loads(response.text)

        embed = nextcord.Embed(
            title = "Kanye West Quote -",
            description = f"'{quote['quote']}'",
            colour = nextcord.Colour.random()
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))