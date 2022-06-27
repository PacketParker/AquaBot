import discord
from discord.ext import commands
from datetime import datetime
from discord import app_commands

yellow = 0xffc400
color = 0xc48aff

class slash_moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(amount='Number of messages you would like deleted')
    async def purge(
        self, 
        interaction: discord.Interaction, 
        amount: int
    ):
        "Delete the specified number of messages from the channel"

        if amount > 100:
            embed = discord.Embed(
                colour = color,
                title = "→ Amount Too Large!",
                description="• You sent an amount larger than 100. Sorry, but you can only delete 100 messages at a time."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            await interaction.channel.purge(limit=amount+1)
            await interaction.response.send_message(f"{amount} messages deleted")


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
            title = f"**User {member} has been kicked for {reason}**",
            colour = yellow
        )

        embed.add_field(name=f'This command was issued by {interaction.user}', value = f'\u200b', inline=False)
        embed.set_thumbnail(url = member.avatar.url)
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

        await interaction.response.send_message(embed=embed)


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
            title = f"**User {member} has been banned for {reason}**",
            colour = discord.Colour.red()
        )

        embed.add_field(name=f'This command was issued by {interaction.user}', value = f'\u200b', inline=False)
        embed.set_thumbnail(url = member.avatar.url)
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

        await interaction.response.send_message(embed=embed)


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
            title = f"**User {member} has been soft-banned for {reason}**",
            colour = discord.Colour.orange()
        )

        embed.add_field(name=f'This command was issued by {interaction.user}', value = f'\u200b', inline=False)
        embed.set_thumbnail(url = member.avatar.url)
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(slash_moderation(bot))