import discord
from discord.ext import commands
from datetime import datetime
from discord import app_commands

color = 0xc48aff

class slash_warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


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
        warn_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        warned_by = interaction.user.id

        await self.bot.db.execute("INSERT OR IGNORE INTO warnings (warn_id, guild_id, user_id, warning, warn_time, warned_by) VALUES (?,?,?,?,?,?)", (warn_id, guild_id, user_id, reason, warn_time, warned_by))
        await self.bot.db.commit()

        embed = discord.Embed(
            title = f"{member.name}#{member.discriminator} Has Been Warned -",
            color = discord.Colour.dark_orange()
        )

        embed.add_field(name = f"User was warned in `{interaction.user.guild.name}`.", value = f"Reason - {reason}")
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await interaction.response.send_message(embed=embed)    
    

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

        async with self.bot.db.execute("SELECT warning FROM warnings WHERE guild_id = ? AND user_id = ?", (guild_id, user_id)) as cursor:
            data = await cursor.fetchall()
            if data:
                warnings = data[0]
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ User has no warnings!",
                    description = f"• {member.mention} has not been warned in the past, or all of their warnings have been deleted."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await interaction.response.send_message(embed=embed)
                
        if warnings == None or 0 and not data and member != None:
            embed = discord.Embed(
                colour = color,
                title = "→ User has no warnings!",
                description = f"• {member.mention} has not been warned in the past, or all of their warnings have been deleted."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await interaction.response.send_message(embed=embed)

        else:
            async with self.bot.db.execute("SELECT * FROM warnings WHERE guild_id = ? AND user_id = ?", (guild_id, user_id)) as cursor:
                data = await cursor.fetchall()

                embed = discord.Embed(
                    title = f"**Warnings For - {member.name}#{member.discriminator}**",
                    color = 0xffe75c
                )
                for data in data:
                    embed.add_field(name = f"Warning Reason - \"{data[3]}\" | ID = {data[0]}", value = f"Warned By: <@{data[5]}> | Warned At: {data[4]}\n", inline=False)
                    
                await interaction.response.send_message(embed=embed)


    @app_commands.command()
    
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(id='ID of the warning you would like to delete')
    async def delwarn(
        self, 
        interaction: discord.Interaction, 
        id: str
    ):  
        "Delete a warning from a user with the warning ID"

        async with self.bot.db.execute("SELECT warn_id FROM warnings WHERE warn_id = ?", (id,)) as cursor:
            data = await cursor.fetchone()

        if data:
            await self.bot.db.execute(f"DELETE FROM warnings WHERE warn_id = ?", (id,))
            await self.bot.db.commit()

            embed = discord.Embed(
                title = "Warning Deleted -",
                color = discord.Colour.fuchsia()
            )

            embed.add_field(name = f"**Warning identified by - {id} - has been deleted.**", value = f"Command Issued By: {interaction.user.mention}")
            embed.set_footer(text = datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await interaction.response.send_message(embed=embed)
        
        else:
            embed = discord.Embed(
                colour = color,
                title = "→ Not a valid ID!",
                description="• That ID is not associated with any warnings in this server."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await interaction.response.send_message(embed=embed, ephemeral=True)               


async def setup(bot):
    await bot.add_cog(slash_warnings(bot))