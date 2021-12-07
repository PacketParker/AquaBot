import discord
from discord.ext import commands
from datetime import datetime

from discord.ext.commands.errors import MemberNotFound, MissingRequiredArgument

color = 0xc48aff

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, 
        ctx: commands.Context, 
        member: discord.Member=commands.Option(description="Member you want to warn"), 
        *, 
        reason: str=commands.Option(description="Reason for warning a member")
    ):
        "Warn a member for a given reason"
        guild_id = ctx.author.guild.id
        user_id = member.id
        warn_id = ctx.message.id
        warn_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        warned_by = ctx.author.id

        if member == None:
            embed = discord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't warn anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif reason == None:
            await ctx.send(f"{ctx.author.mention}, you must provide a reason in order to warn {member.name}#{member.discriminator}")

        elif reason != None and member != None:
            await self.bot.db.execute("INSERT OR IGNORE INTO warnings (warn_id, guild_id, user_id, warning, warn_time, warned_by) VALUES (?,?,?,?,?,?)", (warn_id, guild_id, user_id, reason, warn_time, warned_by))
            await self.bot.db.commit()

            embed = discord.Embed(
                title = f"{member.name}#{member.discriminator} Has Been Warned -",
                color = discord.Colour.dark_orange()
            )

            embed.add_field(name = f"User was warned in `{ctx.author.guild.name}`.", value = f"Reason - {reason}")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)    


    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, AttributeError):
            embed = discord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't warn anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Required Argument!",
                description = f"• {error}"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, MemberNotFound):
            embed = discord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• That member was not found, please check your spelling and try again."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage messages` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)
        
        elif not MissingRequiredArgument:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, 
        ctx: commands.Context, 
        member: discord.Member=commands.Option(description="The member whose warnings you want to see")
    ):
        "Show all warnings for a given reason"
        guild_id = ctx.guild.id
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
                return await ctx.send(embed=embed)
                
        if member == None:
            embed = discord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't kick anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if warnings == None or 0 and not data and member != None:
            embed = discord.Embed(
                colour = color,
                title = "→ User has no warnings!",
                description = f"• {member.mention} has not been warned in the past, or all of their warnings have been deleted."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed)

        else:
            async with self.bot.db.execute("SELECT * FROM warnings WHERE guild_id = ? AND user_id = ?", (guild_id, user_id)) as cursor:
                data = await cursor.fetchall()

                embed = discord.Embed(
                    title = f"**Warnings For - {member.name}#{member.discriminator}**",
                    color = 0xffe75c
                )
                for data in data:
                    embed.add_field(name = f"Warning Reason - \"{data[3]}\" | ID = {data[0]}", value = f"Warned By: <@{data[5]}> | Warned At: {data[4]}\n", inline=False)
                    
            await ctx.send(embed=embed)


    @warnings.error
    async def warnings_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            embed = discord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• That member was not found, please check your spelling and try again."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Required Argument!",
                description = f"• {error}"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage messages` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif not MissingRequiredArgument:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, 
        ctx: commands.Context, 
        id: int=commands.Option(description="ID associated with the warning you want to delete")
    ):  
        "Delete a warning from a user with the warning ID"
        if id == None:
            embed = discord.Embed(
                colour = color,
                title = "→ No ID Provided!",
                description = f"• Please provide an warn ID for me to remove."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif id != None:
            await self.bot.db.execute(f"DELETE FROM warnings WHERE warn_id = ?", (id,))
            await self.bot.db.commit()

            embed = discord.Embed(
                title = "Warning Deleted -",
                color = discord.Colour.fuchsia()
            )

            embed.add_field(name = f"**Warning identified by - {id} - has been deleted.**", value = f"Command Issued By: {ctx.author.mention}")
            embed.set_footer(text = datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)


    @delwarn.error
    async def delwarn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage messages` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ ID Given Not Int!",
                description="• The ID you sent was not an integer (numbers), please resend the command with an int."
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
    bot.add_cog(Warnings(bot))