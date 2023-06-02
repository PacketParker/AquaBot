import discord
from discord.ext import commands
import datetime
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.default_permissions(manage_messages=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(amount='Number of messages you would like deleted')
    async def purge(
        self,
        interaction: discord.Interaction,
        amount: app_commands.Range[int, 1, 100]
    ):
        "Delete the specified number of messages from the channel"
        await interaction.channel.purge(limit=amount+1)
        await interaction.response.send_message(f"{amount} {'messages' if amount > 1 else 'message'} deleted")


    @app_commands.default_permissions(kick_members=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(member='Member you would like to kick')
    @app_commands.describe(reason='Reason for kicking the member')
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):
        "Kick a member from your server"
        await member.kick(reason=reason)
        embed = discord.Embed(
            title=f"{member} Kicked",
            description=f"{interaction.user.mention} has kicked {member.mention} for `\"{reason}\"`.",
            color=discord.Color.orange()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.default_permissions(ban_members=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(member='Member you would like to ban')
    @app_commands.describe(reason='Reason for banning the member')
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):
        "Ban a member from your server"
        await member.ban(reason=reason)
        embed = discord.Embed(
            title=f"{member} Banned",
            description=f"{interaction.user.mention} has banned {member.mention} for `\"{reason}\"`.",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.default_permissions(kick_members=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(member='Member you would like to softban')
    @app_commands.describe(reason='Reason for softbanning the member')
    async def softban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):
        "Ban and then immediately unban a member"
        await member.ban(reason=reason)
        await member.unban()
        embed = discord.Embed(
            title=f"{member} Softbanned",
            description=f"{interaction.user.mention} has softbanned {member.mention} for `\"{reason}\"`.",
            color=discord.Color.orange()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))