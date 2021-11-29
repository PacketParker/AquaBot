import zlib
import discord

from discord.ext import commands


class SocketFix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self._zlib = zlib.decompressobj()
        self._buffer = bytearray()

    @commands.Cog.listener()
    async def on_socket_raw_receive(self, msg):
        if type(msg) is bytes:
            self._buffer.extend(msg)

            if len(msg) < 4 or msg[-4:] != b'\x00\x00\xff\xff':
                return

            try:
                msg = self._zlib.decompress(self._buffer)
            except Exception:
                self._buffer = bytearray()  # Reset buffer on fail just in case...
                return

            msg = msg.decode('utf-8')
            self._buffer = bytearray()

        msg = discord.utils._from_json(msg)
        self.bot.dispatch('on_socket_response', msg)


def setup(bot):
    bot.add_cog(SocketFix(bot))