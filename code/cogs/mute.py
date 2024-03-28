import discord
from discord.ext import commands, tasks
import datetime
from discord import app_commands

from global_variables import CONNECTION, BOT_COLOR


class Mute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_load(self):
        self.mute_check.start()

    @tasks.loop(seconds=60)
    async def mute_check(self):
        cur = CONNECTION.cursor()
        cur.execute("SELECT * FROM tempmute WHERE time < %s", (datetime.datetime.now(),))
        data = cur.fetchall()
        for row in data:
            try:
                guild_id = row[0]
                user_id = row[1]
                role_id = row[2]
                guild = await self.bot.fetch_guild(guild_id)
                user = await guild.fetch_member(user_id)
                role = guild.get_role(role_id)
                await user.remove_roles(role)
                cur.execute("DELETE FROM tempmute WHERE guild_id = %s AND user_id = %s", (guild_id, user_id))
                CONNECTION.commit()
            except:
                pass


    @app_commands.default_permissions(manage_roles=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(role_name='Name of your servers muted role')
    async def setmute(
        self,
        interaction: discord.Interaction,
        role_name: discord.Role
    ):
        "Set the role for users to be given when muted"
        guild_id = interaction.user.guild.id
        role = role_name
        role_id = role.id

        cur = CONNECTION.cursor()
        cur.execute("SELECT role_id FROM mute WHERE guild_id = %s", (guild_id,))
        role_id = cur.fetchone()
        if role_id != None:
            cur.execute("UPDATE mute SET role_id = %s WHERE guild_id = %s", (role.id, guild_id))
            CONNECTION.commit()

        else:
            cur.execute("INSERT INTO mute (role_id, guild_id) VALUES(%s, %s)", (role.id, guild_id))
            CONNECTION.commit()

        embed = discord.Embed(
            title = "Mute Role Set",
            description = f"The mute role for {interaction.guild.name} has been set to: <@&{role.id}>",
            color=BOT_COLOR
        )
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.default_permissions(manage_roles=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def delmute(
        self,
        interaction: discord.Interaction
    ):
        "Delete the role set to be given to muted users"
        guild_id = interaction.user.guild.id
        cur = CONNECTION.cursor()
        cur.execute("SELECT role_id FROM mute WHERE guild_id = %s", (guild_id,))
        data = cur.fetchone()
        if data:
            cur.execute("DELETE FROM mute WHERE guild_id = %s", (guild_id,))
            CONNECTION.commit()

            embed = discord.Embed(
                title = "Mute Role Deleted",
                description = f"The mute role for {interaction.user.guild.name} has been deleted from my database.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed)

        else:
            embed = discord.Embed(
                title = "Mute Role Not Set",
                description = f"The mute role is not set, therefore there is no role I can delete.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.default_permissions(manage_roles=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def muterole(
        self,
        interaction: discord.Interaction
    ):
        "See the current role set for when users are muted"
        guild_id = interaction.user.guild.id
        cur = CONNECTION.cursor()
        cur.execute("SELECT role_id FROM mute WHERE guild_id = %s", (guild_id,))
        data = cur.fetchone()
        if data:
            role = interaction.guild.get_role(data[0])
            if role:
                embed = discord.Embed(
                    title=f"Mute Role for {interaction.user.guild.name}",
                    description=f"The role given to members who are muted in this server is: <@&{role.id}>",
                    color=BOT_COLOR
                )
                embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
                return await interaction.response.send_message(embed=embed)

            else:
                embed = discord.Embed(
                    title="Mute Role Not Found",
                    description=f"You have previously set a mute role, but it seems that the role you set has since been deleted. Please add a new mute role with the `/setmute` command.",
                    color=BOT_COLOR
                )
                embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
                return await interaction.response.send_message(embed=embed)

        else:
            embed = discord.Embed(
                title = "No Role Set",
                description = f"It seems you haven't set a muted role yet. Please go do that with `/setmute` before running this command.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.default_permissions(manage_roles=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(member='Name of the member you want to temporarily mute')
    @app_commands.describe(time='Amount of time (in hours) to mute the member')
    async def tempmute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        time: app_commands.Range[int, 1, None]
    ):
        "Mute a user for a specified amount of time"
        try:
            guild_id = interaction.user.guild.id
            cur = CONNECTION.cursor()
            cur.execute("SELECT role_id FROM mute WHERE guild_id = %s", (guild_id,))
            data = cur.fetchone()
            role_id = data[0]
            role_name = interaction.user.guild.get_role(role_id)
            role = discord.utils.get(interaction.user.guild.roles, name=f"{role_name}")

            await member.add_roles(role)
            embed = discord.Embed(
                title=f"Temporarily Muted {member}",
                description=f"{interaction.user.mention} has temporarily muted {member.mention} for {time} hours.",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed)

            cur = CONNECTION.cursor()
            cur.execute("INSERT INTO tempmute (guild_id, user_id, role_id, time) VALUES (%s, %s, %s, %s)", (guild_id, member.id, role.id, (datetime.datetime.now() + datetime.timedelta(hours=time))))
            CONNECTION.commit()

        except TypeError:
            embed = discord.Embed(
                title = "No Role Set",
                description = f"It seems you haven't set a muted role yet. Please go do that with `/setmute` before running this command.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.default_permissions(manage_roles=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(member='Name of the member you want to mute')
    @app_commands.describe(reason='Reason for muting the member')
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):
        "Mutes a user for an indefinite amount of time"
        try:
            guild_id = interaction.user.guild.id
            cur = CONNECTION.cursor()
            cur.execute("SELECT role_id FROM mute WHERE guild_id = %s", (guild_id,))
            data = cur.fetchone()
            role_id = data[0]
            role_name = interaction.user.guild.get_role(role_id)
            role = discord.utils.get(interaction.user.guild.roles, name=f"{role_name}")

            await member.add_roles(role)
            embed = discord.Embed(
                title=f"Muted {member}",
                description=f"{interaction.user.mention} has successfully muted {member.mention} for `\"{reason}\"`.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed)

        except TypeError or AttributeError:
            embed = discord.Embed(
                title = "No Role Set",
                description = f"It seems you haven't set a muted role yet. Please go do that with `/setmute` before running this command.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.default_permissions(manage_roles=True)
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(member='Name of the member you want to unmute')
    async def unmute(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        "Unmute a specified member"
        try:
            guild_id = interaction.user.guild.id
            cur = CONNECTION.cursor()
            cur.execute("SELECT role_id FROM mute WHERE guild_id = %s", (guild_id,))
            data = cur.fetchone()
            role_id = data[0]
            role_name = interaction.user.guild.get_role(role_id)
            role = discord.utils.get(interaction.user.guild.roles, name=f"{role_name}")

            if role in member.roles:
                await member.remove_roles(role)
                embed = discord.Embed(
                    title=f"Unmuted {member}",
                    description=f"{interaction.user.mention} has successfully unmuted {member.mention}.",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.avatar.url)
                embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
                await interaction.response.send_message(embed=embed)

            else:
                embed = discord.Embed(
                    title="User Isn't Muted",
                    description=f"{member.mention} isn't muted, therefore I cannot unmute them. Maybe you meant to mute them with the `mute` command?",
                    color=BOT_COLOR
                )
                embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except TypeError or AttributeError:
            embed = discord.Embed(
                title="No Role Set",
                description=f"It seems you haven't set a muted role yet. Please go do that with `/setmute` before running this command.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Mute(bot))