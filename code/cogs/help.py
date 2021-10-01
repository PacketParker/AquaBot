from typing import List, Tuple, Union
from urllib.parse import quote_plus

import nextcord
from nextcord.ext import commands
from modules.card import Card
from modules.economy import Economy
from modules.helpers import *
from PIL import Image

color = 0xc48aff

class Dropdown(nextcord.ui.Select):
    def __init__(self):

        options = [
            nextcord.SelectOption(label='Gambling', description='blackjack, slots, money, leaderboard', emoji="💰"),
            nextcord.SelectOption(label='Moderation', description='kick, ban, softban', emoji="<:moderation:893273273385754686>"),
            nextcord.SelectOption(label='Info', description='ping, serverinfo, botinfo, wohis', emoji="ℹ️"),
            nextcord.SelectOption(label='Fun', description='reverse, donald', emoji='🎉'),
            nextcord.SelectOption(label='Misc', description='invite, covid, password', emoji="❓"),
        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == 'Gambling':
            embed = nextcord.Embed(
                title = "💰 - Gambling Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Blackjack**", value = "**Usage: `$blackjack <bet>`**\nIf no bet is given, the deafult bet of $250 will be placed", inline=False)
            embed.add_field(name = "**Slots**", value = "**Usage: `$slots <bet>`**\nIf no bet is given, the default bet of $250 will be placed.", inline=False)
            embed.add_field(name = "**Money**", value = "**Usage: `$money` **\nThis shows your current dollar balance", inline=False)
            embed.add_field(name = "**Leaderboard**", value = "**Usage: `$leaderboard` **\nShows the top 5 players with the most money. This is a global leaderboard and not per server.", inline=False)
            await interaction.response.edit_message(embed=embed)

        if self.values[0] == 'Moderation':
            embed = nextcord.Embed(
                title = "<:moderation:893273273385754686> - Moderation Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Kick**", value = "**Usage: `$kick <member> <reason>`** \nKick a member from your server. They will be able to join back with a new invite.", inline=False)
            embed.add_field(name = "**Ban**", value = "**Usage: `$slots <member> <reason>`** \nBan a member from your server. They will not be able to join back until they are unbanned.", inline=False)
            embed.add_field(name = "**Softban**", value = "**Usage: `$softban <member> (reason)`** \nThis command will ban and then immediately unban the member in order to get rid of their message history.", inline=False)
            await interaction.response.edit_message(embed=embed) 

        if self.values[0] == "Info":
            embed = nextcord.Embed(
                title = "ℹ️ - Info Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Ping**", value = "**Usage: `$ping` **\nGives the current ping of the bot.", inline=False)
            embed.add_field(name = "**Server Info**", value = "**Usage: `$serverinfo` **\nGives lots of information on your server, inlcuding: region, boosters, roles, etc.", inline=False)
            embed.add_field(name = "**Whois**", value = "**Usage: `$whois <member>`** \nGives information on a member in your server. Information includes account creation date, when they joined your server, and much more.", inline=False)
            embed.add_field(name = "**Bot Info**", value = "**Usage: `$botinfo`** \nGives information on the bot.", inline=False)
            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == 'Fun':
            embed = nextcord.Embed(
                title = "🎉 - Fun Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Reverse**", value = "**Usage: `$reverse <text>`** \nReverses whatever text you put in.", inline=False)
            embed.add_field(name = "**Donald**", value = "**Usage: `$donald` **\nSends a qoute from Donald Trump.", inline=False)
            await interaction.response.edit_message(embed=embed) 

        if self.values[0] == 'Misc':
            embed = nextcord.Embed(
                title = "❓ - Misc Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Covid**", value = "**Usage: `$covid` **\nSends the current global COVID-19 data.", inline=False)
            embed.add_field(name = "**Password**", value = "**Usage: `$password` **\nWill DM you a password for you to use on sites. These passwords are never stored and are entirely random.", inline=False)
            embed.add_field(name = "**Invite**", value = "**Usage: `$invite` **\nSends the invite link for the bot.", inline=False)
            await interaction.response.edit_message(embed=embed) 
        else:
            await interaction.response.send_message("Hmmm... something is broken. Please contact the bot developer with `$contact`")

class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.add_item(Dropdown())
        url = "https://discord.com/api/oauth2/authorize?client_id=889027125275922462&permissions=8&scope=bot"
        self.add_item(nextcord.ui.Button(label="Invite Me", url=url, row=3))
        url = "https://pkmeiner.com"
        self.add_item(nextcord.ui.Button(label="Bot Site", url=url, row=3))

    @nextcord.ui.button(label='Main Page', style=nextcord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Help",
            description = "For extended information on commands and categories, please choose and option from the dropdown menu below.",
            colour = nextcord.Colour.random()   
        )

        await interaction.response.edit_message(embed=embed)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, row=2)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = nextcord.Embed(
            title = "Help",
            description = "For extended information on commands and categories, please choose and option from the dropdown menu below.",
            colour = nextcord.Colour.random()    
        )

        view = DropdownView()
        await ctx.send(embed=embed, view=view)


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))