import nextcord
from nextcord import voice_client
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request
import asyncio
import nacl
from datetime import datetime

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff

class MemberHas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id == 734858944689864816:
            message = self.bot.get_channel(840658771893682176)

            if before.channel is None and after.channel and member.id != self.bot.user.id:
                await message.send("MEMBER HAS JOINED")
                voice_channel = after.channel
                vc = await voice_channel.connect()
                vc.play(nextcord.FFmpegPCMAudio('connect.mp3'))
                while vc.is_playing():
                    await asyncio.sleep(3)
                await vc.disconnect()

            elif after.channel is None and before.channel and member.id != self.bot.user.id:
                await message.send("MEMBER HAS LEFT")
                voice_channel = before.channel
                vc = await voice_channel.connect()
                vc.play(nextcord.FFmpegPCMAudio('disconnect.mp3'))
                while vc.is_playing():
                    await asyncio.sleep(3)
                await vc.disconnect()


    @commands.Cog.listener()
    async def on_error(self, ctx, error):
        if isinstance(error, nextcord.errors.ClientException):
            return

        if isinstance(error, (commands.MissingRequiredArgument, commands.TooManyArguments, commands.BadArgument)):
            embed = nextcord.Embed(
                title = "→ Incorrect Syntax!",
                description = f"• That is the incorrect way to send that command. In order to see how to use that command, use `{ctx.prefix}help {ctx.command.name}`",
                colour = color
            )
            await ctx.send(embed=embed)

        elif not commands.MissingRequiredArgument and not commands.TooManyArguments and not commands.BadArgument:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberHas(bot))