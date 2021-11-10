import re
import nextcord
import lavalink
from nextcord.ext import commands
import math

url_rx = re.compile(r'https?://(?:www\.)?.+')

class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""

class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""

class LavalinkVoiceClient(nextcord.VoiceClient):
    """
    This is the preferred way to handle external voice sending
    This client will be created via a cls in the connect method of the channel
    see the following documentation:
    https://discordpy.readthedocs.io/en/latest/api.html#voiceprotocol
    """

    def __init__(self, client: nextcord.Client, channel: nextcord.abc.Connectable):
        self.client = client
        self.channel = channel
        if hasattr(self.client, 'lavalink'):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(
                    '127.0.0.1',
                    2333,
                    'youshallnotpass',
                    'us-central',
                    'default-node')
            self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        lavalink_data = {
                't': 'VOICE_SERVER_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        lavalink_data = {
                't': 'VOICE_STATE_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool) -> None:
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel)

    async def disconnect(self, *, force: bool) -> None:
        player = self.lavalink.player_manager.get(self.channel.guild.id)
        if not force and not player.is_connected:
            return

        await self.channel.guild.change_voice_state(channel=None)
        player.channel_id = None
        self.cleanup()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(self.bot.user.id)
            bot.lavalink.add_node('127.0.0.1', 2333, 'youshallnotpass', 'us-central', 'default-node')  # Host, Port, Password, Region, Name

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Join a voicechannel first.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == self.bot.user.id and after.channel is None:
            guild = member.guild
            try:
                await guild.voice_client.disconnect(force=True)
            except:
                pass
            player = self.bot.lavalink.player_manager.get(member.guild.id)
            await player.stop()


    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = nextcord.Embed(color=nextcord.Color.green())

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks - [{ctx.author.mention}]'
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]}) - [{ctx.author.mention}]'

            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip the current track
        if not player.is_playing:
            await player.play()

        await ctx.guild.change_voice_state(channel = ctx.author.voice.channel, self_deaf=True)


    @commands.command()
    async def stop(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            embed = nextcord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=nextcord.Color.green()
            )
            return await ctx.send(embed=embed)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voicechannel!')

        player.queue.clear()
        await player.stop()
        await ctx.voice_client.disconnect(force=True)
        embed = nextcord.Embed(
            description = f"**Goodbye, thank you :wave: - [{ctx.author.mention}]**", 
            color=nextcord.Color.green()
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def clear(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            embed = nextcord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=nextcord.Color.green()
            )
            return await ctx.send(embed=embed)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voicechannel!')

        player.queue.clear()
        embed = nextcord.Embed(
            description = f"**Queue Cleared - [{ctx.author.mention}]**", 
            color=nextcord.Color.green()
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def skip(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if player.is_playing:
            await player.skip()
            embed = nextcord.Embed(
                description = f"**Track Skipped - [{ctx.author.mention}]**",
                colour = nextcord.Colour.green()
            )
            await ctx.send(embed=embed)

        if not player.is_playing:
            embed = nextcord.Embed(
                title="→ Nothing Playing", 
                description="• Nothing is currently playing, so I can't skip anything.", 
                color=nextcord.Color.green()
            )
            return await ctx.send(embed=embed)


    @commands.command()
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if player.is_playing:
            await player.set_pause(pause = True)
            embed = nextcord.Embed(
                description = f"**Pause ⏸️ - [{ctx.author.mention}]**",
                colour = nextcord.Colour.green()
            )
            await ctx.send(embed=embed)

        if not player.is_playing:
            embed = nextcord.Embed(
                title="→ Nothing Playing", 
                description="• Nothing is currently playing, so I can't pause anything.", 
                color=nextcord.Color.green()
            )
            return await ctx.send(embed=embed)


    @commands.command()
    async def resume(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if player.is_playing:
            await player.set_pause(pause = False)
            embed = nextcord.Embed(
                description = f"**Resuming ⏯️ - [{ctx.author.mention}]**",
                colour = nextcord.Colour.green()
            )
            await ctx.send(embed=embed)

        if not player.is_playing:
            embed = nextcord.Embed(
                title="→ Nothing Paused", 
                description="• Nothing is currently paused, so I can't resume anything.", 
                color=nextcord.Color.green()
            )
            return await ctx.send(embed=embed)


    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int = 1):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.queue:
            embed = nextcord.Embed(
                title="→ Nothing Queued", 
                description="• Nothing is currently in the queue.", 
                color=nextcord.Color.green()
            )
            return await ctx.send(embed=embed)

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = nextcord.Embed(
            colour=nextcord.Color.green(),
            description=f'**{len(player.queue)} tracks**\n\n{queue_list}'
        )
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.send(embed=embed)


    @commands.command(name="np", aliases=['nowplaying'])
    async def now_playing(self,ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            embed = nextcord.Embed(
                title="→ Nothing Playing", 
                description="• Nothing is currently playing.", 
                color=nextcord.Color.green()
            )
            return await ctx.send(embed=embed)

        embed= nextcord.Embed(
            title = player.current.title,
            url = f"https://youtube.com/watch?v={player.current.identifier}",
            colour = nextcord.Colour.green()
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def remove(self, ctx, index: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.queue:
            embed = nextcord.Embed(
                title="→ Nothing Queued", 
                description="• Nothing is currently in the queue.", 
                color=nextcord.Color.green()
            )
            return await ctx.send(embed=embed)

        if index > len(player.queue) or index < 1:
            return await ctx.send('Index has to be >=1 and <=queue size')

        index = index - 1
        removed = player.queue.pop(index)

        embed = nextcord.Embed(
            description = 'Removed **' + removed.title + f'** from the queue - [{ctx.author.mention}]',
            colour = nextcord.Colour.green()
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            embed = nextcord.Embed(
                title="→ Nothing Playing", 
                description="• Nothing is currently playing.", 
                color=nextcord.Color.green()
            )
            return await ctx.send(embed=embed)

        player.shuffle = not player.shuffle

        embed = nextcord.Embed(
            description = '🔀 | Shuffle ' + ('enabled' if player.shuffle else 'disabled') + f' - [{ctx.author.mention}]',
            colour = nextcord.Colour.green()
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def repeat(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            embed = nextcord.Embed(
                title="→ Nothing Playing", 
                description="• Nothing is currently playing.", 
                color=nextcord.Color.green()
            )
            return await ctx.send(embed=embed)

        player.repeat = not player.repeat

        embed = nextcord.Embed(
            description = '🔁 | Repeat ' + ('enabled' if player.repeat else 'disabled') + f' - [{ctx.author.mention}]',
            colour = nextcord.Colour.green()
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))