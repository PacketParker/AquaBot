import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from datetime import datetime
import time
import asyncio

log_channel_id = 889293946801516554

yellow = 0xffc400
color = 0xc48aff

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
#TODO have the bot dm a member when they have been muted, unmuted, banned, softbanned, kicked, etc.

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def createmute(self, ctx):
        server = ctx.message.guild
        perms = nextcord.Permissions(send_messages=False, read_messages=True)
        await self.bot.create_role(server, name='Muted', permissions=perms)


    @commands.command()
    @commands.has_permissions()
    async def mute(self, ctx, member: nextcord.Member=None, *, reason=None, time):
        log = self.bot.get_channel(log_channel_id)
        role = nextcord.utils.get(ctx.guild.roles, name="muted")
        time_convert = {"s":1, "m":60, "h":3600,"d":86400}
        tempmute= int(time[0]) * time_convert[time[-1]]

        if ctx.message.guild.id != 891743644938297395:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Not Available!",
                description = f"• This command is only available for the admins in the official bot help server."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
   
        if member == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't mute anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        if reason == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Please provide a reason!",
                description = f"• I can't mute anyone if a reason is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        if ctx.message.guild.id == 891743644938297395 and member != None and reason != None:
            await member.add_roles(role)
            embed = nextcord.Embed(
                title = f"**User {member} has been muted for {reason}**",
                description = f"They have been muted for {tempmute}",
                colour = yellow
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)
            await asyncio.sleep(tempmute)
            await member.remove_roles(role)
            await ctx.send(f"{member} has just finished their tempmute.")


    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, TypeError):
            await ctx.send("Please provide a member, reason, and then time to have this memeber muted. Example: `$mute @ted being stupid 60m")
   
   
    #@commands.command()
    #@commands.has_permissions(kick_members=True)
    #async def mute(self, ctx, member: nextcord.Member, *, reason=None):
#Give user the muted role 


    #@commands.command()
    #@commands.has_permissions(kick_members=True)
    #async def unmute(self, ctx, member: nextcord.Member, *, reason=None):
#Takes muted role away from user


def setup(bot):
    bot.add_cog(Mute(bot))