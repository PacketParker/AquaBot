import discord
from discord.ext import commands
from datetime import datetime

from discord.ext.commands.errors import CommandInvokeError, MissingRequiredArgument

log_channel_id = 889293946801516554

yellow = 0xffc400
color = 0xc48aff

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, 
        ctx, 
        amount: int=commands.Option(description="Amount of messages to delete")
    ):
        "Delete the specified number of messages from the channel"
        log = self.bot.get_channel(log_channel_id)
        if amount == None:
            embed = discord.Embed(
                colour = color,
                title = "→ Amount Not Given!",
                description=f"• Please provide an amount of messages you would like to delete. Example: `{ctx.prefix}purge 5`"
            )
            await ctx.send(embed=embed, ephemeral=True)
    
        elif amount > 100:
            embed = discord.Embed(
                colour = color,
                title = "→ Amount Too Large!",
                description="• You sent an amount larger than 100. Sorry, but you can only delete 100 messages at a time."
            )
            await ctx.send(embed=embed, ephemeral=True)

        else:
            await ctx.channel.purge(limit=amount+1)
            await ctx.send("Messages Deleted", ephemeral=True)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = discord.Embed(
                    title = f"**{ctx.author} has run the purge command in {ctx.channel.name}**",
                    colour = yellow
                )
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await log.send(embed=embed)


    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage messages` permission."
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

        if isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage messages` permission. \nAsk an admin to fix this issue."
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
    @commands.has_permissions(kick_members=True)
    async def kick(self, 
        ctx, 
        member: discord.Member=commands.Option(description="Member you want to kick"), 
        reason: str=commands.Option(description="Reason for kicking the member")
    ):
        "Kick a member from your server"
        log = self.bot.get_channel(log_channel_id)

        if member == None:
            embed = discord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't kick anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if reason == None and member != None:
            await ctx.send(f"{ctx.author.mention}, you must provide a reason in order to kick {member}", ephemeral=True)
        
        elif reason != None and member!= None:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title = f"**User {member} has been kicked for {reason}**",
                colour = yellow
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = discord.Embed(
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
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `kick members` permission."
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

        if isinstance(error, CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You do not have the required permissions to kick the member."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `kick members` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = discord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
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
    @commands.has_permissions(kick_members=True)
    async def ban(self, 
        ctx, 
        member: discord.Member=commands.Option(description="Member you want to ban"), 
        reason: str=commands.Option(description="Reason you want to ban the member")
    ):
        "Ban a member from your server"
        log = self.bot.get_channel(log_channel_id)

        if member == None:
            embed = discord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't kick anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if reason == None and member != None:
            await ctx.send(f"{ctx.author.mention}, you must provide a reason in order to ban {member}", ephemeral=True)

        elif reason != None and member != None:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title = f"**User {member} has been banned for {reason}**",
                colour = discord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = discord.Embed(
                    title = f"**User {member} has been banned for {reason}**",
                    colour = discord.Colour.red()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `ban members` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)
        
        if isinstance(error, CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You do not have the required permissions to ban the member."
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
                description = "• I am missing `ban members` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = discord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
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
    @commands.has_permissions(ban_members=True)
    async def softban(self, 
        ctx, 
        member: discord.Member=commands.Option(description="Member you want to softban"), 
        reason: str=commands.Option(description="Reason you want to softban a member")
    ):
        "Ban and then immediately unban a member"
        log = self.bot.get_channel(log_channel_id)

        if member == None:
            embed = discord.Embed(
                colour = color,
                title = "→ Please provide a member!",
                description = f"• I can't kick anyone if a member is not provided."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if reason == None and member != None:
            await member.ban(reason=reason)
            await member.unban()
            embed = discord.Embed(
                title = f"**User {member} has been soft-banned with no given reason**",
                colour = discord.Colour.orange()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = discord.Embed(
                    title = f"**User {member} has been soft-banned with no given reason**",
                    colour = discord.Colour.orange()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)

        elif reason != None and member != None:
            await member.ban(reason=reason)
            await member.unban()
            embed = discord.Embed(
                title = f"**User {member} has been soft-banned for {reason}**",
                colour = discord.Colour.orange()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = discord.Embed(
                    title = f"**User {member} has been soft-banned for {reason}**",
                    colour = discord.Colour.orange()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url = ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @softban.error
    async def softban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `ban members` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You do not have the required permissions to softban the member."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `ban members` permission. \nAsk an admin to fix this issue."
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

        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = discord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
            )
            await ctx.send(embed=embed, ephemeral=True)

        elif not MissingRequiredArgument:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)


    @commands.command(slash_command_guilds = [891743644938297395])
    @commands.has_permissions(manage_channels=True)
    async def lock(self, 
        ctx, 
        reason: str=commands.Option(description="Reason for locking the channel")
    ):
        "Lock a channel so users can no longer send messages"
        log = self.bot.get_channel(log_channel_id)
        channel = ctx.channel

        if ctx.message.guild.id != 889027208964874240:
            embed = discord.Embed(
                colour = color,
                title = "→ Not Available!",
                description = f"• This command is only available for the admins in the official bot help server."
            )

            await ctx.send(embed=embed, ephemeral=True)

        if reason != None and ctx.message.guild.id == 889027208964874240:
            role = discord.utils.get(ctx.guild.roles, name="@everyone")
            await channel.set_permissions(role, send_messages=False)
            embed = discord.Embed(
                title = f"**Channel `{channel.name}` has been locked**",
                description = f"Reason: {reason}",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/locked_1f512.png")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = discord.Embed(
                    title = f"**Channel `{channel.name}` has been locked**",
                    description = f"Reason: {reason}",
                    colour = discord.Colour.magenta()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url=ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = discord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
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

        elif not MissingRequiredArgument:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)


    @commands.command(slash_command_guilds = [891743644938297395])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, 
        ctx, 
        reason: str=commands.Option(description="Reason for unlocking the channel")
    ):
        "Unlock a channel so users can send messages again"
        log = self.bot.get_channel(log_channel_id)
        channel = ctx.channel

        if ctx.message.guild.id != 889027208964874240:
            embed = discord.Embed(
                colour = color,
                title = "→ Not Available!",
                description = f"• This command is only available for the admins in the official bot help server."
            )

            await ctx.send(embed=embed, ephemeral=True)

        if reason != None and ctx.message.guild.id == 889027208964874240:
            role = discord.utils.get(ctx.guild.roles, name="@everyone")
            await channel.set_permissions(role, send_messages=True)
            embed = discord.Embed(
                title = f"**Channel `{channel.name}` has been unlocked**",
                description = f"Reason: {reason}",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/locked_1f512.png")
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

            if ctx.guild.id == 889027208964874240:
                log = self.bot.get_channel(log_channel_id)
                embed = discord.Embed(
                    title = f"**Channel `{channel.name}` has been unlocked**",
                    description = f"Reason: {reason}",
                    colour = discord.Colour.magenta()
                )

                embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
                embed.set_thumbnail(url=ctx.author.avatar.url)
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                await log.send(embed=embed)


    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, (commands.UserNotFound, commands.MemberNotFound)):
            embed = discord.Embed(
                colour = color,
                title = "→ Member Not Found!",
                description = f"• Member {error.argument} was not found."
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

        elif not MissingRequiredArgument:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Moderation(bot))
