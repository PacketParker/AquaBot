import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request

log_channel_id = 889293946801516554

black = 0x000000

class misc(commands.Cog):
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



def setup(bot):
    bot.add_cog(misc(bot))
