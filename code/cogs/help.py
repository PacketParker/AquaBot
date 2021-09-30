import asyncio
import os
import random
from typing import List, Tuple, Union

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
            nextcord.SelectOption(label='Gambling', description='blackjack, slots, buyc, sellc, money, leaderboard'),
            nextcord.SelectOption(label='Moderation', description='kick, ban, softban'),
            nextcord.SelectOption(label='Info', description='ping, serverinfo, wohis'),
            nextcord.SelectOption(label='Fun', description='reverse, donald'),
            nextcord.SelectOption(label='Misc', description='invite, covid, password'),
        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == 'Gambling':
            embed = nextcord.Embed(
                title = "Gambling Help",
                description = "**Hit the blackjack tables, go to the slot machines, and check your balance.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Blackjack**", value = "**Usage: `$blackjack <bet>` \nExample: `$blackjack 500` **\nIf no bet is given, the deafult bet of $250 will be placed", inline=False)
            embed.add_field(name = "**Slots**", value = "**Usage: `$slots <bet>` \nExample: `$slots 4` **\nIf no bet is given, the default bet of 1 credit will be placed.", inline=False)
            embed.add_field(name = "**Buy Credits**", value = "**Usage: `$buyc <amount>` \nExample: `$buyc 5` **\nThis command allows you to purchase credits for $250 dollars each. These credits are used at the slot machines", inline=False)
            embed.add_field(name = "**Sell Credits**", value = "**Usage: `$sellc <amount>` \nExample: `$sellc 5` **\nThis command allows you to sell your credits for $250 each in order to raise your cash balance.", inline=False)
            embed.add_field(name = "**Money**", value = "**Usage: `$money` **\nThis shows your current dollar and credit balances", inline=False)
            embed.add_field(name = "**Leaderboard**", value = "**Usage: `$leaderboard` **\nShows the top 5 players with the most money. This is a global leaderboard and not per server.", inline=False)
            await interaction.response.edit_message(embed=embed)
        if self.values[0] == 'Moderation':
            embed = nextcord.Embed(
                title = "Moderation Help",
                description = "**Keep your members in line.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Kick**", value = "**Usage: `$kick <member> <reason>` \nExample: `$kick @bob goodbye`** \nKick a member from your server. They will be able to join back with a new invite.", inline=False)
            embed.add_field(name = "**Ban**", value = "**Usage: `$slots <member> <reason>` \nExample: `$ban @bob goodbye`** \nBan a member from your server. They will not be able to join back until they are unbanned.", inline=False)
            embed.add_field(name = "**Softban**", value = "**Usage: `$softban <member>` \nExample: `$softban @bob see you soon`** \nThis command will ban and then immediately unban the member in order to get rid of their message history.", inline=False)
            await interaction.response.edit_message(embed=embed) 
        if self.values[0] == "Info":
            embed = nextcord.Embed(
                title = "Info Help",
                description = "**Get information on the bot, your server, and members within it.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Ping**", value = "**Usage: `$ping` **\nGives the current ping of the bot.", inline=False)
            embed.add_field(name = "**Serverinfo**", value = "**Usage: `$serverinfo` **\nGives lots of information on your server, inlcuding: region, boosters, roles, etc.", inline=False)
            embed.add_field(name = "**Whois**", value = "**Usage: `$whois <member>` \nExample: `$wohis @bob`** \nGives information on a member in your server. Information includes account creation date, when they joined your server, and much more.", inline=False)
            await interaction.response.edit_message(embed=embed)  
        if self.values[0] == 'Fun':
            embed = nextcord.Embed(
                title = "Fun Help",
                description = "**Have some fun.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Reverse**", value = "**Usage: `$reverse <text>` \nExample: `$reverse heres some text`** \nReverses whatever text you put in.", inline=False)
            embed.add_field(name = "**Donald**", value = "**Usage: `$donald` **\nSends a qoute from Donald Trump.", inline=False)
            await interaction.response.edit_message(embed=embed) 


        if self.values[0] == 'Misc':
            embed = nextcord.Embed(
                title = "Misc Help",
                description = "**Some uncategorized commands.**",
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