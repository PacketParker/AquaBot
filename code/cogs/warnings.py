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
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx: commands.Context, member: nextcord.Member=None, *, reason=None):
        guild_id = ctx.author.guild.id
        user_id = member.id
        await self.bot.db.execute("INSERT OR IGNORE INTO warnings (guild_id, user_id, warning) VALUES (?,?,?)", (guild_id, user_id, reason))
        await self.bot.db.commit()

        embed = nextcord.Embed(
            title = f"{member.name}#{member.discriminator} Has Been Warned -",
            description = f"User was warned in `{ctx.author.guild.name}`. Reason = {reason}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)    


    @commands.command()
    async def warnings(self, ctx: commands.Context, *, member: nextcord.Member):
        guild_id = ctx.guild.id
        user_id = member.id

        async with self.bot.db.execute("SELECT warning FROM warnings WHERE guild_id = ? AND user_id = ?", (guild_id, user_id)) as cursor:
            data = await cursor.fetchone()
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
                
        if warnings == None or 0 and not data:
            embed = nextcord.Embed(
                colour = color,
                title = "→ User has no warnings!",
                description = f"• {member.mention} has not been warned in the past, or all of their warnings have been deleted."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed)

        else:
            # get user exp
            async with self.bot.db.execute("SELECT warning FROM warnings WHERE guild_id = ? AND user_id = ?", (guild_id, user_id)) as cursor:
                data = await cursor.fetchone()
                warnings = data[0]

            await ctx.send(f"WARNINGS FOR {member.name}#{member.discriminator} \n {warnings}")




def setup(bot):
    bot.add_cog(Warnings(bot))