import discord
import asyncio
from discord.ext import commands
from datetime import datetime

from utils.helpers import *

log_channel_id = 889293946801516554
color = 0xc48aff

class Mute_(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def setmute(self, 
        ctx: commands.Context, 
        role_name: discord.Role=commands.Option(description="Name of muted role")
    ):
        "Set the role for users to be given when muted"
        guild_id = ctx.author.guild.id
        role = role_name
        role_id = role.id

        cursor = await self.bot.db.execute("UPDATE mute SET role_id = ? WHERE guild_id = ?", (role_id, guild_id))
        await self.bot.db.commit()

        if cursor.rowcount == 0:
            cursor = await self.bot.db.execute("INSERT INTO mute (role_id, guild_id) VALUES(?, ?)", (role_id, guild_id))
            await self.bot.db.commit()

        embed = discord.Embed(
            title = "Mute Role Changed -",
            description = f"<@&{role_id}> has been assigned as the mute role for {ctx.author.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @setmute.error
    async def setmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description = "• You are missing the `manage roles` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage roles` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)
            
        elif isinstance(error, commands.RoleNotFound):
            embed = discord.Embed(
                colour = color,
                title = "→ Role Not Found!",
                description = f"• That role wasn't found. Check your spelling, or simply just ping the role you want to assign as the muted role. Example: `{ctx.prefix}setmute @Muted`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ No Role Given!",
                description = f"• It seems you didn't provide a role for me. Heres an example on how to use the command: `{ctx.prefix}setmute @Muted`, or do `{ctx.prefix}help` for help."
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
    @commands.has_permissions(manage_roles=True)
    async def delmute(self, ctx: commands.Context):
        "Delete the role set to be given to muted users"
        guild_id = ctx.author.guild.id
        async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                await self.bot.db.execute(f"DELETE FROM mute WHERE guild_id = ?", (guild_id,))
                await self.bot.db.commit()

                embed = discord.Embed(
                    title = "Mute Role Deleted -",
                    description = f"The mute role for {ctx.author.guild.name} has been deleted.",
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Mute Role Not Set!",
                    description = f"• The mute role is not set, therefore there is no role I can delete."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed, ephemeral=True)


    @delmute.error
    async def delmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage roles` permission."
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
                description = "• I am missing `manage roles` permission. \nAsk an admin to fix this issue."
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
    @commands.has_permissions(manage_roles=True)
    async def muterole(self, ctx: commands.Context):
        "See the current role set for when users are muted"
        guild_id = ctx.author.guild.id
        async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                role_id = data[0]
                embed = discord.Embed(
                    title = f"Mute role for {ctx.author.guild.name}",
                    description= f'<@&{role_id}>'
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await ctx.send(embed=embed)
            
            else:
                embed = discord.Embed(
                    title = f"→ Mute Role Not Set!",
                    description= f'The mute role has not yet been set. Ask an admin to set it up using `{ctx.prefix}setmute`'
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await ctx.send(embed=embed, ephemeral=True)


    @muterole.error
    async def muterole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage roles` permission."
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
                description = "• I am missing `manage roles` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ No Role Set!",
                description = f"• It seems you haven't set a muted role yet. Please go do that with `{ctx.prefix}setmute` before running this command."
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
    @commands.has_permissions(manage_roles=True)
    async def tempmute(self, 
        ctx, 
        member: discord.Member=commands.Option(description="Member to be muted"), 
        time: str and int=commands.Option(description="Amount of time. EX: 5 days, or 2 hours")
    ): 
        "Mute a user for a specified amount of time"
        log = self.bot.get_channel(log_channel_id)
        if member == None:
            embed = discord.Embed(
                colour = color,
                title = "→ No Member!",
                description = f"• Please provide a member for me to mute. Example: `{ctx.prefix}mute @bob 3."
            )
            await ctx.send(embed=embed, ephemeral=True)

        elif time == None:
            embed = discord.Embed(
                colour = color,
                title = "→ No Time!",
                description = f"• Please provide an amount of time for me to mute {member} for. Example: `{ctx.prefix}mute @bob 3`."
            )
            await ctx.send(embed=embed, ephemeral=True)

        elif time != None and member != None:
            minutes = time * 3600
            guild_id = ctx.author.guild.id
            async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                data = await cursor.fetchone()
                role_id = data[0]
            role_name = ctx.guild.get_role(role_id)
            role = discord.utils.get(ctx.guild.roles, name=f"{role_name}")
            await member.add_roles(role)
            embed = discord.Embed(
                title = f"**User {member} has been muted for {time} hours.**",
                colour = discord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                minutes = time * 3600
                guild_id = ctx.author.guild.id
                async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                    data = await cursor.fetchone()
                    role_id = data[0]
                role_name = ctx.guild.get_role(role_id)
                role = discord.utils.get(ctx.guild.roles, name=f"{role_name}")
                await member.add_roles(role)
                embed = discord.Embed(
                    title = f"**User {member} has been muted for {time} hours.**",
                    colour = discord.Colour.red()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)

            if minutes:
                await asyncio.sleep(minutes)
                await member.remove_roles(role)

    
    @tempmute.error
    async def tempmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage roles` permission."
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
                description = "• I am missing `manage roles` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ No Role Set!",
                description = f"• It seems you haven't set a muted role yet. Please go do that with `{ctx.prefix}setmute` before running this command."
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
    @commands.has_permissions(manage_roles=True)
    async def mute(self, 
        ctx: commands.Context, 
        member: discord.Member=commands.Option(description="Member to be muted"), 
        reason: str=commands.Option(description="Reason for muting the user")
    ): 
        "Mutes a user for an indefinite amount of time"
        log = self.bot.get_channel(log_channel_id)
        if member == None:
            embed = discord.Embed(
                colour = color,
                title = "→ No Member!",
                description = f"• Please provide a member for me to mute. Example: `{ctx.prefix}mute @bob spamming."
            )
            await ctx.send(embed=embed, ephemeral=True)

        elif member != None:
            guild_id = ctx.author.guild.id
            async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                data = await cursor.fetchone()
                role_id = data[0]
            role_name = ctx.guild.get_role(role_id)
            role = discord.utils.get(ctx.guild.roles, name=f"{role_name}")
            await member.add_roles(role)
            embed = discord.Embed(
                title = f"**User {member} has been muted for {reason}.**",
                colour = discord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = discord.Embed(
                    title = f"**User {member} has been muted for {reason}.**",
                    colour = discord.Colour.red()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage roles` permission."
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
                description = "• I am missing `manage roles` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ No Role Set!",
                description = f"• It seems you haven't set a muted role yet. Please go do that with `{ctx.prefix}setmute` before running this command."
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
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, 
        ctx: commands.Context, 
        member: discord.Member=commands.Option(description="Member to be unmuted")
    ):
        "Unmute a specified member"
        if member == None:
            embed = discord.Embed(
                colour = color,
                title = "→ No Member!",
                description = f"• Please provide a member for me to mute. Example: `{ctx.prefix}unmute @bob`."
            )
            await ctx.send(embed=embed, ephemeral=True)
        
        elif member != None:
            log = self.bot.get_channel(log_channel_id)
            guild_id = ctx.author.guild.id
            async with self.bot.db.execute("SELECT role_id FROM mute WHERE guild_id = ?", (guild_id,)) as cursor:
                data = await cursor.fetchone()
                role_id = data[0]
            role_name = ctx.guild.get_role(role_id)
            role = discord.utils.get(ctx.guild.roles, name=f"{role_name}")
            embed = discord.Embed(
                title = f"**User {member} has been unmuted.**",
                colour = discord.Colour.green()
            )
            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)
            await member.remove_roles(role)

            if ctx.guild.id == 889027208964874240:
                embed = discord.Embed(
                    title = f"**User {member} has been unmuted.**",
                    colour = discord.Colour.green()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage roles` permission."
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
                description = "• I am missing `manage roles` permission. \nAsk an admin to fix this issue."
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


def setup(bot):
    bot.add_cog(Mute_(bot))