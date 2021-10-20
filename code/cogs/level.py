import nextcord
from nextcord import Color
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request
import aiosqlite
import math
import asyncio
from datetime import datetime

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff


class messageCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        self.bot.multiplier = 1

        async with self.bot.dbLevelChannel.execute("SELECT channel_id FROM level_channel WHERE guild_id = ?", (message.guild.id,)) as cursor:
            data = await cursor.fetchone()
            channel = data[0]

            if channel == 0 or None:
                return

        if not message.author.bot:
            cursor = await self.bot.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)", (message.guild.id, message.author.id, 1)) 

            if cursor.rowcount == 0:
                await self.bot.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
                cur = await self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
                data = await cur.fetchone()
                exp = data[0]
                lvl = math.sqrt(exp) / self.bot.multiplier
            
                if lvl.is_integer():
                    await message.channel.send(f"{message.author.mention} well done! You're now level: {int(lvl)}.")

            await self.bot.db.commit()


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def setlevel(self, ctx: commands.Context, *, channel_name: nextcord.TextChannel):
        guild_id = ctx.author.guild.id
        channel = channel_name
        channel_id = channel.id
        cursor = await self.bot.dbLevelChannel.execute("INSERT OR IGNORE INTO level_channel (guild_id, channel_id) VALUES (?,?)", (guild_id, channel_id))
        await self.bot.dbLevelChannel.commit()
        embed = nextcord.Embed(
            title = "Mute Role Changed -",
            description = f"<#{channel_id}> has been assigned as the mute role for {ctx.author.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @setlevel.error
    async def setlevel_error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Role Not Found!",
                description = f"• That role wasn't found. Check your spelling, or simply just ping the role you want to assign as the muted role. Example: `$setmute @Muted`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Role Given!",
                description = f"• It seems you didn't provide a role for me. Heres an example on how to use the command: `$setmute @Muted`, or do `$help` for help."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @commands.command()
    async def stats(self, ctx, member: nextcord.Member=None):
        self.bot.multiplier = 1

        if member is None: member = ctx.author

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

        embed = nextcord.Embed(title=f"Stats for {member.name}", colour=nextcord.Colour.gold())
        embed.add_field(name="Level", value=str(lvl))
        embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}")
        embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}")
        embed.add_field(name="Level Progress", value=f"{round(lvl_percentage, 2)}%")

        await ctx.send(embed=embed)

    @commands.command()
    async def levelboard(self, ctx): 
        buttons = {}
        for i in range(1, 6):
            buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i # only show first 5 pages

        previous_page = 0
        current = 1
        index = 1
        entries_per_page = 10

        embed = nextcord.Embed(title=f"Leaderboard Page {current}", description="", colour=nextcord.Colour.gold())
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



def setup(bot):
    bot.add_cog(messageCount(bot))
