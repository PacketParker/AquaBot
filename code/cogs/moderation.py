import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
import datetime

timestamp=str(datetime.datetime.utcnow())
log_channel_id = 889293946801516554

yellow = 0xffc400
color = 0xc48aff

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        message = ctx.message

        if reason == None:
            await ctx.send(f"{ctx.author.mention}, you must provide a reason in order to kick {member}")
        
        elif reason != None:
            await member.kick(reason=reason)
            embed = nextcord.Embed(
                title = f"**User {member} has been kicked for {reason}**",
                colour = yellow
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `kick members` permission."
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `kick members` permission. \nAsk an admin to fix this issue."
            )
            await ctx.send(embed=embed)
        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
            )
            await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured when trying to execute that command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        message = ctx.message

        if reason == None:
            await ctx.send(f"{ctx.author.mention}, you must provide a reason in order to ban {member}")

        elif reason != None:
            await member.ban(reason=reason)
            embed = nextcord.Embed(
                title = f"**User {member} has been banned for {reason}**",
                colour = nextcord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `ban members` permission."
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `ban members` permission. \nAsk an admin to fix this issue."
            )
            await ctx.send(embed=embed)
        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
            )
            await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured when trying to execute that command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: nextcord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        message = ctx.message

        if reason == None:
            await member.ban(reason=reason)
            await member.unban()
            embed = nextcord.Embed(
                title = f"**User {member} has been soft-banned with no given reason**",
                colour = nextcord.Colour.orange()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)

        elif reason != None:
            await member.ban(reason=reason)
            await member.unban()
            embed = nextcord.Embed(
                title = f"**User {member} has been soft-banned for {reason}**",
                colour = nextcord.Colour.orange()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)


    @softban.error
    async def softban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `ban members` permission."
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `ban members` permission. \nAsk an admin to fix this issue."
            )
            await ctx.send(embed=embed)
        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
            )
            await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured when trying to execute that command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            await ctx.send(embed=embed)


    #@commands.command()
    #@commands.has_permissions(kick_members=True)
    #async def mute(self, ctx, member: nextcord.Member, *, reason=None):
#Give user the muted role 


    #@commands.command()
    #@commands.has_permissions(kick_members=True)
    #async def unmute(self, ctx, member: nextcord.Member, *, reason=None):
#Takes muted role away from user


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: nextcord.TextChannel=None, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        channel = channel or ctx.channel
        message = ctx.message

        if reason == None:
            cuties = nextcord.utils.get(ctx.guild.roles, name="cuties")
            await channel.set_permissions(cuties, send_messages=False)
            shout_ping = nextcord.utils.get(ctx.guild.roles, name="shout ping")
            await channel.set_permissions(shout_ping, send_messages=False)
            nitro_ping = nextcord.utils.get(ctx.guild.roles, name="nitro ping")
            await channel.set_permissions(nitro_ping, send_messages=False)
            event_ping = nextcord.utils.get(ctx.guild.roles, name="event ping")
            await channel.set_permissions(event_ping, send_messages=False)
            embed = nextcord.Embed(
                title = f"**Channel `{channel.name}` has been locked**",
                description = f"No given reason",
                colour = nextcord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/locked_1f512.png")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

        if reason != None:
            cuties = nextcord.utils.get(ctx.guild.roles, name="cuties")
            await channel.set_permissions(cuties, send_messages=False)
            shout_ping = nextcord.utils.get(ctx.guild.roles, name="shout ping")
            await channel.set_permissions(shout_ping, send_messages=False)
            nitro_ping = nextcord.utils.get(ctx.guild.roles, name="nitro ping")
            await channel.set_permissions(nitro_ping, send_messages=False)
            event_ping = nextcord.utils.get(ctx.guild.roles, name="event ping")
            await channel.set_permissions(event_ping, send_messages=False)
            embed = nextcord.Embed(
                title = f"**Channel `{channel.name}` has been locked**",
                description = f"Reason: {reason}",
                colour = nextcord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/locked_1f512.png")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)


    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            await ctx.send(embed=embed)
        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
            )
            await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured when trying to execute that command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: nextcord.TextChannel=None, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        channel = channel or ctx.channel
        message = ctx.message

        if reason == None:
            cuties = nextcord.utils.get(ctx.guild.roles, name="cuties")
            await channel.set_permissions(cuties, send_messages=True)
            shout_ping = nextcord.utils.get(ctx.guild.roles, name="shout ping")
            await channel.set_permissions(shout_ping, send_messages=True)
            nitro_ping = nextcord.utils.get(ctx.guild.roles, name="nitro ping")
            await channel.set_permissions(nitro_ping, send_messages=True)
            event_ping = nextcord.utils.get(ctx.guild.roles, name="event ping")
            await channel.set_permissions(event_ping, send_messages=True)
            embed = nextcord.Embed(
                title = f"**Channel `{channel.name}` has been unlocked**",
                description = f"No given reason",
                colour = nextcord.Colour.magenta()
            )
            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/unlocked_1f513.png")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

        if reason != None:
            cuties = nextcord.utils.get(ctx.guild.roles, name="cuties")
            await channel.set_permissions(cuties, send_messages=True)
            shout_ping = nextcord.utils.get(ctx.guild.roles, name="shout ping")
            await channel.set_permissions(shout_ping, send_messages=True)
            nitro_ping = nextcord.utils.get(ctx.guild.roles, name="nitro ping")
            await channel.set_permissions(nitro_ping, send_messages=True)
            event_ping = nextcord.utils.get(ctx.guild.roles, name="event ping")
            await channel.set_permissions(event_ping, send_messages=True)
            embed = nextcord.Embed(
                title = f"**Channel `{channel.name}` has been unlocked**",
                description = f"Reason: {reason}",
                colour = nextcord.Colour.magenta()
            )
            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/unlocked_1f513.png")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)


    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            await ctx.send(embed=embed)
        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
            )
            await ctx.send(embed=embed)

        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured when trying to execute that command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
