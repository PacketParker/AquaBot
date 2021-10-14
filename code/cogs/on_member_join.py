import nextcord
import asyncio
import re
from nextcord.ext import commands
import sys
import traceback
from datetime import datetime

from modules.id_db import ID

log_channel_id = 889293946801516554
color = 0xc48aff

class Join_(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.join = ID()


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def setjoin(self, ctx: commands.Context, *, channel_name: nextcord.TextChannel):
        guild_id = ctx.author.guild.id
        join = channel_name
        join_id = join.id
        self.join.set_channel(guild_id, join_id)
        embed = nextcord.Embed(
            title = "Join Channel Changed -",
            description = f"<#{join_id}> has been assigned as the channel for new member message in {ctx.author.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @setjoin.error
    async def setjoin_error(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Channel Not Found!",
                description = f"• That role wasn't found. Check your spelling, or simply just tag the channel you want to assign for new member messages. Example: `$setjoin #channel`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Channel Given!",
                description = f"• It seems you didn't provide a channel for me. Heres an example on how to use the command: `$setjoin #channel`, or do `$help` for help."
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
    @commands.has_permissions(manage_roles=True)
    async def joinchannel(self, ctx: commands.Context):
        guild_id = ctx.author.guild.id
        profile = self.join.channel_get_entry_for_commands(guild_id)
        embed = nextcord.Embed(
            title = f"New member message channel for {ctx.author.guild.name}",
            description= '<#{}>'.format(profile[1])
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @joinchannel.error
    async def joinchannel_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Role Set!",
                description = f"• It seems you haven't set a muted role yet. Please go do that with `$setmute` before running this command."
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


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = member.guild.id
        profile = self.join.channel_get_entry_for_commands(guild_id)
        channel = self.bot.get_channel(profile[2])

        embed = nextcord.Embed(
            title = f"New Member",
            description = f"Welcome {member.mention} to `{member.guild}`. Thank you for joining our server!",
            colour = nextcord.Colour.random()
        )
        embed.set_footer(text="User joined at: " + datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        embed.set_thumbnail(url=member.avatar.url)

        await channel.send(embed=embed)
            

def setup(bot):
    bot.add_cog(Join_(bot))