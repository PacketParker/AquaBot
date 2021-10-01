import time
import nextcord
import psutil
import os
from nextcord.ext import commands
from datetime import datetime

color = 0xc48aff

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        ping = (time.monotonic() - before) * 1000
        embed = nextcord.Embed(
            title = f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms",
            colour = nextcord.Colour.yellow()
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)

    @ping.error
    async def ping_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `$help kick` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    async def invite(self, ctx):
        embed = nextcord.Embed(
            colour = nextcord.Colour.blurple(),
            title = "Invite me to your server!",
            description = "[Click here to add](https://discord.com/api/oauth2/authorize?client_id=889027125275922462&permissions=8&scope=bot)"
        )
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = nextcord.Embed(
            color=nextcord.Colour.red(),
            title=f"→ Server Info For {guild.name}",
            description="\n— "
                        "\n➤ Shows all information about a guild."
                        "\n➤The information will be listed below!"
                        "\n —"
        )
        regions = {
            "us_west": ":flag_us: — USA West",
            "us_east": ":flag_us: — USA East",
            "us_central": ":flag_us: — USA Central",
            "us_south": ":flag_us: — USA South",
            "sydney": ":flag_au: — Sydney",
            "eu_west": ":flag_eu: — Europe West",
            "eu_east": ":flag_eu: — Europe East",
            "eu_central": ":flag_eu: — Europe Central",
            "singapore": ":flag_sg: — Singapore",
            "russia": ":flag_ru: — Russia",
            "southafrica": ":flag_za:  — South Africa",
            "japan": ":flag_jp: — Japan",
            "brazil": ":flag_br: — Brazil",
            "india": ":flag_in: — India",
            "hongkong": ":flag_hk: — Hong Kong",
        }
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
        embed.add_field(name="• Guild region: ", value=regions[guild.region.name])
        embed.add_field(name="• Guild verification: ", value=verifications[guild.verification_level.name])
        embed.add_field(name="• Member count: ", value=f"{guild.member_count}")
        embed.add_field(name="• Nitro boosters: ", value=guild.premium_subscription_count or "No Nitro Boosters!")
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @serverinfo.error
    async def serverinfo_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured when running that command, please try again later. \nIf you believe this is an error, please contact the bot developer through `$contact`"
        )  
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)



    @commands.command(aliases=['userinfo'])
    async def whois(self, ctx, member: nextcord.Member):
        embed = nextcord.Embed(
            color=nextcord.Colour.magenta(),
            title=f"→ User Information For {member}",
            description="— "
                        "\n➤ Shows all information about a user. "
                        "\n➤ The information will be listed below!"
                        "\n —"
        )

        status = {
            "online": ":status_online:",
            "idle": ":status_idle:",
            "offline": ":status_offline:",
            "dnd": ":status_dnd:"
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
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = nextcord.Embed(
                color=color,
                title="→ Invalid Member!",
                description="• Please mention a valid member! Example: `!whois @user`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(
                color=color,
                title="→ Invalid Argument!",
                description="• Please put a valid option! Example: `!whois @user`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `$help whois` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @commands.command()
    async def botinfo(self, ctx):
        embed = nextcord.Embed(
            color=nextcord.Colour.magenta(),
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



def setup(bot):
    bot.add_cog(Information(bot))