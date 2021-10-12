from typing import List, Optional
from urllib.parse import quote_plus

import nextcord
from nextcord.ext import commands
from modules.card import Card
from modules.economy import Economy
from modules.helpers import *
from PIL import Image

color = 0xc48aff

class HelpDropdown(nextcord.ui.Select):
    def __init__(self):

        options = [
            nextcord.SelectOption(label='Gambling', description='blackjack, slots, coinflip, money, leaderboard', emoji="💰"),
            nextcord.SelectOption(label='Moderation', description='kick, ban, softban, purge', emoji="<:moderation:893273273385754686>"),
            nextcord.SelectOption(label='Info', description='contact, covid, invite, track, ping, serverinfo, whois, botinfo, vote', emoji="ℹ️"),
            nextcord.SelectOption(label='Music (BETA)', description='play, skip, queue, remove, stop, clear, repeat, shuffle, nowplaying, pause, remove', emoji='🎵'),
            nextcord.SelectOption(label='Fun', description='reverse, donald', emoji='🎉'),
        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == 'Gambling':
            embed = nextcord.Embed(
                title = "💰 - Gambling Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**🃏 - Blackjack (bj)**", value = "**Usage: `$blackjack <bet>`**\nIf no bet is given, the deafult bet of $125 will be placed", inline=False)
            embed.add_field(name = "**🎰 - Slots**", value = "**Usage: `$slots <bet>`**\nIf no bet is given, the default bet of $125 will be placed.", inline=False)
            embed.add_field(name = "**🪙 - Coinflip (cf)**", value = "**Usage: `$coinflip <bet>`**\nHeads means you win, tails means you lose. If no bet is given, the default bet of $125 will be placed.", inline=False)
            embed.add_field(name = "**💵 - Money**", value = "**Usage: `$money` **\nThis shows your current dollar balance", inline=False)
            embed.add_field(name = "**🏅 - Leaderboard**", value = "**Usage: `$leaderboard` **\nShows the top 5 players with the most money. This is a global leaderboard and not per server.", inline=False)
            await interaction.response.edit_message(embed=embed)

        if self.values[0] == 'Moderation':
            embed = nextcord.Embed(
                title = "<:moderation:893273273385754686> - Moderation Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )
      
            embed.add_field(name = "**Purge**", value = "**Usage: `$purge <amount>`** \nDelete messages from your server. Max amount that can be deleted at one time is `100` messages.")
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

            embed.add_field(name = "**Contact**", value = "**Usage: `$contact`** \nWill DM you and help you get in contact with staff members to resolve your issue, bug.", inline=True)
            embed.add_field(name = "**Covid**", value = "**Usage: `$covid` **\nSends the current global COVID-19 data.", inline=True)
            embed.add_field(name = "**Invite**", value = "**Usage: `$invite` **\nSends the invite for the bot.", inline=True)
            embed.add_field(name = "**Track**", value = "**Usage: `track`** \nSends the amount of servers that the bot is in, as well as the cumulative amount of members.", inline=True)
            embed.add_field(name = "**Ping**", value = "**Usage: `$ping` **\nGives the current ping of the bot.", inline=True)
            embed.add_field(name = "**Server Info**", value = "**Usage: `$serverinfo` **\nGives lots of information on your server, inlcuding: region, boosters, roles, etc.", inline=True)
            embed.add_field(name = "**Whois**", value = "**Usage: `$whois <member>`** \nGives information on a member in your server. Information includes account creation date, when they joined your server, and much more.", inline=True)
            embed.add_field(name = "**Bot Info**", value = "**Usage: `$botinfo`** \nGives information on the bot.", inline=True)
            embed.add_field(name = "**Vote**", value = "**Usage: `$vote`** \nSends the link for you to vote for our bot on top.gg", inline=True)
            await interaction.response.edit_message(embed=embed)  


        if self.values[0] == "Music (BETA)":
            embed = nextcord.Embed(
                title = "🎵 - Music Help \n*NOTE - These commands are still in beta. Please report bugs using `$contact`",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Play**", value = "**Usage: `$play <name of song / URL>` **\nSearches YouTube, and then plays the top song.", inline=True)
            embed.add_field(name = "**Skip**", value = "**Usage: `$skip` **\nSkips the song that is currently playing.", inline=True)
            embed.add_field(name = "**Queue**", value = "**Usage: `$queue`** \nSends all of the songs that are in the queue.", inline=True)
            embed.add_field(name = "**Remove**", value = "**Usage: `$remove <song #>` **\nRemoves the specified song from the queue.", inline=True)
            embed.add_field(name = "**Stop**", value = "**Usage: `$stop`** \nStops music, clears queue, and leaves VC.", inline=True),            embed.add_field(name = "**Clear**", value = "**Usage: `$clear` **\nRemoves ALL songs in the queue.", inline=True)
            embed.add_field(name = "**Repeat**", value = "**Usage: `$remove`** \nRepeats the song that is playing. Run the command again to stop repeating.", inline=True)
            embed.add_field(name = "**Shuffle**", value = "**Usage: `$shuffle`** \nWill play a random song in the queue. Run the command again to stop shuffling.", inline=True)
            embed.add_field(name = "**Nowplaying**", value = "**Usage: `$nowplaying` **\nSends the song that is currently playing.", inline=True)
            embed.add_field(name = "**Pause**", value = "**Usage: `$pause`** \nPauses the currently playing song.", inline=True)
            embed.add_field(name = "**Resume**", value = "**Usage: `$resume` **\nResumes the paused song.", inline=True)

            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == 'Fun':
            embed = nextcord.Embed(
                title = "🎉 - Fun Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Reverse**", value = "**Usage: `$reverse <text>`** \nReverses whatever text you put in.", inline=False)
            embed.add_field(name = "**Donald**", value = "**Usage: `$donald` **\nSends a quote from Donald Trump.", inline=False)
            embed.add_field(name = "**Kanye**", value = "**Usage: `$kanye` **\nSends a quote from Kanye West.", inline=False)
            await interaction.response.edit_message(embed=embed) 

        else:
            return

class HelpView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.add_item(HelpDropdown())
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


class GuildHelpDropdown(nextcord.ui.Select):
    def __init__(self):

        options = [
            nextcord.SelectOption(label='Gambling', description='blackjack, slots, coinflip, money, leaderboard', emoji="💰"),
            nextcord.SelectOption(label='Moderation', description='kick, ban, softban, mute, unmute, lock, unlock, purge', emoji="<:moderation:893273273385754686>"),
            nextcord.SelectOption(label='Info', description='contact, covid, invite, track, ping, serverinfo, whois, botinfo, vote', emoji="ℹ️"),
            nextcord.SelectOption(label='Music (BETA)', description='play, skip, queue, remove, stop, clear, repeat, shuffle, nowplaying, pause, remove', emoji='🎵'),
            nextcord.SelectOption(label='Fun', description='reverse, donald', emoji='🎉'),
        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == 'Gambling':
            embed = nextcord.Embed(
                title = "💰 - Gambling Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**🃏 - Blackjack (bj)**", value = "**Usage: `$blackjack <bet>`**\nIf no bet is given, the deafult bet of $125 will be placed", inline=False)
            embed.add_field(name = "**🎰 - Slots**", value = "**Usage: `$slots <bet>`**\nHeads means you win, tails means you lose. If no bet is given, the default bet of $125 will be placed.", inline=False)
            embed.add_field(name = "**🪙 - Coinflip (cf)**", value = "**Usage: `$coinflip <bet>`**\nIf no bet is given, the default bet of $125 will be placed.", inline=False)
            embed.add_field(name = "**💵 - Money**", value = "**Usage: `$money` **\nThis shows your current dollar balance", inline=False)
            embed.add_field(name = "**🏅 - Leaderboard**", value = "**Usage: `$leaderboard` **\nShows the top 5 players with the most money. This is a global leaderboard and not per server.", inline=False)
            await interaction.response.edit_message(embed=embed)

        if self.values[0] == 'Moderation':
            embed = nextcord.Embed(
                title = "<:moderation:893273273385754686> - Moderation Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Mute**", value = "**Usage: `$mute <member> <time>` \nExample: `$mute @bob 2d 4h 6m 8s`** \nMute a member so they can't send anymore messages for a specified amount of time.", inline=True)
            embed.add_field(name = "**Unmute**", value = "**Usage: `$unmute <member>`** \nUnmute a member so they are able to send messages again.", inline=True)      
            embed.add_field(name = "**Purge**", value = "**Usage: `$purge <amount>`** \nDelete messages from your server. Max amount that can be deleted at one time is `100` messages.", inline=True)
            embed.add_field(name = "**Kick**", value = "**Usage: `$kick <member> <reason>`** \nKick a member from your server. They will be able to join back with a new invite.", inline=True)
            embed.add_field(name = "**Ban**", value = "**Usage: `$slots <member> <reason>`** \nBan a member from your server. They will not be able to join back until they are unbanned.", inline=True)
            embed.add_field(name = "**Softban**", value = "**Usage: `$softban <member> (reason)`** \nThis command will ban and then immediately unban the member in order to get rid of their message history.", inline=True)
            embed.add_field(name = "**Lock**", value = "**Usage: `$lock (reason)`** \nThis will lock the channel where the command was sent.", inline=True)
            embed.add_field(name = "**Unlock**", value = "**Usage: `$unlock (reason)`** \nThis will unlock the channel where the command was sent.", inline=True)
            
            await interaction.response.edit_message(embed=embed) 

        if self.values[0] == "Info":
            embed = nextcord.Embed(
                title = "ℹ️ - Info Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Contact**", value = "**Usage: `$contact`** \nWill DM you and help you get in contact with staff members to resolve your issue, bug.", inline=True)
            embed.add_field(name = "**Covid**", value = "**Usage: `$covid` **\nSends the current global COVID-19 data.", inline=True)
            embed.add_field(name = "**Invite**", value = "**Usage: `$invite` **\nSends the invite for the bot.", inline=True)
            embed.add_field(name = "**Track**", value = "**Usage: `track`** \nSends the amount of servers that the bot is in, as well as the cumulative amount of members.", inline=True)
            embed.add_field(name = "**Ping**", value = "**Usage: `$ping` **\nGives the current ping of the bot.", inline=True)
            embed.add_field(name = "**Server Info**", value = "**Usage: `$serverinfo` **\nGives lots of information on your server, inlcuding: region, boosters, roles, etc.", inline=True)
            embed.add_field(name = "**Whois**", value = "**Usage: `$whois <member>`** \nGives information on a member in your server. Information includes account creation date, when they joined your server, and much more.", inline=True)
            embed.add_field(name = "**Bot Info**", value = "**Usage: `$botinfo`** \nGives information on the bot.", inline=True)
            embed.add_field(name = "**Vote**", value = "**Usage: `$vote`** \nSends the link for you to vote for our bot on top.gg", inline=True)
            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == "Music (BETA)":
            embed = nextcord.Embed(
                title = "🎵 - Music Help \n*NOTE - These commands are still in beta. Please report bugs using `$contact`",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Play**", value = "**Usage: `$play <name of song / URL>` **\nSearches YouTube, and then plays the top song.", inline=True)
            embed.add_field(name = "**Skip**", value = "**Usage: `$skip` **\nSkips the song that is currently playing.", inline=True)
            embed.add_field(name = "**Queue**", value = "**Usage: `$queue`** \nSends all of the songs that are in the queue.", inline=True)
            embed.add_field(name = "**Remove**", value = "**Usage: `$remove <song #>` **\nRemoves the specified song from the queue.", inline=True)
            embed.add_field(name = "**Stop**", value = "**Usage: `$stop`** \nStops music, clears queue, and leaves VC.", inline=True),            embed.add_field(name = "**Clear**", value = "**Usage: `$clear` **\nRemoves ALL songs in the queue.", inline=True)
            embed.add_field(name = "**Repeat**", value = "**Usage: `$remove`** \nRepeats the song that is playing. Run the command again to stop repeating.", inline=True)
            embed.add_field(name = "**Shuffle**", value = "**Usage: `$shuffle`** \nWill play a random song in the queue. Run the command again to stop shuffling.", inline=True)
            embed.add_field(name = "**Nowplaying**", value = "**Usage: `$nowplaying` **\nSends the song that is currently playing.", inline=True)
            embed.add_field(name = "**Pause**", value = "**Usage: `$pause`** \nPauses the currently playing song.", inline=True)
            embed.add_field(name = "**Resume**", value = "**Usage: `$resume` **\nResumes the paused song.", inline=True)

            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == 'Fun':
            embed = nextcord.Embed(
                title = "🎉 - Fun Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = nextcord.Colour.random()
            )

            embed.add_field(name = "**Reverse**", value = "**Usage: `$reverse <text>`** \nReverses whatever text you put in.", inline=False)
            embed.add_field(name = "**Donald**", value = "**Usage: `$donald` **\nSends a quote from Donald Trump.", inline=False)
            embed.add_field(name = "**Kanye**", value = "**Usage: `$kanye` **\nSends a quote from Kanye West.", inline=False)
            await interaction.response.edit_message(embed=embed) 

        else:
            return

class GuildHelpView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.add_item(GuildHelpDropdown())
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
        if ctx.message.guild.id != 889027208964874240:
            embed = nextcord.Embed(
                title = "Help",
                description = "For extended information on commands and categories, please choose and option from the dropdown menu below.",
                colour = nextcord.Colour.random()    
            )

            view = HelpView()
            await ctx.send(embed=embed, view=view)

        if ctx.message.guild.id == 889027208964874240:
            embed = nextcord.Embed(
                title = "Help",
                description = "For extended information on commands and categories, please choose and option from the dropdown menu below.",
                colour = nextcord.Colour.random()    
            )

            view = GuildHelpView()
            await ctx.send(embed=embed, view=view)


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))