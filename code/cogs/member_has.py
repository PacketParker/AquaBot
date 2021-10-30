import nextcord
from nextcord import voice_client
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request
import asyncio
import nacl

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

def setup(bot):
    bot.add_cog(MemberHas(bot))