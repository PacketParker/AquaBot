import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.utils import get
import datetime
import json

timestamp=str(datetime.datetime.utcnow())
log_channel_id = 889293946801516554

yellow = 0xffc400

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        message = ctx.message

        if reason == None:
            await ctx.send(f"{ctx.author.mention}, you must provide a reason in order to kick {member}")
        
        elif reason != None:
            embed = discord.Embed(
                title = f"**User {member} has been kicked for {reason}**",
                colour = yellow
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)
            await member.kick(reason=reason)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        message = ctx.message

        if reason == None:
            await ctx.send(f"{ctx.author.mention}, you must provide a reason in order to ban {member}")

        elif reason != None:
            embed = discord.Embed(
                title = f"**User {member} has been banned for {reason}**",
                colour = discord.Colour.red()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)
            await member.kick(reason=reason)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        message = ctx.message

        if reason == None:
            embed = discord.Embed(
                title = f"**User {member} has been soft-banned with no given reason**",
                colour = discord.Colour.orange()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)
            await member.ban(reason=reason)
            await member.unban()

        elif reason != None:
            embed = discord.Embed(
                title = f"**User {member} has been soft-banned for {reason}**",
                colour = discord.Colour.orange()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)
            await member.kick(reason=reason)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def deafen(self, ctx, member: discord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        message = ctx.message

        if member.voice is None:
            await ctx.send(f'{ctx.author.mention}, that member is not in a voice channel and therefore cannot be deafened.')

        elif member.voice != None and reason == None:
            embed = discord.Embed(
                title = f"**User {member} has been deafened with no given reason.**",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)
            await member.edit(deafen=True)

        elif member.voice != None and reason != None:
            embed = discord.Embed(
                title = f"**User {member} has been deafened for {reason}**",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)
            await member.edit(deafen=True)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def undeafen(self, ctx, member: discord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        message = ctx.message

        if member.voice is None:
            await ctx.send(f'{ctx.author.mention}, that member is not in a voice channel and therefore cannot be undeafened.')

        elif member.voice != None and reason == None:
            embed = discord.Embed(
                title = f"**User {member} has been undeafened with no given reason**",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)
            await member.edit(deafen=False)

        elif member.voice != None and reason != None:
            embed = discord.Embed(
                title = f"**User {member} has been undeafened for {reason}**",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)
            await member.edit(deafen=False)


    #@commands.command()
    #@commands.has_permissions(kick_members=True)
    #async def mute(self, ctx, member: discord.Member, *, reason=None):
#Give user the muted role 


    #@commands.command()
    #@commands.has_permissions(kick_members=True)
    #async def unmute(self, ctx, member: discord.Member, *, reason=None):
#Takes muted role away from user


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel=None, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        channel = channel or ctx.channel
        message = ctx.message

        if reason == None:
            cuties = discord.utils.get(ctx.guild.roles, name="cuties")
            await channel.set_permissions(cuties, send_messages=False)
            shout_ping = discord.utils.get(ctx.guild.roles, name="shout ping")
            await channel.set_permissions(shout_ping, send_messages=False)
            nitro_ping = discord.utils.get(ctx.guild.roles, name="nitro ping")
            await channel.set_permissions(nitro_ping, send_messages=False)
            event_ping = discord.utils.get(ctx.guild.roles, name="event ping")
            await channel.set_permissions(event_ping, send_messages=False)
            embed = discord.Embed(
                title = f"**Channel `{channel.name}` has been locked**",
                description = f"No given reason",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/locked_1f512.png")
            embed.set_footer(text=f'Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)

        if reason != None:
            cuties = discord.utils.get(ctx.guild.roles, name="cuties")
            await channel.set_permissions(cuties, send_messages=False)
            shout_ping = discord.utils.get(ctx.guild.roles, name="shout ping")
            await channel.set_permissions(shout_ping, send_messages=False)
            nitro_ping = discord.utils.get(ctx.guild.roles, name="nitro ping")
            await channel.set_permissions(nitro_ping, send_messages=False)
            event_ping = discord.utils.get(ctx.guild.roles, name="event ping")
            await channel.set_permissions(event_ping, send_messages=False)
            embed = discord.Embed(
                title = f"**Channel `{channel.name}` has been locked**",
                description = f"Reason: {reason}",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/locked_1f512.png")
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel=None, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        channel = channel or ctx.channel
        message = ctx.message

        if reason == None:
            cuties = discord.utils.get(ctx.guild.roles, name="cuties")
            await channel.set_permissions(cuties, send_messages=True)
            shout_ping = discord.utils.get(ctx.guild.roles, name="shout ping")
            await channel.set_permissions(shout_ping, send_messages=True)
            nitro_ping = discord.utils.get(ctx.guild.roles, name="nitro ping")
            await channel.set_permissions(nitro_ping, send_messages=True)
            event_ping = discord.utils.get(ctx.guild.roles, name="event ping")
            await channel.set_permissions(event_ping, send_messages=True)
            embed = discord.Embed(
                title = f"**Channel `{channel.name}` has been unlocked**",
                description = f"No given reason",
                colour = discord.Colour.magenta()
            )
            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/unlocked_1f513.png")
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)

        if reason != None:
            cuties = discord.utils.get(ctx.guild.roles, name="cuties")
            await channel.set_permissions(cuties, send_messages=True)
            shout_ping = discord.utils.get(ctx.guild.roles, name="shout ping")
            await channel.set_permissions(shout_ping, send_messages=True)
            nitro_ping = discord.utils.get(ctx.guild.roles, name="nitro ping")
            await channel.set_permissions(nitro_ping, send_messages=True)
            event_ping = discord.utils.get(ctx.guild.roles, name="event ping")
            await channel.set_permissions(event_ping, send_messages=True)
            embed = discord.Embed(
                title = f"**Channel `{channel.name}` has been unlocked**",
                description = f"Reason: {reason}",
                colour = discord.Colour.magenta()
            )
            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/unlocked_1f513.png")
            embed.set_footer(text='Command issued at: ' + message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

            await ctx.send(embed=embed)





            ##HERE STARTS THE WARN COMMANDS



def setup(bot):
    bot.add_cog(moderation(bot))
