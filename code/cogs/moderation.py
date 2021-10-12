import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from datetime import datetime
import asyncio

log_channel_id = 889293946801516554

yellow = 0xffc400
color = 0xc48aff

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int=None):
        log = self.bot.get_channel(log_channel_id)
        if amount == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Amount Not Given!",
                description="• Please provide an amount of messages you would like to delete. Example: `$purge 5`"
            )
            await ctx.send(embed=embed)
    
        elif amount > 100:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Amount Too Large!",
                description="• You sent an amount larger than 100. Sorry, but you can only delete 100 messages at a time."
            )
            await ctx.send(embed=embed)

        else:
            await ctx.channel.purge(limit=amount+1)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = nextcord.Embed(
                    title = f"**{ctx.author} has run the purge command in {ctx.channel.name}**",
                    colour = yellow
                )
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await log.send(embed=embed)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage messages` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        if isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage messages` permission. \nAsk an admin to fix this issue."
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
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member=None, *, reason=None):
        log = self.bot.get_channel(log_channel_id)

        if member == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't kick anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        if reason == None and member != None:
            await ctx.send(f"{ctx.author.mention}, you must provide a reason in order to kick {member}")
        
        elif reason != None and member!= None:
            await member.kick(reason=reason)
            embed = nextcord.Embed(
                title = f"**User {member} has been kicked for {reason}**",
                colour = yellow
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = nextcord.Embed(
                    title = f"**User {member} has been kicked for {reason}**",
                    colour = yellow
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)

    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `kick members` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `kick members` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
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
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, member: nextcord.Member=None, *, reason=None):
        log = self.bot.get_channel(log_channel_id)

        if member == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't kick anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        if reason == None and member != None:
            await ctx.send(f"{ctx.author.mention}, you must provide a reason in order to ban {member}")

        elif reason != None and member != None:
            await member.ban(reason=reason)
            embed = nextcord.Embed(
                title = f"**User {member} has been banned for {reason}**",
                colour = nextcord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = nextcord.Embed(
                    title = f"**User {member} has been banned for {reason}**",
                    colour = nextcord.Colour.red()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `ban members` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `ban members` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
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
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: nextcord.Member=None, *, reason=None):
        log = self.bot.get_channel(log_channel_id)

        if member == None:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't kick anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        if reason == None and member != None:
            await member.ban(reason=reason)
            await member.unban()
            embed = nextcord.Embed(
                title = f"**User {member} has been soft-banned with no given reason**",
                colour = nextcord.Colour.orange()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = nextcord.Embed(
                    title = f"**User {member} has been soft-banned with no given reason**",
                    colour = nextcord.Colour.orange()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)

        elif reason != None and member != None:
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

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = nextcord.Embed(
                    title = f"**User {member} has been soft-banned for {reason}**",
                    colour = nextcord.Colour.orange()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @softban.error
    async def softban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `ban members` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `ban members` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
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
                description = f"• An error occured, try running `$help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        channel = ctx.channel

        if ctx.message.guild.id != 889027208964874240:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Not Available!",
                description = f"• This command is only available for the admins in the official bot help server."
            )

            await ctx.send(embed=embed)

        if reason == None and ctx.message.guild.id == 889027208964874240:
            role = nextcord.utils.get(ctx.guild.roles, name="@everyone")
            await channel.set_permissions(role, send_messages=False)
            embed = nextcord.Embed(
                title = f"**Channel `{channel.name}` has been locked**",
                description = f"No given reason",
                colour = nextcord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/locked_1f512.png")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = nextcord.Embed(
                    title = f"**Channel `{channel.name}` has been locked**",
                    description = f"No given reason",
                    colour = nextcord.Colour.magenta()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url=ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)

        if reason != None and ctx.message.guild.id == 889027208964874240:
            role = nextcord.utils.get(ctx.guild.roles, name="@everyone")
            await channel.set_permissions(role, send_messages=False)
            embed = nextcord.Embed(
                title = f"**Channel `{channel.name}` has been locked**",
                description = f"Reason: {reason}",
                colour = nextcord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/locked_1f512.png")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = nextcord.Embed(
                    title = f"**Channel `{channel.name}` has been locked**",
                    description = f"Reason: {reason}",
                    colour = nextcord.Colour.magenta()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url=ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
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
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        channel = ctx.channel

        if ctx.message.guild.id != 889027208964874240:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Not Available!",
                description = f"• This command is only available for the admins in the official bot help server."
            )

            await ctx.send(embed=embed)

        if reason == None and ctx.message.guild.id == 889027208964874240:
            role = nextcord.utils.get(ctx.guild.roles, name="@everyone")
            await channel.set_permissions(role, send_messages=True)
            embed = nextcord.Embed(
                title = f"**Channel `{channel.name}` has been unlocked**",
                description = f"No given reason",
                colour = nextcord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/locked_1f512.png")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = nextcord.Embed(
                    title = f"**Channel `{channel.name}` has been unlocked**",
                    description = f"No given reason",
                    colour = nextcord.Colour.magenta()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url=ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)

        if reason != None and ctx.message.guild.id == 889027208964874240:
            role = nextcord.utils.get(ctx.guild.roles, name="@everyone")
            await channel.set_permissions(role, send_messages=True)
            embed = nextcord.Embed(
                title = f"**Channel `{channel.name}` has been unlocked**",
                description = f"Reason: {reason}",
                colour = nextcord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/locked_1f512.png")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = nextcord.Embed(
                    title = f"**Channel `{channel.name}` has been unlocked**",
                    description = f"Reason: {reason}",
                    colour = nextcord.Colour.magenta()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url=ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
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


def setup(bot):
    bot.add_cog(Moderation(bot))
