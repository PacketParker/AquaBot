import nextcord
from nextcord import voice_client
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request
import asyncio
import nacl
import random

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff

class MemberHas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id == 734858944689864816:
            outcomeJoin = random.randint(1, 4)
            outcome = random.randint(1, 3)

            if before.channel is None and after.channel and member.id != self.bot.user.id:
                try:
                    if outcomeJoin == 1:
                        voice_channel = after.channel
                        vc = await voice_channel.connect()
                        vc.play(nextcord.FFmpegPCMAudio('utils/connect/connected1.mp3'))
                        while vc.is_playing():
                            await asyncio.sleep(0.1)
                        await vc.disconnect()

                    if outcomeJoin == 2:
                        voice_channel = after.channel
                        vc = await voice_channel.connect()
                        vc.play(nextcord.FFmpegPCMAudio('utils/connect/connected2.wav'))
                        while vc.is_playing():
                            await asyncio.sleep(0.1)
                        await vc.disconnect()

                    if outcomeJoin == 3:
                        voice_channel = after.channel
                        vc = await voice_channel.connect()
                        vc.play(nextcord.FFmpegPCMAudio('utils/connect/connected3.wav'))
                        while vc.is_playing():
                            await asyncio.sleep(0.1)
                        await vc.disconnect()  

                    if outcomeJoin == 4:
                        voice_channel = after.channel
                        vc = await voice_channel.connect()
                        vc.play(nextcord.FFmpegPCMAudio('utils/connect/connected4.mp3'))
                        while vc.is_playing():
                            await asyncio.sleep(0.1)
                        await vc.disconnect()
                except:
                    pass

            elif after.channel is None and before.channel and member.id != self.bot.user.id:
                try:
                    if outcome == 1:
                        voice_channel = before.channel
                        vc = await voice_channel.connect()
                        vc.play(nextcord.FFmpegPCMAudio('utils/disconnect/disconnected1.mp3'))
                        while vc.is_playing():
                            await asyncio.sleep(0.1)
                        await vc.disconnect()

                    if outcome == 2:
                        voice_channel = before.channel
                        vc = await voice_channel.connect()
                        vc.play(nextcord.FFmpegPCMAudio('utils/disconnect/disconnected2.mp3'))
                        while vc.is_playing():
                            await asyncio.sleep(0.1)
                        await vc.disconnect()

                    if outcome == 3:
                        voice_channel = before.channel
                        vc = await voice_channel.connect()
                        vc.play(nextcord.FFmpegPCMAudio('utils/disconnect/disconnected3.wav'))
                        while vc.is_playing():
                            await asyncio.sleep(0.1)
                        await vc.disconnect()

                except:
                    pass


def setup(bot):
    bot.add_cog(MemberHas(bot))