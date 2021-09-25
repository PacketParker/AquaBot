import time
import nextcord
import psutil
import os
from nextcord.ext import commands
import requests

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")


    @commands.command(aliases=["joinme", "join", "botinvite"])
    async def invite(self, ctx):
        """ Invite me to your server """
        await ctx.send(f"**{ctx.author.name}**, use this URL to invite me\n<{nextcord.utils.oauth_url(self.bot.user.id)}>")


    @commands.command(aliases=['server'])
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

        await ctx.send(embed=embed)


    @commands.command(aliases=['userinfo'])
    async def whois(self, ctx, member: nextcord.Member):
        embed = nextcord.Embed(
            color=nextcord.Colour.magenta(),
            title=f"→ Userinfo For {member}",
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

        # - TODO: See why this is returning "None" even though there is an if statement to check this
        if member.activity is None:
            embed.add_field(name="• Activity: ", value="No activity!")
        else:
            embed.add_field(name="• Activity: ", value=member.activity.name)
        if member.bot is True:
            embed.add_field(name="• Discord bot? ", value="<:bot_tag:648198074094583831> = <:tick_yes:648198008076238862>")
        else:
            embed.add_field(name="• Discord bot?", value="<:bot_tag:648198074094583831> = <:tick_no:648198035435945985>")
        if member.is_on_mobile() is True:
            embed.add_field(name="• On mobile? ", value=":iphone:")
        else:
            embed.add_field(name="• On mobile? ", value=":no_mobile_phones:")

        embed.add_field(name="• Status: ", value=status[member.status.name])
        embed.add_field(name="• Top role: ", value=f"`@{member.top_role}`")
        embed.add_field(name="• Roles: ", inline=False, value=roles)

        await ctx.send(embed=embed)


    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = nextcord.Embed(
                color=nextcord.Colour.magenta(),
                title="→ Invalid Member!",
                description="• Please mention a valid member! Example: `!whois @user`"
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(
                color=nextcord.Colour.magenta(),
                title="→ Invalid Argument!",
                description="• Please put a valid option! Example: `!whois @user`"
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))