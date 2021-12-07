import discord
from discord.ext import commands
from utils.helpers import *
import re

color = 0xc48aff

class HelpDropdown(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Economy', description='add, profile, shop, blackjack, slots, coinflip, money, leaderboard', emoji="💰"),
            discord.SelectOption(label='Moderation', description='mute, tempmute, unmute, kick, ban, softban, purge', emoji="<:moderation:893273273385754686>"),
            discord.SelectOption(label='Info', description='contact, prices, crypto, covid, invite, track, serverinfo, whois, botinfo, vote', emoji="ℹ️"),
            discord.SelectOption(label='Music (BETA)', description='play, skip, queue, remove, stop, clear, repeat, shuffle, nowplaying, pause, remove', emoji='🎵'),
            discord.SelectOption(label='Admin', description='setprefix, setlevel, lvlreset, dellevel, lvlchannel, setmute, muterole, delmute, setjoin', emoji="⚙️"),
            discord.SelectOption(label='Fun', description='level, lvlboard, ping, new', emoji='🎉'),
        ]

        super().__init__(placeholder='Choose a category...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'Economy':
            embed = discord.Embed(
                title = "💰 - Economy Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = discord.Colour.random()
            )

            embed.add_field(name = "**Add**", value = f"**Usage: `{self.view.ctx.clean_prefix}add`**\nGives you $2,500. Can be run every 2 hours", inline=False)
            embed.add_field(name = "**Profile**", value = f"**Usage: `{self.view.ctx.clean_prefix}profile <member>`**\nShows the amount of money and ranks that a user has", inline=False)
            embed.add_field(name = "**Shop**", value = f"**Usage: `{self.view.ctx.clean_prefix}shop`**\nGives you the shop menus so that you can buy items", inline=False)
            embed.add_field(name = "**🃏 - Blackjack**", value = f"**Usage: `{self.view.ctx.clean_prefix}blackjack <bet>`**\nIf no bet is given, the deafult bet of $125 will be placed", inline=False)
            embed.add_field(name = "**🎰 - Slots**", value = f"**Usage: `{self.view.ctx.clean_prefix}slots <bet>`**\nIf no bet is given, the default bet of $125 will be placed.", inline=False)
            embed.add_field(name = "**🪙 - Coinflip**", value = f"**Usage: `{self.view.ctx.clean_prefix}coinflip <bet>`**\nHeads means you win, tails means you lose. If no bet is given, the default bet of $125 will be placed.", inline=False)
            embed.add_field(name = "**💵 - Money**", value = f"**Usage: `{self.view.ctx.clean_prefix}money` **\nThis shows your current dollar balance", inline=False)
            embed.add_field(name = "**🏅 - Leaderboard**", value = f"**Usage: `{self.view.ctx.clean_prefix}leaderboard` **\nShows the top 5 players with the most money. This is a global leaderboard and not per server.", inline=False)
            await interaction.response.edit_message(embed=embed)

        if self.values[0] == 'Moderation':
            embed = discord.Embed(
                title = "<:moderation:893273273385754686> - Moderation Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = discord.Colour.random()
            )
            embed.add_field(name = "**Warn**", value = f"**Usage: `{self.view.ctx.clean_prefix}warn <member> <reason>`** \nWarn a member for doing something against the rules.", inline=True)
            embed.add_field(name = "**Delwarn**", value = f"**Usage: `{self.view.ctx.clean_prefix}delwarn <warn ID>`** \nDelete a warning from a member so that it is no longer on their record.", inline=True)
            embed.add_field(name = "**Warnings**", value = f"**Usage: `{self.view.ctx.clean_prefix}warnings <member>`** \nSee all of the warnings for a member. Also includes when they were warned, and who warned them.", inline=True)
            embed.add_field(name = "**Mute**", value = f"**Usage: `{self.view.ctx.clean_prefix}mute <member> <time>`** \nMute a member so they can't send anymore messages.", inline=True)
            embed.add_field(name = "**Tempmute**", value = f"**Usage: `{self.view.ctx.clean_prefix}tempmute <member> <time>` \nExample: `{self.view.ctx.clean_prefix}tempmute @bob 2d 4h 6m 8s`** \nMutes the member temporarily, they will be unmute once the specified time has passed.", inline=True)
            embed.add_field(name = "**Unmute**", value = f"**Usage: `{self.view.ctx.clean_prefix}unmute <member>`** \nUnmute a member so they are able to send messages again.", inline=True)      
            embed.add_field(name = "**Purge**", value = f"**Usage: `{self.view.ctx.clean_prefix}purge <amount>`** \nDelete messages from your server. Max amount that can be deleted at one time is `100` messages.")
            embed.add_field(name = "**Kick**", value = f"**Usage: `{self.view.ctx.clean_prefix}kick <member> <reason>`** \nKick a member from your server. They will be able to join back with a new invite.", inline=True)
            embed.add_field(name = "**Ban**", value = f"**Usage: `{self.view.ctx.clean_prefix}slots <member> <reason>`** \nBan a member from your server. They will not be able to join back until they are unbanned.", inline=True)
            embed.add_field(name = "**Softban**", value = f"**Usage: `{self.view.ctx.clean_prefix}softban <member> (reason)`** \nThis command will ban and then immediately unban the member in order to get rid of their message history.", inline=True)
            await interaction.response.edit_message(embed=embed) 

        if self.values[0] == "Info":
            embed = discord.Embed(
                title = "ℹ️ - Info Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = discord.Colour.random()
            )

            embed.add_field(name = "**Contact**", value = f"**Usage: `{self.view.ctx.clean_prefix}contact`** \nWill DM you and help you get in contact with staff members to resolve your issue, bug.", inline=True)
            embed.add_field(name = "**Prices**", value = f"**Usage: `{self.view.ctx.clean_prefix}prices`** \nShows the prices for the 20 cryptocurrencies that we currently list", inline=True)
            embed.add_field(name = "**Crypto**", value = f"**Usage: `{self.view.ctx.clean_prefix}crypto <ticker>`** \nShows expanded information on the specific currency given its ticker.", inline=True)
            embed.add_field(name = "**Covid**", value = f"**Usage: `{self.view.ctx.clean_prefix}covid` **\nSends the current global COVID-19 data.", inline=True)
            embed.add_field(name = "**Invite**", value = f"**Usage: `{self.view.ctx.clean_prefix}invite` **\nSends the invite for the bot and the official support server.", inline=True)
            embed.add_field(name = "**Track**", value = f"**Usage: `{self.view.ctx.clean_prefix}track`** \nSends the amount of servers that the bot is in, as well as the cumulative amount of members.", inline=True)
            embed.add_field(name = "**Server Info**", value = f"**Usage: `{self.view.ctx.clean_prefix}serverinfo` **\nGives lots of information on your server, inlcuding: region, boosters, roles, etc.", inline=True)
            embed.add_field(name = "**Whois**", value = f"**Usage: `{self.view.ctx.clean_prefix}whois <member>`** \nGives information on a member in your server. Information includes account creation date, when they joined your server, and much more.", inline=True)
            embed.add_field(name = "**Bot Info**", value = f"**Usage: `{self.view.ctx.clean_prefix}botinfo`** \nGives information on the bot.", inline=True)
            embed.add_field(name = "**Vote**", value = f"**Usage: `{self.view.ctx.clean_prefix}vote`** \nSends the link for you to vote for our bot on top.gg", inline=True)
            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == "Music (BETA)":
            embed = discord.Embed(
                title = f"🎵 - Music Help \n*NOTE - These commands are still in beta. Please report bugs using `{self.view.ctx.clean_prefix}contact`",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = discord.Colour.random()
            )

            embed.add_field(name = "**Play**", value = f"**Usage: `{self.view.ctx.clean_prefix}play <name of song / URL>` **\nSearches YouTube, and then plays the top song.", inline=True)
            embed.add_field(name = "**Skip**", value = f"**Usage: `{self.view.ctx.clean_prefix}skip` **\nSkips the song that is currently playing.", inline=True)
            embed.add_field(name = "**Queue**", value = f"**Usage: `{self.view.ctx.clean_prefix}queue`** \nSends all of the songs that are in the queue.", inline=True)
            embed.add_field(name = "**Remove**", value = f"**Usage: `{self.view.ctx.clean_prefix}remove <song #>` **\nRemoves the specified song from the queue.", inline=True)
            embed.add_field(name = "**Stop**", value = f"**Usage: `{self.view.ctx.clean_prefix}stop`** \nStops music, clears queue, and leaves VC.", inline=True),            
            embed.add_field(name = "**Clear**", value = f"**Usage: `{self.view.ctx.clean_prefix}clear` **\nRemoves ALL songs in the queue.", inline=True)
            embed.add_field(name = "**Repeat**", value = f"**Usage: `{self.view.ctx.clean_prefix}remove`** \nRepeats the song that is playing. Run the command again to stop repeating.", inline=True)
            embed.add_field(name = "**Shuffle**", value = f"**Usage: `{self.view.ctx.clean_prefix}shuffle`** \nWill play a random song in the queue. Run the command again to stop shuffling.", inline=True)
            embed.add_field(name = "**Np**", value = f"**Usage: `{self.view.ctx.clean_prefix}np` **\nSends the song that is currently playing.", inline=True)
            embed.add_field(name = "**Pause**", value = f"**Usage: `{self.view.ctx.clean_prefix}pause`** \nPauses the currently playing song.", inline=True)
            embed.add_field(name = "**Resume**", value = f"**Usage: `{self.view.ctx.clean_prefix}resume` **\nResumes the paused song.", inline=True)

            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == "Admin":
            embed = discord.Embed(
                title = "⚙️ - Admin Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = discord.Colour.random()
            )

            embed.add_field(name = "**Setprefix**", value = f"**Usage: `{self.view.ctx.clean_prefix}setprefix <new prefix>` **\nSets the prefix for the bot in your specific server.", inline=True)
            embed.add_field(name = "**Setlevel**", value = f"**Usage: `{self.view.ctx.clean_prefix}setlevel <name of channel>` **\nSets the channel for level up messages to be sent to.", inline=True)
            embed.add_field(name = "**Lvlreset**", value = f"**Usage: `{self.view.ctx.clean_prefix}lvlreset` **\nResets all of the levels for everyone in the server.", inline=True)
            embed.add_field(name = "**Dellevel**", value = f"**Usage: `{self.view.ctx.clean_prefix}dellevel` **\nDeletes the channel from our database, and stops sending new level up messages.", inline=True)
            embed.add_field(name = "**Lvlchannel**", value = f"**Usage: `{self.view.ctx.clean_prefix}lvlchannel` ** \nShows the current channel for leveling messages.", inline=True)
            embed.add_field(name = "**Setmute**", value = f"**Usage: `{self.view.ctx.clean_prefix}setmute <name of role>` **\nSets the role that will be given to users whenever you use the `{self.view.ctx.clean_prefix}mute` command.", inline=True)
            embed.add_field(name = "**Delmute**", value = f"**Usage: `{self.view.ctx.clean_prefix}delmute` **\nDeletes the muted role from our database.", inline=True)
            embed.add_field(name = "**Muterole**", value = f"**Usage: `{self.view.ctx.clean_prefix}muterole`** \nSends the current role that is assigned as the muted role for your server.", inline=True)
            embed.add_field(name = "**Setjoin**", value = f"**Usage: `{self.view.ctx.clean_prefix}setjoin <name of channel>` **\nSets the channel for messages to be sent whenever a new user joins your server.", inline=True)
            embed.add_field(name = "**Deljoin**", value = f"**Usage: `{self.view.ctx.clean_prefix}deljoin`** \nDeletes the channel from our database, and stops sending new user messages.", inline=True),
            embed.add_field(name = "**Joinchannel**", value = f"**Usage: `{self.view.ctx.clean_prefix}joinchannel`** \nSends the current channel that is assigned as the new user messages channel.", inline=True)

            await interaction.response.edit_message(embed=embed)  

        if self.values[0] == 'Fun':
            embed = discord.Embed(
                title = "🎉 - Fun Help",
                description = "**Options in `<>` are mandatory, and those in `()` are optional.**",
                colour = discord.Colour.random()
            )

            embed.add_field(name = "**Level**", value = f"**Usage: `{self.view.ctx.clean_prefix}level`** \nSends your current level in the server.", inline=False)
            embed.add_field(name = "**Lvlboard**", value = f"**Usage: `{self.view.ctx.clean_prefix}lvlboard`** \nSends the current leaderboard for your servers leveling system.", inline=False)
            embed.add_field(name = "**Ping**", value = f"**Usage: `{self.view.ctx.clean_prefix}ping` **\nGives the current ping of the bot.", inline=True)
            embed.add_field(name = "**New**", value = f"**Usage: `{self.view.ctx.clean_prefix}new`** \nSends all of the changes to the bot.", inline=False)
            await interaction.response.edit_message(embed=embed) 

        else:
            return

class HelpView(discord.ui.View):
    def __init__(self, ctx, *, timeout = 180.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.value = None
        self.add_item(HelpDropdown())
        url = "https://discord.com/api/oauth2/authorize?client_id=889027125275922462&permissions=8&scope=bot"
        self.add_item(discord.ui.Button(label="Invite Me", url=url, row=3))
        url = "https://pkmeiner.com"
        self.add_item(discord.ui.Button(label="Bot Site", url=url, row=3))

    @discord.ui.button(label='Main Page', style=discord.ButtonStyle.blurple, row=2)
    async def main_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
            title = "Help",
            description = f"**IMPORTANT - A lot of stuff changed, please use the `new` command to see all of the changes** \n\nFor extended information on commands and categories, please choose an option from the dropdown menu below.",
            colour = discord.Colour.random()    
        )

        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label='Delete', style=discord.ButtonStyle.red, row=2)
    async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()



class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        "Sends the bots commands and features"
        embed = discord.Embed(
            title = "Help",
            description = f"**IMPORTANT - A lot of stuff changed, please use the `new` command to see all of the changes** \n\nFor extended information on commands and categories, please choose an option from the dropdown menu below.",
            colour = discord.Colour.random()    
        )

        view = HelpView(ctx)
        await ctx.send(embed=embed, view=view)


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if re.fullmatch(rf"<@!?{self.bot.user.id}>", message.content):
            ctx = await self.bot.get_context(message)
            prefix = await self.bot.get_prefix(message)
            embed = discord.Embed(
                title = f"Prefix - {prefix}",
                description = f"**Use the prefix above to run commands, or use `{prefix}help` in order to get help on what commands are available.**",
                colour = discord.Colour.blurple()    
            )
            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))