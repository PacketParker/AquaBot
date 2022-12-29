import discord
from discord.ext import commands, tasks
from discord import app_commands
import requests

covid_dict = {'total_cases':0, 'total_deaths':0, 'total_recovered':0, 'active_cases':0, 
    'critical_cases':0, 'cases_today':0, 'deaths_today':0, 'tests':0}

class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    async def cog_load(self):
        self.update_covid.start()


    @tasks.loop(seconds=300)
    async def update_covid(self):
        response = requests.get("https://disease.sh/v3/covid-19/all")

        if response.status_code == 200:
            data = response.json()
            cases = int(data["cases"])
            deaths = int(data["deaths"])
            recovered = int(data["recovered"])
            active = int(data["active"])
            critical = int(data["critical"])
            cases_today = int(data["todayCases"])
            deaths_today = int(data["todayDeaths"])
            tests = int(data["tests"])
        
        else:
            return

        update_crypto_dict = {'total_cases':cases, 'total_deaths':deaths, 
        'total_recovered':recovered, 'active_cases':active, 'critical_cases':critical,
        'cases_today':cases_today, 'deaths_today':deaths_today, 'tests':tests}

        covid_dict.update(update_crypto_dict)


    @app_commands.command()
    async def covid(
        self, 
        interaction: discord.Interaction
    ):
        "Get current global Covid-19 data"
        embed = discord.Embed(
            title = "World COVID-19 Data",
            description = "Data is updated once every 5 minutes",
            colour = 0x000000
        )

        embed.add_field(name="Total Cases", value=f"```{covid_dict['total_cases']:,}```", inline=True)
        embed.add_field(name="Total Deaths", value=f"```{covid_dict['total_deaths']:,}```", inline=True)
        embed.add_field(name="Total Recovered", value=f"```{covid_dict['total_recovered']:,}```", inline=True)
        embed.add_field(name="Active Cases", value=f"```{covid_dict['active_cases']:,}```", inline=True)
        embed.add_field(name="Critical Cases", value=f"```{covid_dict['critical_cases']:,}```", inline=True)
        embed.add_field(name="Cases Today", value=f"```{covid_dict['cases_today']:,}```", inline=True)
        embed.add_field(name="Deaths Today", value=f"```{covid_dict['deaths_today']:,}```", inline=True)
        embed.add_field(name="Tests", value=f"```{covid_dict['tests']:,}```", inline=True)

        embed.set_footer(text="Information provided from:  https://disease.sh/v3/covid-19/all")
        file = discord.File("./code/utils/covid.png", filename="covid.png")
        embed.set_thumbnail(url="attachment://covid.png")

        await interaction.response.send_message(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(Covid(bot))