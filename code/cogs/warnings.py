import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request
import aiosqlite
from datetime import datetime

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx: commands.Context, member: nextcord.Member=None, *, reason=None):
        guild_id = ctx.author.guild.id
        user_id = member.id
        warn_id = ctx.message.id
        warn_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        warned_by = ctx.author.id

        if member == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't kick anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        elif reason == None:
            await ctx.send(f"{ctx.author.mention}, you must provide a reason in order to warn {member.name}#{member.discriminator}")

        elif reason != None and member != None:
            await self.bot.db.execute("INSERT OR IGNORE INTO warnings (warn_id, guild_id, user_id, warning, warn_time, warned_by) VALUES (?,?,?,?,?,?)", (warn_id, guild_id, user_id, reason, warn_time, warned_by))
            await self.bot.db.commit()

            embed = nextcord.Embed(
                title = f"{member.name}#{member.discriminator} Has Been Warned -",
                color = nextcord.Colour.dark_orange()
            )

            embed.add_field(name = f"User was warned in `{ctx.author.guild.name}`.", value = f"Reason - {reason}")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)    


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx: commands.Context, *, member: nextcord.Member):
        guild_id = ctx.guild.id
        user_id = member.id

        async with self.bot.db.execute("SELECT warning FROM warnings WHERE guild_id = ? AND user_id = ?", (guild_id, user_id)) as cursor:
            data = await cursor.fetchall()
            if data:
                warnings = data[0]
            else:
                embed = nextcord.Embed(
                    colour = color,
                    title = "→ User has no warnings!",
                    description = f"• {member.mention} has not been warned in the past, or all of their warnings have been deleted."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed)
                
        if member == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't kick anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        if warnings == None or 0 and not data and member != None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ User has no warnings!",
                description = f"• {member.mention} has not been warned in the past, or all of their warnings have been deleted."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed)

        else:
            async with self.bot.db.execute("SELECT * FROM warnings WHERE guild_id = ? AND user_id = ?", (guild_id, user_id)) as cursor:
                data = await cursor.fetchall()

                embed = nextcord.Embed(
                    title = f"**Warnings For - {member.name}#{member.discriminator}**",
                    color = 0xffe75c
                )
                for data in data:
                    embed.add_field(name = f"Warning Reason - \"{data[3]}\" | ID = {data[0]}", value = f"Warned By: <@{data[5]}> | Warned At: {data[4]}\n", inline=False)
                    
                    
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, ctx: commands.Context, *, id: int = None):  
        if id == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ No ID Provided!",
                description = f"• Please provide an warn ID for me to remove."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        elif id != None:
            await self.bot.db.execute(f"DELETE FROM warnings WHERE warn_id = ?", (id,))
            await self.bot.db.commit()

            embed = nextcord.Embed(
                title = "Warning Deleted -",
                color = nextcord.Colour.fuchsia()
            )

            embed.add_field(name = f"**Warning identified by - {id} - has been deleted.**", value = f"Command Issued By: {ctx.author.mention}")
            embed.set_footer(text = datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Warnings(bot))