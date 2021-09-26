import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request
import secrets
from io import BytesIO

log_channel_id = 889293946801516554

black = 0x000000

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def covid(self, ctx):
        URL = "https://disease.sh/v3/covid-19/all"

        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                cases = data["cases"]
                deaths = data["deaths"]
                recovered = data["recovered"]
                active = data["active"]
                countries = data["affectedCountries"]

                embed = nextcord.Embed(
                    title = "World COVID-19 Data",
                    colour = black
                )

                embed.add_field(name=":microbe: Total cases", value=f"{cases:,}", inline=True)
                embed.add_field(name=":skull_crossbones: Total deaths", value=f"{deaths:,}", inline=True)
                embed.add_field(name=":syringe: Total recovered", value=f"{recovered:,}", inline=True)
                embed.add_field(name="Total active cases", value=f"{active:,}", inline=True)
                embed.add_field(name=":map: Total affected countries", value=f"{countries:,}", inline=True)

                await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {response.status} status.")


    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept any numbers between 3-1400")
        if hasattr(ctx, "guild") and ctx.guild is not None:
            await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
        await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")


def setup(bot):
    bot.add_cog(Misc(bot))
