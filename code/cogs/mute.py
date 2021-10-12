import nextcord
import asyncio
import re
from nextcord.ext import commands
import sys
import traceback
from datetime import datetime

log_channel_id = 889293946801516554
color = 0xc48aff
time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class Mute_(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command(aliases = ["mute"])
    @commands.has_permissions(manage_roles=True)
    async def mute_(self, ctx, member:nextcord.Member=None, *, argument=None): 
        log = self.bot.get_channel(log_channel_id)
        if member == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Member!",
                description = f"• Please provide a member for me to mute. Example: `$mute @bob 3d 5h 7m 9s."
            )
            await ctx.send(embed=embed)

        elif argument == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Time!",
                description = f"• Please provide an amount of time for me to mute {member} for. Example: `$mute @bob 3d 5h 7m 9s`."
            )
            await ctx.send(embed=embed)

        elif argument != None and member != None:
            args = argument.lower()
            matches = re.findall(time_regex, args)
            time = 0
            for v, k in matches:
                time += time_dict[k]*float(v)
            role = nextcord.utils.get(ctx.guild.roles, name=f"Muted")
            await member.add_roles(role)
            embed = nextcord.Embed(
                title = f"**User {member} has been muted for {argument}.**",
                colour = nextcord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                args = argument.lower()
                matches = re.findall(time_regex, args)
                time = 0
                for v, k in matches:
                    time += time_dict[k]*float(v)
                role = nextcord.utils.get(ctx.guild.roles, name=f"Muted")
                await member.add_roles(role)
                embed = nextcord.Embed(
                    title = f"**User {member} has been muted for {argument}.**",
                    colour = nextcord.Colour.red()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)

            if time:
                await asyncio.sleep(time)
                await member.remove_roles(role)

    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: nextcord.Member=None):
        if member == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Member!",
                description = f"• Please provide a member for me to mute. Example: `$unmute @bob`."
            )
            await ctx.send(embed=embed)
        
        elif member != None:
            log = self.bot.get_channel(log_channel_id)
            role = nextcord.utils.get(ctx.guild.roles, name="Muted")
            embed = nextcord.Embed(
                title = f"**User {member} has been unmuted.**",
                colour = nextcord.Colour.green()
            )
            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)
            await member.remove_roles(role)

            if ctx.guild.id == 889027208964874240:
                embed = nextcord.Embed(
                    title = f"**User {member} has been unmuted.**",
                    colour = nextcord.Colour.green()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @unmute.error
    async def unmute_error(self, ctx):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Mute_(bot))