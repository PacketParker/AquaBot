import discord
from discord.ext import commands
from datetime import datetime
from discord.ext.commands.errors import CommandInvokeError, MissingRequiredArgument

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

        if isinstance(error, commands.CommandInvokeError):
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

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'\u200b', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

    
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

        elif isinstance(error, commands.CommandInvokeError):
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

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'\u200b', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)


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

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Required Argument!",
                description = f"• {error}"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.CommandInvokeError):
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

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'\u200b', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)

        elif reason != None and member != None:
            await member.ban(reason=reason)
            await member.unban()
            embed = discord.Embed(
                title = f"**User {member} has been soft-banned for {reason}**",
                colour = discord.Colour.orange()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'\u200b', inline=False)
            embed.set_thumbnail(url = member.avatar.url)
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

            await ctx.send(embed=embed)


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

        elif isinstance(error, commands.CommandInvokeError):
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


def setup(bot):
    bot.add_cog(Moderation(bot))