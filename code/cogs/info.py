import time
import discord
from discord.ext import commands
from datetime import datetime
from aiohttp import request

black = 0x000000
color = 0xc48aff

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def ping(self, ctx):
        "Pong! 🏓"
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(
            title = f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms",
            colour = discord.Colour.yellow()
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)

    @ping.error
    async def ping_error(self, ctx, error):
        embed = discord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed, ephemeral=True)


    @commands.command()
    async def invite(self, ctx):
        "Get the invite link for the bot and official server"
        embed = discord.Embed(
            title = "Invites",
            description = "Here's the invite for [Aqua Bot](https://discord.com/api/oauth2/authorize?client_id=889027125275922462&permissions=8&scope=bot) \nHere's the invite for the [Official Support Server](https://discord.gg/fAD3jcexzM)"
        )
        await ctx.send(embed=embed, ephemeral=True)


    @commands.command()
    async def serverinfo(self, ctx):
        "Get information related to the current server. i.e. creation date, roles, etc."
        guild = ctx.guild
        embed = discord.Embed(
            color=discord.Colour.red(),
            title=f"→ Server Info For {guild.name}",
            description="\n— "
                        "\n➤ Shows all information about a guild."
                        "\n➤The information will be listed below!"
                        "\n —"
        )

        verifications = {
            "none": "<:white_circle:625695417782239234> — No Verification",
            "low": "<:green_circle:625541294525251643> — Low Verification",
            "medium": "<:yellow_circle:625540435820937225> — Medium Verification",
            "high": "<:orange_circle:625542217100165135> — High Verification",
            "extreme": "<:red_circle:625833379258040330> — Extreme Verification"
        }
        embed.set_thumbnail(url = guild.icon.url)
        embed.add_field(name="• Guild name: ", value=str(guild.name))
        embed.add_field(name="• Guild ID: ", value=str(guild.id))
        embed.add_field(name="• Guild owner: ", value=guild.owner)
        embed.add_field(name="• Guild owner ID: ", value=guild.owner_id)
        embed.add_field(name="• Guild made in: ", value=guild.created_at.strftime("%A %d, %B %Y"))
        embed.add_field(name="• Channels count: ", value=len(guild.channels))
        embed.add_field(name="• Guild verification: ", value=verifications[guild.verification_level.name])
        embed.add_field(name="• Member count: ", value=f"{guild.member_count}")
        embed.add_field(name="• Nitro boosters: ", value=guild.premium_subscription_count or "No Nitro Boosters!")
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @serverinfo.error
    async def serverinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Required Argument!",
                description = f"• {error}"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        else:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)


    @commands.command()
    async def whois(self, 
        ctx, 
        member: discord.Member=commands.Option(description="Member whose information you want")
    ):
        "Send account information for the given user"
        if member is None:
            member = ctx.author

        embed = discord.Embed(
            color=discord.Colour.magenta(),
            title=f"→ User Information For {member}",
            description="— "
                        "\n➤ Shows all information about a user. "
                        "\n➤ The information will be listed below!"
                        "\n —"
        )

        status = {
            "online": ":green_circle: - Online",
            "idle": ":yellow_circle: - Idle",
            "offline": ":black_circle: - Offline",
            "dnd": ":red_circle: - DND"
        }

        roles = [role for role in member.roles]
        roles = f" ".join([f"`@{role}`, " for role in roles])

        embed.set_thumbnail(url = member.avatar.url)
        embed.add_field(name="• Account name: ", value=str(member))
        embed.add_field(name="• Discord ID: ", value=str(member.id))
        embed.add_field(name="• Nickname: ", value=member.nick or "No nickname!")
        embed.add_field(name="• Account created at: ", value=member.created_at.strftime("%A %d, %B %Y."))
        embed.add_field(name="• Account joined at: ", value=member.joined_at.strftime("%A %d, %B %Y"))

        if member.activity is None:
            embed.add_field(name="• Activity: ", value="No activity!")
        else:
            embed.add_field(name="• Activity: ", value=member.activity.name)
        if member.bot is True:
            embed.add_field(name="• Discord bot? ", value=":robot: = :white_check_mark:")
        else:
            embed.add_field(name="• Discord bot?", value=":robot: = :x:")
        if member.is_on_mobile() is True:
            embed.add_field(name="• On mobile? ", value=":iphone: = Yes")
        else:
            embed.add_field(name="• On mobile? ", value=":no_mobile_phones: = No")

        embed.add_field(name="• Status: ", value=status[member.status.name])
        embed.add_field(name="• Top role: ", value=f"`@{member.top_role}`")
        embed.add_field(name="• Roles: ", inline=False, value=roles)
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @whois.error
    async def whois_error(self, ctx, error, member: discord.Member=None):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                color=discord.Colour.magenta(),
                title=f"→ User Information For {member}",
                description="— "
                            "\n➤ You have too many roles, because of this we have removed that function. "
                            "\n➤ The information will be listed below!"
                            "\n —"
            )

            status = {
                "online": ":green_circle: - Online",
                "idle": ":yellow_circle: - Idle",
                "offline": ":black_circle: - Offline",
                "dnd": ":red_circle: - DND"
            }

            embed.set_thumbnail(url = member.avatar.url)
            embed.add_field(name="• Account name: ", value=str(member))
            embed.add_field(name="• Discord ID: ", value=str(member.id))
            embed.add_field(name="• Nickname: ", value=member.nick or "No nickname!")
            embed.add_field(name="• Account created at: ", value=member.created_at.strftime("%A %d, %B %Y."))
            embed.add_field(name="• Account joined at: ", value=member.joined_at.strftime("%A %d, %B %Y"))

            if member.activity is None:
                embed.add_field(name="• Activity: ", value="No activity!")
            else:
                embed.add_field(name="• Activity: ", value=member.activity.name)
            if member.bot is True:
                embed.add_field(name="• Discord bot? ", value=":robot: = :white_check_mark:")
            else:
                embed.add_field(name="• Discord bot?", value=":robot: = :x:")
            if member.is_on_mobile() is True:
                embed.add_field(name="• On mobile? ", value=":iphone: = Yes")
            else:
                embed.add_field(name="• On mobile? ", value=":no_mobile_phones: = No")

            embed.add_field(name="• Status: ", value=status[member.status.name])
            embed.add_field(name="• Top role: ", value=f"`@{member.top_role}`")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color=color,
                title="→ Invalid Member!",
                description=f"• Please mention a valid member! Example: `{ctx.prefix}whois @user`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color=color,
                title="→ Invalid Argument!",
                description=f"• Please put a valid option! Example: `{ctx.prefix}whois @user`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = discord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        else:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)


    @commands.command()
    async def botinfo(self, ctx):
        "Get information about the bot. i.e. creator, creation data, etc."
        embed = discord.Embed(
            color=discord.Colour.magenta(),
            title=f"→ Bot Information",
            description="— "
                        "\n➤ Shows information about the bot. "
                        "\n —"
        )
        before = time.monotonic()
        ping = (time.monotonic() - before) * 1000
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        embed.add_field(name="• Bot Creator: ", value="Fiji#3608"),
        embed.add_field(name="• Ping: ", value = f"{int(ping)}ms"),
        embed.add_field(name="• Account name: ", value=str(self.bot.user.name))
        embed.add_field(name="• Discord ID: ", value=str(self.bot.user.id))
        embed.add_field(name="• Bot created at: ", value=self.bot.user.created_at.strftime("%A %d, %B %Y."))
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    async def track(self, ctx):
        "Send current amount of servers the bot is in"
        guilds = len(self.bot.guilds)
        members = len(self.bot.users)
        embed = discord.Embed(
            title = "→ Here are my stats!",
            description="— "
                        "\n➤ Information below "
                        "\n —",
            colour = discord.Colour.random()
        )
        embed.add_field(name="• Amount of Servers: ", value=f"{guilds:,}", inline=False),
        embed.add_field(name="• Amount of Members: ", value=f"{members:,}", inline=False),
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    async def vote(self, ctx):
        "Get link to vote for the bot on top.gg"
        embed = discord.Embed(
            title = "→ Vote for me on top.gg!",
            description = "[Click here to vote](https://top.gg/bot/889027125275922462)",
            colour = discord.Colour.blurple()
        )
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    async def covid(self, ctx):
        "Get current global Covid-19 data"
        embed = discord.Embed(
            title = "World COVID-19 Data",
            description = "Data is updated once every 5 minutes",
            colour = 0x000000
        )

        for key in ctx.bot.covid_dict:
            embed.add_field(name = f"{key}", value = f"{ctx.bot.covid_dict[key]:,}", inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))