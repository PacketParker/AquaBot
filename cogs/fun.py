import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request
import aiohttp
import random

log_channel_id = 889293946801516554

black = 0x000000


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["slots", "bet"])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")


    @commands.command()
    async def reverse(self, ctx, text):
        text_reverse = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        embed = nextcord.Embed(
            color=nextcord.Colour.orange(),
            title=f"→ Reversed Text",
            description=f"• {text_reverse}"
        )

        await ctx.send(embed=embed)


    @reverse.error
    async def reverse_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(
                color=nextcord.Colour.orange(),
                title="→ Invalid Argument!",
                description="• Please put a valid option! Example: `l!reverse <text>`"
            )
            await ctx.send(embed=embed)


    @commands.command(aliases=['tronalddump', 'tronald', 'donaldtrump', 'trump'])
    async def donald(self, ctx):
        """Collect a random stupid quote from Donald Trump"""
        url = 'https://www.tronalddump.io/random/quote'
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(url) as r:
                data = await r.json()
        await ctx.send(f'**Donald Trump:** {data["value"].capitalize()}')


def setup(bot):
    bot.add_cog(fun(bot))