from xml.dom.minidom import Attr
import discord
from discord.ext import commands
import math
import asyncio
from datetime import datetime
from discord import app_commands

color = 0xc48aff

class slash_level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
            
        if message.author == self.bot.user:
            return

        self.bot.multiplier = 2
        guild_id = message.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                return
                
        if channel_id == None or 0 and not data:
            return

        cursor = await self.bot.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)", (message.guild.id, message.author.id, 1)) 

        if cursor.rowcount == 0:
            await self.bot.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            cur = await self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            data = await cur.fetchone()
            exp = data[0]
            lvl = math.sqrt(exp) / self.bot.multiplier
        
            if lvl.is_integer():
                channel = self.bot.get_channel(channel_id)
                await channel.send(f"{message.author.mention} congratulations! You have leveled up, your new level is - `{int(lvl)}`")

            await self.bot.db.commit()

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(channel='Channel for level up messages to be sent')
    async def setlevel(
        self, 
        interaction: discord.Interaction, 
        channel: discord.TextChannel
    ):
        "Set a channel for level up messages to be sent"

        guild_id = interaction.user.guild.id
        channel = channel
        channel_id = channel.id

        cursor = await self.bot.db.execute("UPDATE level_channel SET channel_id = ? WHERE guild_id = ?", (channel_id, guild_id))
        await self.bot.db.commit()

        if cursor.rowcount == 0:
            cursor = await self.bot.db.execute("INSERT INTO level_channel (channel_id, guild_id) VALUES(?, ?)", (channel_id, guild_id))
            await self.bot.db.commit()

        embed = discord.Embed(
            title = "Level Channel Changed -",
            description = f"<#{channel_id}> has been assigned as the level-up message channel for {interaction.user.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    @app_commands.checks.has_permissions(manage_channels=True)
    async def dellevel(
        self, 
        interaction: discord.Interaction
    ):
        "Remove the channel assigned from sending level up messages"

        guild_id = interaction.user.guild.id
        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                await self.bot.db.execute(f"DELETE FROM level_channel WHERE guild_id = ?", (guild_id,))
                await self.bot.db.commit()

                embed = discord.Embed(
                    title = "Leveling Channel Deleted -",
                    description = f"The level channel for {interaction.user.guild.name} has been deleted.",
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• No leveling channel has been setup, therefore I can not delete any channel."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command()
    @app_commands.checks.has_permissions(manage_channels=True)
    async def levelchannel(
        self, 
        interaction: discord.Interaction
    ):
        "See the channel currently assigned to send level up messages to"

        guild_id = interaction.user.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `/setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await interaction.response.send_message(embed=embed, ephemeral=True)
                
        if channel_id == None or 0 and not data:
            embed = discord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `/setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            embed = discord.Embed(
                title = f"Leveling Channel For {interaction.user.guild.name}",
                description= f'<#{channel_id}>'
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await interaction.response.send_message(embed=embed)
            

    @app_commands.command()
    @app_commands.describe(member='Member whose level you would like to view')
    async def level(
        self, 
        interaction: discord.Interaction,
        member: discord.Member
    ):
        "See the current level for the given member"

        self.bot.multiplier = 1
        guild_id = interaction.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `/setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await interaction.response.send_message(embed=embed, ephemeral=True)
                
        if channel_id == None or 0 and not data:
            embed = discord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `/setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            # get user exp
            async with self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (interaction.guild.id, member.id)) as cursor:
                data = await cursor.fetchone()
                try:
                    exp = data[0]
                except TypeError:
                    embed = discord.Embed(title=f"Stats for {member.name}", colour=discord.Colour.gold())
                    embed.add_field(name="You don't have any exp!", value="Send some messages to get more exp and level up!")

                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                # calculate rank
            async with self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ?", (interaction.guild.id,)) as cursor:
                rank = 1
                async for value in cursor:
                    if exp < value[0]:
                        rank += 1

            lvl = int(math.sqrt(exp)//self.bot.multiplier)

            current_lvl_exp = (self.bot.multiplier*(lvl))**2
            next_lvl_exp = (self.bot.multiplier*((lvl+1)))**2

            lvl_percentage = ((exp-current_lvl_exp) / (next_lvl_exp-current_lvl_exp)) * 100

            embed = discord.Embed(title=f"Stats for {member.name}", colour=discord.Colour.gold())
            embed.add_field(name="Level", value=str(lvl))
            embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}")
            embed.add_field(name="Rank", value=f"{rank}/{interaction.guild.member_count}")
            embed.add_field(name="Level Progress", value=f"{round(lvl_percentage, 2)}%")

            await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def levelboard(
        self, 
        interaction: discord.Interaction
    ): 
        "See the current leaderboard for leveling in your server"

        guild_id = interaction.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `/setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await interaction.response.send_message(embed=embed, ephemeral=True)
                
        if channel_id == None or 0 and not data:
            embed = discord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `/setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            buttons = {}
            for i in range(1, 6):
                buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i # only show first 5 pages

            previous_page = 0
            current = 1
            index = 1
            entries_per_page = 10

            embed = discord.Embed(title=f"Leaderboard Page {current}", description="", colour=discord.Colour.gold())
            await interaction.response.send_message(embed=embed)
            msg = await interaction.original_message()

            for button in buttons:
                await msg.add_reaction(button)

            while True:
                if current != previous_page:
                    embed.title = f"Leaderboard Page {current}"
                    embed.description = ""

                    async with self.bot.db.execute(f"SELECT user_id, exp FROM guildData WHERE guild_id = ? ORDER BY exp DESC LIMIT ? OFFSET ? ", (interaction.guild.id, entries_per_page, entries_per_page*(current-1),)) as cursor:
                        index = entries_per_page*(current-1)

                        async for entry in cursor:
                            index += 1
                            member_id, exp = entry
                            member = interaction.guild.get_member(member_id)
                            embed.description += f"{index}) {member.mention} : {exp}\n"

                        await msg.edit(embed=embed)

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == interaction.user and reaction.emoji in buttons, timeout=60.0)

                except asyncio.TimeoutError:
                    return await msg.clear_reactions()

                else:
                    previous_page = current
                    await msg.remove_reaction(reaction.emoji, interaction.user)
                    current = buttons[reaction.emoji]


    @app_commands.command()
    @app_commands.checks.has_permissions(administrator=True)
    async def levelreset(
        self, 
        interaction: discord.Interaction
    ):
        "Reset all levels in your server"

        guild_id = interaction.user.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `/setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await interaction.response.send_message(embed=embed, ephemeral=True)
                
        if channel_id == None or 0 and not data:
            embed = discord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `/setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            embed = discord.Embed(
                color=0xa3a3ff, 
                title = ":warning: ALERT :warning: ", 
                description=f"{interaction.user.mention}, are you sure you want to delete the levels for everyone in this server? y/n",
            )
            embed.set_footer(text="Send either `y` or `n` in order to continue.")
            
            await interaction.response.send_message(embed=embed)

            a = ["y", "yes", "Yes", "YEs", "YES"]
            b = ["n", "no", "No", "NO"] 

            msg = await self.bot.wait_for('message', check=lambda message:message.author == interaction.user and message.channel.id == interaction.channel.id)
            if msg.content in a:
                embed = discord.Embed(
                    title=f"All levels have just been DELETED!", 
                    description=f"Levels deleted by: {interaction.user.name}#{interaction.user.discriminator}",
                    color=0xa3a3ff
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await self.bot.db.execute("DELETE FROM guildData WHERE guild_id = ?", (guild_id,))
                await self.bot.db.commit()
                await interaction.followup.send(embed=embed)

            elif msg.content in b:
                embed = discord.Embed(
                    title = ":red_circle: NOTICE :red_circle:", 
                    description = f"All levels were NOT deleted!",
                    color=0xa3a3ff
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await interaction.followup.send(embed=embed)

            else:
                embed = discord.Embed(
                    title = ":red_circle: NOTICE :red_circle:", 
                    description = "All levels were NOT deleted!",
                    color=0xa3a3ff
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(slash_level(bot))