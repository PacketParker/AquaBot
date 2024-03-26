import re
import discord
import lavalink
from discord.ext import commands
import math
import requests
import datetime
from discord import app_commands
from custom_source import CustomSource
from reader import BOT_COLOR

url_rx = re.compile(r'https?://(?:www\.)?.+')

class LavalinkVoiceClient(discord.VoiceClient):
    """
    This is the preferred way to handle external voice sending
    This client will be created via a cls in the connect method of the channel
    see the following documentation:
    https://discordpy.readthedocs.io/en/latest/api.html#voiceprotocol
    """

    def __init__(self, client: commands.Bot, channel: discord.abc.Connectable):
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
                'default-node'
            )
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

    async def connect(self, *, timeout: float, reconnect: bool, self_deaf: bool = True, self_mute: bool = False) -> None:
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel, self_mute=self_mute, self_deaf=self_deaf)

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
            bot.lavalink.add_node(
                '127.0.0.1',
                2333,
                'youshallnotpass',
                'us-central',
                'default-node'
            )  # Host, Port, Password, Region, Name

        self.lavalink: lavalink.Client = bot.lavalink
        self.lavalink.add_event_hooks(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.lavalink._event_hooks.clear()

    async def ensure_before(self, interaction):
        """ Command before-invoke handler. """
        guild_check = interaction.guild is not None

        if guild_check:
            await self.ensure_voice(interaction)

        return guild_check

    async def ensure_voice(self, interaction: discord.Interaction):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.lavalink.player_manager.create(interaction.guild.id)
        should_connect = interaction.command.name in ('play',)

        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message('Join a voicechannel first.', ephemeral=True)
            raise ZeroDivisionError

        if not player.is_connected:
            if not should_connect:
                await interaction.response.send_message('Not connected.', ephemeral=True)
                raise ZeroDivisionError

            permissions = interaction.user.voice.channel.permissions_for(interaction.user)

            if not permissions.connect or not permissions.speak:
                await interaction.response.send_message('I need the `CONNECT` and `SPEAK` permissions.', ephemeral=True)
                raise ZeroDivisionError

            player.store('channel', interaction.channel.id)
            await interaction.user.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if int(player.channel_id) != interaction.user.voice.channel.id:
                await interaction.response.send_message('You need to be in my voicechannel.', ephemeral=True)
                raise ZeroDivisionError

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = event.player.guild_id
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and member == self.bot.user:
            if after.channel is None:
                    player = self.lavalink.player_manager.get(member.guild.id)
                    player.queue.clear()
                    await player.stop()
                    guild = member.guild
                    try:
                        await guild.voice_client.disconnect(force=True)
                        player.shuffle = not player.shuffle if player.shuffle else player.shuffle
                    except AttributeError:
                        pass


    @app_commands.command()
    @app_commands.describe(name="Name or link of song")
    async def play(
        self,
        interaction: discord.Interaction,
        name: str
    ):
        "Play a song from your favorite music provider"
        await self.ensure_before(interaction)
        player = self.lavalink.player_manager.get(interaction.guild.id)
        query = name

        # Below begins the start of the search for Spotify links - we must check for playlist, albums, and tracks
        # We use a custom source in order to provide us with the correct information and streams
        if "open.spotify.com/playlist" in query:
            playlist_id = query.split("playlist/")[1].split("?si=")[0]
            playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
            headers = {"Authorization": f"Bearer {self.bot.access_token}"}
            response = requests.get(playlist_url, headers=headers)
            if response.status_code == 200:
                playlist = response.json()

                embed = discord.Embed(
                    title = "Playlist Queued",
                    description = f"**{playlist['name']}** from **{playlist['owner']['display_name']}**\n` {len(playlist['tracks']['items'])} ` tracks\n\nQueued by: {interaction.user.mention}",
                    color=BOT_COLOR
                )
                embed.set_thumbnail(url=playlist['images'][0]['url'])
                embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
                await interaction.response.send_message(embed=embed)

                tracks = await CustomSource.load_playlist(self, interaction.user, playlist)
                for track in tracks['tracks']:
                    player.add(requester=interaction.user, track=track)

        if "open.spotify.com/album" in query:
            album_id = query.split("album/")[1]
            album_url = f"https://api.spotify.com/v1/albums/{album_id}"
            headers = {"Authorization": f"Bearer {self.bot.access_token}"}
            response = requests.get(album_url, headers=headers)
            if response.status_code == 200:
                album = response.json()

                embed = discord.Embed(
                    title = "Album Queued",
                    description = f"**{album['name']}** by **{album['artists'][0]['name']}**\n` {len(album['tracks']['items'])} ` tracks\n\nQueued by: {interaction.user.mention}",
                    color=BOT_COLOR
                )
                embed.set_thumbnail(url=album['images'][0]['url'])
                embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
                await interaction.response.send_message(embed=embed)

                tracks = await CustomSource.load_album(self, interaction.user, album)
                for track in tracks['tracks']:
                    player.add(requester=interaction.user, track=track)

        if "open.spotify.com/track" in query:
            track_id = query.split("track/")[1]
            track_url = f"https://api.spotify.com/v1/tracks/{track_id}"
            headers = {"Authorization": f"Bearer {self.bot.access_token}"}
            response = requests.get(track_url, headers=headers)
            if response.status_code == 200:
                track = response.json()

                embed = discord.Embed(
                    title = "Track Queued",
                    description = f"**{track['name']}** by **{track['artists'][0]['name']}**\n\nQueued by: {interaction.user.mention}",
                    color=BOT_COLOR
                )
                embed.set_thumbnail(url=track['album']['images'][0]['url'])
                embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
                await interaction.response.send_message(embed=embed)

                track_ = await CustomSource.load_item(self, interaction.user, track)
                player.add(requester=interaction.user, track=track_.tracks[0])

        if 'open.spotify.com/artists' in query:
            return await interaction.response.send_message("Sorry, I can't play artists. You must provide a song/album/playlist.", ephemeral=True)

        if 'open.spotify.com' in query:
            if not player.is_playing:
                await player.play()
            return

        # Now begins the soundcloud section, this can be just like the youtube section
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)

        # Below is for YouTube search, which is the default and is used when no link is provided
        if not url_rx.match(query) and not results or not results['tracks']:
            query = f'scsearch:{query}'
        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await interaction.response.send_message('Nothing found!', ephemeral=True)

        embed = discord.Embed(color=BOT_COLOR)

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                track_ = lavalink.AudioTrack(track, interaction.user.id, extra=f"https://img.youtube.com/vi/{track['info']['identifier']}/hqdefault.jpg")
                player.add(requester=interaction.user, track=track_)

            embed.title = 'Playlist Queued!'
            embed.description = f"**{results['playlistInfo']['name']}**\n` {len(tracks)} ` tracks\n\nQueued by: {interaction.user.mention}"
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        else:
            track = results['tracks'][0]
            embed.title = 'Track Queued'
            embed.description = f"**{track['info']['title']}** by **{track['info']['author']}**\n\nQueued by: {interaction.user.mention}"
            embed.set_thumbnail(url=f"https://img.youtube.com/vi/{track['info']['identifier']}/hqdefault.jpg")
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")

            track_ = lavalink.AudioTrack(track, interaction.user.id, recommended=True, extra=f"https://img.youtube.com/vi/{track['info']['identifier']}/hqdefault.jpg")
            player.add(requester=interaction.user, track=track_)

        await interaction.response.send_message(embed=embed)

        # We don't want to call .play() if the player is playing as that will
        # effectively skip the current track
        if not player.is_playing:
            await player.play()


    @app_commands.command()
    async def stop(
        self,
        interaction: discord.Interaction
    ):
        "Disconnects the bot from the voice channel and clears the queue"
        await self.ensure_before(interaction)

        player = self.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_connected:
            embed = discord.Embed(
                title="No Channel",
                description="I am not currently connected to any voice channel.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        player.queue.clear()
        await player.stop()
        player.shuffle = not player.shuffle if player.shuffle else player.shuffle
        guild = interaction.guild
        await guild.voice_client.disconnect(force=True)
        embed = discord.Embed(
            title="Queue Cleared and Music Stopped",
            description=f"Thank you for using Aqua Bot :wave:\n\nIssued by: {interaction.user.mention}",
            color=BOT_COLOR
        )
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def clear(
        self,
        interaction: discord.Interaction
    ):
        "Clear the current queue of songs"
        await self.ensure_before(interaction)

        player = self.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_connected:
            embed = discord.Embed(
                title="No Channel",
                description="I am not currently connected to any voice channel.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        player.queue.clear()
        embed = discord.Embed(
            title="Queue Cleared",
            description = f"The queue has been cleared of all songs!\n\nIssued by: {interaction.user.mention}",
            color=0x0088a9
        )
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def skip(
        self,
        interaction: discord.Interaction
    ):
        "Skips the song that is currently playing"
        await self.ensure_before(interaction)

        player = self.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                title="Nothing Playing",
                description="Nothing is currently playing, so I can't skip anything.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await player.skip()
        if not player.is_playing:
            embed = discord.Embed(
                title="Track Skipped",
                description=f"The queue is now empty, so I have left the voice channel. Thank you for using Aqua Bot.\n\nIssued by: {interaction.user.mention}",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            return await interaction.response.send_message(embed=embed)

        embed = discord.Embed(
            title="Track Skipped",
            description = f"**Now Playing: [{player.current.title}]({player.current.uri})**\n\nQueued by: {player.current.requester.mention}",
            color=BOT_COLOR
        )
        embed.set_thumbnail(url=player.current.extra['extra'])
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def pause(
        self,
        interaction: discord.Interaction
    ):
        "Pauses the song that is currently playing"
        await self.ensure_before(interaction)

        player = self.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                title="Nothing Playing",
                description="Nothing is currently playing, so I can't pause anything.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await player.set_pause(pause=True)
        embed = discord.Embed(
            title = f"Music Now Paused ⏸️",
            description = f"**[{player.current.title}]({player.current.uri})**\n\nQueued by: {player.current.requester.mention}",
            color=BOT_COLOR
        )
        embed.set_thumbnail(url=player.current.extra['extra'])
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def resume(
        self,
        interaction: discord.Interaction
    ):
        "Resumes the paused song"
        await self.ensure_before(interaction)

        player = self.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                title="Nothing Paused",
                description="Nothing is currently paused, so I can't resume anything.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await player.set_pause(pause=False)
        embed = discord.Embed(
            title=f"Music Now Resumed ⏯️",
            description=f"**[{player.current.title}]({player.current.uri})**\n\nQueued by: {player.current.requester.mention}",
            color=BOT_COLOR
        )
        embed.set_thumbnail(url=player.current.extra['extra'])
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    @app_commands.describe(page="Queue page number - leave blank if you are unsure")
    async def queue(
        self,
        interaction: discord.Interaction,
        page: int = 1
    ):
        "See the current queue of songs"
        await self.ensure_before(interaction)

        player = self.lavalink.player_manager.get(interaction.guild.id)

        if not player.queue:
            embed = discord.Embed(
                title="Nothing Queued",
                description="Nothing is currently in the queue, add a song with the `/play` command.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            # Change ms duration to hour, min, sec in the format of 00:00:00
            track_duration = lavalink.utils.format_time(track.duration)
            # If the track is less than an hour, remove the hour from the duration
            if track_duration.split(':')[0] == '00':
                track_duration = track_duration[3:]

            queue_list += f"`{index+1}. ` [{track.title}]({track.uri}) - {track.author} `({track_duration})`\n"

        embed = discord.Embed(
            title=f"Queue for {interaction.guild.name}",
            description=f'**{len(player.queue)} tracks total**\n\n{queue_list}',
            color=BOT_COLOR
        )
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def np(
        self,
        interaction: discord.Interaction
    ):
        "Show what song is currently playing"
        await self.ensure_before(interaction)

        player = self.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                title="Nothing Playing",
                description="Nothing is currently playing, play a song with the `/play` command.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        time_in = str(datetime.timedelta(milliseconds=player.position))[:-7]
        total_duration = lavalink.utils.format_time(player.current.duration)
        # If total_duration has no hours, then remove the hour part from both times
        if total_duration.split(":")[0] == "00":
            time_in = time_in[2:]
            total_duration = total_duration[3:]

        embed= discord.Embed(
            title="Now Playing 🎶",
            description=f"**[{player.current.title}]({player.current.uri})**\n{f'` {time_in}/{total_duration} `'}\n\nQueued by: {player.current.requester.mention}",
            color=BOT_COLOR
        )
        embed.set_thumbnail(url=player.current.extra['extra'])
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    @app_commands.describe(number='Song number to have removed')
    async def remove(
        self,
        interaction: discord.Interaction,
        number: int
    ):
        "Removes the specified song from the queue"
        await self.ensure_before(interaction)

        player = self.lavalink.player_manager.get(interaction.guild.id)

        if not player.queue:
            embed = discord.Embed(
                title="Nothing Queued",
                description="Nothing is currently in the queue, so there is nothing for me to remove.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            return await interaction.response.send_message(embed=embed)

        if number > len(player.queue) or number < 1:
            return await interaction.response.send_message('The number entered is not a number within the queue - please try again!', ephemeral=True)

        index = number - 1
        removed_title = player.queue[index].title
        removed_url = player.queue[index].uri
        player.queue.pop(index)

        embed = discord.Embed(
            title="Song Removed from Queue",
            description=f"**Song Removed - [{removed_title}]({removed_url})**\n\nIssued by: {interaction.user.mention}",
            color=BOT_COLOR
        )
        embed.set_thumbnail(url=player.current.extra['extra'])
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def shuffle(
        self,
        interaction: discord.Interaction
    ):
        "Plays the songs in the queue in a randomized order, until turned off"
        await self.ensure_before(interaction)

        player = self.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                title="Nothing Playing",
                description="Nothing is currently playing, therefore I cannot shuffle the music.",
                color=BOT_COLOR
            )
            embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        player.shuffle = not player.shuffle

        embed = discord.Embed(
            title=f"{'Shuffle Enabled 🔀' if player.shuffle else 'Shuffle Disabled 🔀'}",
            description=f"{'All music will now be shuffled.' if player.shuffle else 'Music will no longer be shuffled.'}",
            color=BOT_COLOR
        )
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))