import discord
from discord.ext import commands
import datetime
from discord import app_commands
from bot import CONNECTION
from reader import BOT_COLOR

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.default_permissions(manage_messages=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(member='The member you would like to warn')
    @app_commands.describe(reason='Reason for warning the member')
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):
        "Warn a member for a given reason"
        guild_id = interaction.user.guild.id
        user_id = member.id
        warn_id = interaction.id
        warn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        warned_by = interaction.user.id

        cur = CONNECTION.cursor()
        cur.execute("INSERT INTO warnings (warn_id, guild_id, user_id, warning, warn_time, warned_by) VALUES (%s, %s, %s, %s, %s, %s)", (warn_id, guild_id, user_id, reason, warn_time, warned_by))
        CONNECTION.commit()

        embed = discord.Embed(
            title = f"`{member.name}#{member.discriminator}` Has Been Warned in {interaction.guild}",
            description=f"Reason: {reason}",
            color = discord.Colour.orange()
        )
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.default_permissions(manage_messages=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(member='The member whose warnings you want to see')
    async def warnings(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        "Show all warnings for a given user"
        guild_id = interaction.user.guild.id
        user_id = member.id

        cur = CONNECTION.cursor()
        cur.execute("SELECT * FROM warnings WHERE guild_id = %s AND user_id = %s", (guild_id, user_id))
        data = cur.fetchall()

        if data:
            embed=discord.Embed(
                title=f"Warnings for `{member.name}#{member.discriminator}` in {interaction.guild}",
                description="",
                color=discord.Color.orange()
            )
            for entry in data:
                embed.description += f"**Reason - `\"{entry[3]}\"` | ID: `{entry[0]}`**\nWarned By: <@{entry[5]}> | Date: {entry[4]}\n\n"

            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed)

        else:
            embed = discord.Embed(
                title="No Warnings",
                description=f"{member.mention} has not been warned in the past, or all of their warnings have been deleted.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed)


    @app_commands.default_permissions(manage_messages=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(id='ID of the warning you would like to delete')
    async def delwarn(
        self,
        interaction: discord.Interaction,
        id: str
    ):
        "Delete a warning from a user with the warning ID"
        cur = CONNECTION.cursor()
        cur.execute("SELECT warn_id FROM warnings WHERE warn_id = %s", (id,))
        data = cur.fetchone()

        if data:
            cur.execute("DELETE FROM warnings WHERE warn_id = %s", (id,))
            CONNECTION.commit()

            embed = discord.Embed(
                title="Warning Deleted",
                description=f"{interaction.user.mention} has deleted the warning identified by `{id}` .",
                color=discord.Color.orange()
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed)

        else:
            embed = discord.Embed(
                title="Invalid ID",
                description="That ID is not associated with any warnings in this server.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Warnings(bot))