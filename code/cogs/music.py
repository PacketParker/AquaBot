import nextcord
from nextcord.ext import commands
import random
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
import youtube_dl
from youtube_dl import YoutubeDL

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""

class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""

class YTDLSource(nextcord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.duration = data.get('duration')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        embed = nextcord.Embed(title="", description=f"Queued [{data['title']}]({data['webpage_url']}) [{ctx.author.mention}]", color=nextcord.Color.green())
        await ctx.send(embed=embed)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(nextcord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(nextcord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            embed = nextcord.Embed(
                title="Now playing", 
                description=f"[{source.title}]({source.web_url}) [{source.requester.mention}]", 
                color=nextcord.Color.green())
            self.np = await self._channel.send(embed=embed)
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except nextcord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel. '
                           'Please make sure you are in a valid channel or provide me with one')

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player


    @commands.command(name='join')
    async def connect_(self, ctx, *, channel: nextcord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                embed = nextcord.Embed(
                    title="→ Author Not In Channel", 
                    description="No channel to join. Please join a voice channel and try again.", 
                    color=nextcord.Color.green())
                await ctx.send(embed=embed)
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
        if (random.randint(0, 1) == 0):
            await ctx.message.add_reaction('👍')
        await ctx.send(f'**Joined `{channel}`**')
        await ctx.guild.change_voice_state(channel = ctx.author.voice.channel, self_deaf=True)


    @commands.command(name='play', aliases=['p'])
    async def play_(self, ctx, *, search: str):
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)
        await ctx.guild.change_voice_state(channel = ctx.author.voice.channel, self_deaf=True)


    @commands.command(name='pause')
    async def pause_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            embed = nextcord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=nextcord.Color.green())
            return await ctx.send(embed=embed)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send("Paused ⏸️")


    @commands.command(name='resume')
    async def resume_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = nextcord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=nextcord.Color.green())
            return await ctx.send(embed=embed)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send("Resuming ⏯️")


    @commands.command(name='skip', aliases = ['s'])
    async def skip_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = nextcord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=nextcord.Color.green())
            return await ctx.send(embed=embed)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
    

    @commands.command(name='remove')
    async def remove_(self, ctx, pos : int=None):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = nextcord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=nextcord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        if pos == None:
            player.queue._queue.pop()
        else:
            try:
                s = player.queue._queue[pos-1]
                del player.queue._queue[pos-1]
                embed = nextcord.Embed(
                    title="→ Song Removed", 
                    description=f"Removed [{s['title']}]({s['webpage_url']}) [{s['requester'].mention}]", 
                    color=nextcord.Color.green())
                await ctx.send(embed=embed)
            except:
                embed = nextcord.Embed(
                    title="→ No Track", 
                    description=f'• Could not find a track for "{pos}"', 
                    color=nextcord.Color.green())
                await ctx.send(embed=embed)
    

    @commands.command(name='clear')
    async def clear_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = nextcord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=nextcord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        player.queue._queue.clear()
        embed = nextcord.Embed(
            title="→ Cleared", 
            description="• I have cleared the songs in the queue", 
            color=nextcord.Color.green())
        await ctx.send(embed=embed)


    @commands.command(name='queue', aliases=['q'])
    async def queue_info(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = nextcord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=nextcord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        if player.queue.empty():
            embed = nextcord.Embed(
                title="→ Empty Queue", 
                description="• There is currently nothing in the queue", 
                color=nextcord.Color.green())
            return await ctx.send(embed=embed)

        seconds = vc.source.duration % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)

        # Grabs the songs in the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, int(len(player.queue._queue))))
        fmt = '\n'.join(f"`{(upcoming.index(_)) + 1}.` [{_['title']}]({_['webpage_url']}) | ` {duration} Requested by: {_['requester']}`\n" for _ in upcoming)
        fmt = f"\n__Now Playing__:\n[{vc.source.title}]({vc.source.web_url}) | ` {duration} Requested by: {vc.source.requester}`\n\n__Up Next:__\n" + fmt + f"\n**{len(upcoming)} songs in queue**"
        embed = nextcord.Embed(
            title=f'→ Queue for {ctx.guild.name}', 
            description=fmt, 
            color=nextcord.Color.green())
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)


    @commands.command(name='np', aliases=['current', 'playing'])
    async def now_playing_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = nextcord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=nextcord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        if not player.current:
            embed = nextcord.Embed(
                title="→ Nothing Playing", 
                description="• I am not currently playing anything", 
                color=nextcord.Color.green())
            return await ctx.send(embed=embed)
        
        seconds = vc.source.duration % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)

        embed = nextcord.Embed(
            title = f"→ Now Playing 🎶", 
            description = f"[{vc.source.title}]({vc.source.web_url}) [{vc.source.requester.mention}] | `{duration}`", 
            color = nextcord.Color.green())
        await ctx.send(embed=embed)


    @commands.command(name='volume')
    async def change_volume(self, ctx, *, vol: float=None):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = nextcord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=nextcord.Color.green())
            return await ctx.send(embed=embed)
        
        if not vol:
            embed = nextcord.Embed(
                title="→ Current Volume", 
                description=f"🔊 - The current volume is **{(vc.source.volume)*100}%**", 
                color=nextcord.Color.green())
            return await ctx.send(embed=embed)

        if not 0 < vol < 101:
            embed = nextcord.Embed(
                title = "→ Incorrect Number", 
                description = "• Please enter a value between 1 and 100", 
                color = nextcord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        embed = nextcord.Embed(
            title="→ New Volume", 
            description=f'**`{ctx.author}`** set the volume to **{vol}%**', 
            color=nextcord.Color.green())
        await ctx.send(embed=embed)


    @commands.command(name='stop')
    async def leave_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = nextcord.Embed(
                title = "→ No Channel", 
                description = "• I am not currently connected to any voice channel", 
                color = nextcord.Color.green())
            return await ctx.send(embed=embed)

        if (random.randint(0, 1) == 0):
            await ctx.message.add_reaction('👋')
        await ctx.send(f'**Successfully disconnected from {vc}**')

        await self.cleanup(ctx.guild)


def setup(bot):
    bot.add_cog(Music(bot))