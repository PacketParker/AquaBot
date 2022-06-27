import discord
from discord.ext import commands
from datetime import datetime
from discord import app_commands

color = 0xc48aff

class slash_join(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command() 
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(channel='The channel you would like new member messages to be sent')
    async def setjoin(
        self, 
        interaction: discord.Interaction, 
        channel: discord.TextChannel
    ):
        "Set the channel for new member messages"

        guild_id = interaction.user.guild.id
        join = channel
        channel_id = join.id
        cursor = await self.bot.db.execute("UPDATE join_channel SET channel_id = ? WHERE guild_id = ?", (channel_id, guild_id))
        await self.bot.db.commit()

        if cursor.rowcount == 0:
            cursor = await self.bot.db.execute("INSERT INTO join_channel (channel_id, guild_id) VALUES(?, ?)", (channel_id, guild_id))
            await self.bot.db.commit()

        embed = discord.Embed(
            title = "Join Channel Changed -",
            description = f"<#{channel_id}> has been assigned as the channel for new member message in {interaction.user.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    @app_commands.checks.has_permissions(manage_channels=True)
    async def deljoin(
        self, 
        interaction: discord.Interaction
    ):
        "Delete the new member channel so messages are no longer sent"

        guild_id = interaction.user.guild.id
        async with self.bot.db.execute("SELECT channel_id FROM join_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                await self.bot.db.execute(f"DELETE FROM join_channel WHERE guild_id = ?", (guild_id,))
                await self.bot.db.commit()
                embed = discord.Embed(
                    title = "New Member Message Channel Deleted -",
                    description = f"The new member message channel for {interaction.user.guild.name} has been deleted.",
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await interaction.response.send_message(embed=embed)

            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Join Channel Not Set!",
                    description = f"• The join channel is not set, therefore there is no channel I can delete."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command()
    @app_commands.checks.has_permissions(manage_channels=True)
    async def joinchannel(
        self, 
        interaction: discord.Interaction
    ):
        "See the current channel set for new member messages"

        guild_id = interaction.user.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM join_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Join Channel Not Set!",
                    description = f"• The join channel has not yet been set. Ask an admin to set it up using `/setjoin`."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await interaction.response.send_message(embed=embed, ephemeral=True)
                
        if channel_id == None or 0 and not data:
            embed = discord.Embed(
                colour = color,
                title = "→ Join Channel Not Set!",
                description = f"• The join channel has not yet been set. Ask an admin to set it up using `/setjoin`."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(
            title = f"New member message channel for {interaction.user.guild.name}",
            description= f'<#{channel_id}>'
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await interaction.response.send_message(embed=embed)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = member.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM join_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]

                if channel_id == 0:
                    return

                if channel_id == None:
                    return

                if channel_id == "NULL":
                    return

            elif not data:
                return
 
            channel = self.bot.get_channel(channel_id)

            embed = discord.Embed(
                title = f"New Member",
                description = f"Welcome {member.mention} to `{member.guild}`. Thank you for joining our server!",
                colour = discord.Colour.random()
            )
            embed.set_footer(text="User joined at: " + datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            embed.set_thumbnail(url=member.avatar.url)

            await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(slash_join(bot))