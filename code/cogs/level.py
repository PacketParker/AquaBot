import discord
from discord.ext import commands
import math
import asyncio
from datetime import datetime

color = 0xc48aff

class messageCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
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


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def setlvl(self, 
        ctx: commands.Context, 
        channel: discord.TextChannel=commands.Option(description="Channel where you want level up messages to be sent")
    ):
        "Set a channel for level up messages to be sent"
        guild_id = ctx.author.guild.id
        channel = channel
        channel_id = channel.id

        cursor = await self.bot.db.execute("UPDATE level_channel SET channel_id = ? WHERE guild_id = ?", (channel_id, guild_id))
        await self.bot.db.commit()

        if cursor.rowcount == 0:
            cursor = await self.bot.db.execute("INSERT INTO level_channel (channel_id, guild_id) VALUES(?, ?)", (channel_id, guild_id))
            await self.bot.db.commit()

        embed = discord.Embed(
            title = "Level Channel Changed -",
            description = f"<#{channel_id}> has been assigned as the level-up message channel for {ctx.author.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @setlvl.error
    async def setlvl_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Required Argument!",
                description = f"• {error}"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
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
    @commands.has_permissions(administrator=True)
    async def lvlreset(self, ctx):
        "Reset all levels in your server"
        guild_id = ctx.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `{ctx.prefix}setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed, ephemeral=True)
                
        if channel_id == None or 0 and not data:
            embed = discord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `{ctx.prefix}setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed, ephemeral=True)

        else:
            embed = discord.Embed(
                color=0xa3a3ff, 
                title = ":warning: ALERT :warning: ", 
                description=f"{ctx.author.mention}, are you sure you want to delete the levels for everyone in this server? y/n",
            )
            embed.set_footer(text="Send either `y` or `n` in order to continue.")
            
            await ctx.send(embed=embed)

            a = ["y", "yes", "Yes", "YEs", "YES"]
            b = ["n", "no", "No", "NO"] 

            msg = await self.bot.wait_for('message', check=lambda message:message.author == ctx.author and message.channel.id == ctx.channel.id)
            if msg.content in a:
                embed = discord.Embed(
                    title=f"All levels have just been DELETED!", 
                    description=f"Levels deleted by: {ctx.author.name}#{ctx.author.discriminator}",
                    color=0xa3a3ff
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await self.bot.db.execute("DELETE FROM guildData WHERE guild_id = ?", (guild_id,))
                await ctx.send(embed=embed)

            elif msg.content in b:
                embed = discord.Embed(
                    title = ":red_circle: NOTICE :red_circle:", 
                    description = f"All levels were NOT deleted!",
                    color=0xa3a3ff
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title = ":red_circle: NOTICE :red_circle:", 
                    description = "All levels were NOT deleted!",
                    color=0xa3a3ff
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await ctx.send(embed=embed)


    @lvlreset.error
    async def lvlreset_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `administrator` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Required Argument!",
                description = f"• {error}"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `administrator` permission. \nAsk an admin to fix this issue."
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
    @commands.has_permissions(manage_channels=True)
    async def dellevel(self, ctx):
        "Remove the channel assigned from sending level up messages"
        guild_id = ctx.author.guild.id
        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                await self.bot.db.execute(f"DELETE FROM level_channel WHERE guild_id = ?", (guild_id,))
                await self.bot.db.commit()

                embed = discord.Embed(
                    title = "Leveling Channel Deleted -",
                    description = f"The level channel for {ctx.author.guild.name} has been deleted.",
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• No leveling channel has been setup, therefore I can not delete any channel."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed, ephemeral=True)


    @dellevel.error
    async def dellevel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Required Argument!",
                description = f"• {error}"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
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
    @commands.has_permissions(manage_channels=True)
    async def lvlchannel(self, ctx):
        "See the channel currently assigned to send level up messages to"
        guild_id = ctx.author.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `{ctx.prefix}setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed, ephemeral=True)
                
        if channel_id == None or 0 and not data:
            embed = discord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `{ctx.prefix}setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed, ephemeral=True)

        else:
            embed = discord.Embed(
                title = f"Leveling Channel For {ctx.author.guild.name}",
                description= f'<#{channel_id}>'
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @lvlchannel.error
    async def lvlchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Required Argument!",
                description = f"• {error}"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)
            
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `{ctx.prefix}setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed, ephemeral=True)

        else:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)


    @commands.command(aliases=["lvl"])
    async def level(self, 
        ctx,
        member: discord.Member=commands.Option(description="Member whose level you want to see")
    ):
        "See the current level for the given member"
        self.bot.multiplier = 1
        guild_id = ctx.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `{ctx.prefix}setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed, ephemeral=True)
                
        if channel_id == None or 0 and not data:
            embed = discord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `{ctx.prefix}setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed, ephemeral=True)

        else:
            # get user exp
            async with self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id)) as cursor:
                data = await cursor.fetchone()
                exp = data[0]

                # calculate rank
            async with self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
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
            embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}")
            embed.add_field(name="Level Progress", value=f"{round(lvl_percentage, 2)}%")

            await ctx.send(embed=embed)


    @level.error
    async def level_error(self, ctx, error):
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
    async def lvlboard(self, ctx): 
        "See the current leaderboard for leveling in your server"
        guild_id = ctx.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Leveling Not Setup!",
                    description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `{ctx.prefix}setlevel` command."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed, ephemeral=True)
                
        if channel_id == None or 0 and not data:
            embed = discord.Embed(
                colour = color,
                title = "→ Leveling Not Setup!",
                description = f"• Leveling for this server has not been setup. Ask an admin to set it up by running the `{ctx.prefix}setlevel` command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed, ephemeral=True)

        else:
            buttons = {}
            for i in range(1, 6):
                buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i # only show first 5 pages

            previous_page = 0
            current = 1
            index = 1
            entries_per_page = 10

            embed = discord.Embed(title=f"Leaderboard Page {current}", description="", colour=discord.Colour.gold())
            msg = await ctx.send(embed=embed)

            for button in buttons:
                await msg.add_reaction(button)

            while True:
                if current != previous_page:
                    embed.title = f"Leaderboard Page {current}"
                    embed.description = ""

                    async with self.bot.db.execute(f"SELECT user_id, exp FROM guildData WHERE guild_id = ? ORDER BY exp DESC LIMIT ? OFFSET ? ", (ctx.guild.id, entries_per_page, entries_per_page*(current-1),)) as cursor:
                        index = entries_per_page*(current-1)

                        async for entry in cursor:
                            index += 1
                            member_id, exp = entry
                            member = ctx.guild.get_member(member_id)
                            embed.description += f"{index}) {member.mention} : {exp}\n"

                        await msg.edit(embed=embed)

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

                except asyncio.TimeoutError:
                    return await msg.clear_reactions()

                else:
                    previous_page = current
                    await msg.remove_reaction(reaction.emoji, ctx.author)
                    current = buttons[reaction.emoji]


    @lvlboard.error
    async def lvlboard_error(self, ctx, error):
        embed = discord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(messageCount(bot))