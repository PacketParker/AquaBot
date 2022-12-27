import discord
from discord.ext import commands, tasks
from discord import app_commands
import requests

covid_dict = {':microbe: Total cases':0, ':skull_crossbones: Total deaths':0, 
    ':syringe: Total recovered':0, ':radioactive: Total active cases':0, ':map: Total affected countries':0}

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
            countries = int(data["affectedCountries"])
        
        else:
            cases = 0
            deaths = 0
            recovered = 0
            active = 0
            countries = 0

        update_crypto_dict = {':microbe: Total cases':cases, ':skull_crossbones: Total deaths':deaths, 
        ':syringe: Total recovered':recovered, ':radioactive: Total active cases':active, 
        ':map: Total affected countries':countries}

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

        for key in covid_dict:
            embed.add_field(name = f"{key}", value = f"```{covid_dict[key]:,}```", inline=True)

        embed.set_footer(text="Information provided from:  https://disease.sh/v3/covid-19/all")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Covid(bot))