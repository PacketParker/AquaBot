import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.utils import get

log_channel_id = 889293946801516554

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)

        embed = discord.Embed(
            title = f"**User {member} has been kicked for {reason}**",
            colour = discord.Colour.orange()
        )

        embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(text='Bot made by Fiji#3608')

        await ctx.send(embed=embed)
        await member.kick(reason=reason)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)

        embed = discord.Embed(
            title = f"**User {member} has been banned for {reason}**",
            colour = discord.Colour.red()
        )

        embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(text='Bot made by Fiji#3608')

        await ctx.send(embed=embed)
        await member.kick(reason=reason)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def deafen(self, ctx, member: discord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        voice_state = member.voice

        if member.voice is None:
            await ctx.send(f'{ctx.author.mention}, that member is not in a voice channel and therefore cannot be deafened.')

        else:
            embed = discord.Embed(
                title = f"**User {member} has been deafened for {reason}**",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Bot made by Fiji#3608')

            await ctx.send(embed=embed)
            await member.edit(deafen=True)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def undeafen(self, ctx, member: discord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        voice_state = member.voice

        if member.voice is None:
            await ctx.send(f'{ctx.author.mention}, that member is not in a voice channel and therefore cannot be undeafened.')

        else:
            embed = discord.Embed(
                title = f"**User {member} has been undeafened for {reason}**",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Bot made by Fiji#3608')

            await ctx.send(embed=embed)
            await member.edit(deafen=False)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        voice_state = member.voice

        if member.voice is None:
            await ctx.send(f'{ctx.author.mention}, that member is not in a voice channel and therefore cannot be muted.')

        else:
            embed = discord.Embed(
                title = f"**User {member} has been muted for {reason}**",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Bot made by Fiji#3608')

            await ctx.send(embed=embed)
            await member.edit(mute=True)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        voice_state = member.voice

        if member.voice is None:
            await ctx.send(f'{ctx.author.mention}, that member is not in a voice channel and therefore cannot be unmuted.')

        else:
            embed = discord.Embed(
                title = f"**User {member} has been unmuted for {reason}**",
                colour = discord.Colour.magenta()
            )

            embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_footer(text='Bot made by Fiji#3608')

            await ctx.send(embed=embed)
            await member.edit(mute=False)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel=None, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        channel = channel or ctx.channel

        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
        }
        await channel.edit(overwrites=overwrites)
        embed = discord.Embed(
            title = f"**Channel `{channel.name}` has been locked**",
            description = f"Reason: {reason}",
            colour = discord.Colour.magenta()
        )

        embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
        embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/locked_1f512.png")
        embed.set_footer(text='Bot made by Fiji#3608')

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel=None, *, reason=None):
        log = self.bot.get_channel(log_channel_id)
        channel = channel or ctx.channel

        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(send_messages=True)
        }
        await channel.edit(overwites=overwrites)
        embed = discord.Embed(
            title = f"**Channel `{channel.name}` has been unlocked**",
            description = f"Reason: {reason}",
            colour = discord.Colour.magenta()
        )
        embed.add_field(name=f'This command was issued by {ctx.author}', value = f'This has been logged to {log.mention}', inline=False)
        embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/unlocked_1f513.png")
        embed.set_footer(text='Bot made by Fiji#3608')

        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(moderation(bot))
