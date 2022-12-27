import re
import discord
import lavalink
from discord.ext import commands
import math
from discord import app_commands

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
            bot.lavalink.add_node('127.0.0.1', 2333, 'youshallnotpass', 'us-central', 'default-node')  # Host, Port, Password, Region, Name

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def ensure_before(self, interaction):
        """ Command before-invoke handler. """
        guild_check = interaction.guild is not None

        if guild_check:
            await self.ensure_voice(interaction)

        return guild_check

    async def ensure_voice(self, interaction: discord.Interaction):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(interaction.guild.id)
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
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and member == self.bot.user:
            if after.channel is None:
                    player = self.bot.lavalink.player_manager.get(member.guild.id)
                    player.queue.clear()
                    await player.stop()
                    guild = member.guild
                    try:
                        await guild.voice_client.disconnect(force=True)
                    except AttributeError:
                        pass

        if before.channel is None and after.channel is not None:
            await member.edit(deafen=True)


    @app_commands.command()
    @app_commands.describe(name="Name or link of song")
    async def play(
        self, 
        interaction: discord.Interaction, 
        name: str
    ):
        "Play a song from your favorite music provider"
        await self.ensure_before(interaction)
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)
        query = name.strip('<>')

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            query = f'scsearch:{query}'

            results = await player.node.get_tracks(query)

            if not results or not results['tracks']:
                return await interaction.response.send_message('Nothing found!')

        embed = discord.Embed(color=discord.Color.green())

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=interaction.user.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks - [{interaction.user.mention}]'
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]}) - [{interaction.user.mention}]'

            track = lavalink.models.AudioTrack(track, interaction.user.id, recommended=True)
            player.add(requester=interaction.user.id, track=track)

        await interaction.response.send_message(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip the current track
        if not player.is_playing:
            await player.play()


    @app_commands.command()
    async def stop(
        self, 
        interaction: discord.Interaction
    ):
        "Disconnects the bot from the voice channel and clears the queue"
        await self.ensure_before(interaction)

        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_connected:
            embed = discord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        if not interaction.user.voice or (player.is_connected and interaction.user.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await interaction.response.send_message('You\'re not in my voicechannel!', ephemeral=True)

        player.queue.clear()
        await player.stop()
        guild = interaction.guild
        await guild.voice_client.disconnect(force=True)
        embed = discord.Embed(
            description = f"**Goodbye, thank you :wave: - [{interaction.user.mention}]**", 
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def clear(
        self, 
        interaction: discord.Interaction
    ):
        "Clear the current queue of songs"
        await self.ensure_before(interaction)

        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_connected:
            embed = discord.Embed(
                title="→ No Channel", 
                description="• I am not currently connected to any voice channel", 
                color=discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        if not interaction.user.voice or (player.is_connected and interaction.user.voice.channel.id != int(player.channel_id)):
            return await interaction.response.send_message('You\'re not in my voicechannel!', ephemeral=True)

        player.queue.clear()
        embed = discord.Embed(
            description = f"**Queue Cleared - [{interaction.user.mention}]**", 
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def skip(
        self, 
        interaction: discord.Interaction
    ):
        "Skips the song that is currently playing"
        await self.ensure_before(interaction)

        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if player.is_playing:
            await player.skip()
            embed = discord.Embed(
                description = f"**Track Skipped - [{interaction.user.mention}]**",
                colour = discord.Colour.green()
            )
            await interaction.response.send_message(embed=embed)

        if not player.is_playing:
            embed = discord.Embed(
                title="→ Nothing Playing", 
                description="• Nothing is currently playing, so I can't skip anything.", 
                color=discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command()
    async def pause(
        self,
        interaction: discord.Interaction    
    ):
        "Pauses the song that is currently playing"
        await self.ensure_before(interaction)

        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if player.is_playing:
            await player.set_pause(pause = True)
            embed = discord.Embed(
                description = f"**Pause ⏸️ - [{interaction.user.mention}]**",
                colour = discord.Colour.green()
            )
            await interaction.response.send_message(embed=embed)

        if not player.is_playing:
            embed = discord.Embed(
                title="→ Nothing Playing", 
                description="• Nothing is currently playing, so I can't pause anything.", 
                color=discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command()
    async def resume(
        self, 
        interaction: discord.Interaction
    ):
        "Resumes the paused song"
        await self.ensure_before(interaction)

        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if player.is_playing:
            await player.set_pause(pause = False)
            embed = discord.Embed(
                description = f"**Resuming ⏯️ - [{interaction.user.mention}]**",
                colour = discord.Colour.green()
            )
            await interaction.response.send_message(embed=embed)

        if not player.is_playing:
            embed = discord.Embed(
                title="→ Nothing Paused", 
                description="• Nothing is currently paused, so I can't resume anything.", 
                color=discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command()
    @app_commands.describe(page="Queue page number - leave blank if you are unsure")
    async def queue(
        self, 
        interaction: discord.Interaction, 
        page: int = 1
    ):
        "See the current queue of songs"
        await self.ensure_before(interaction)

        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if not player.queue:
            embed = discord.Embed(
                title="→ Nothing Queued", 
                description="• Nothing is currently in the queue.", 
                color=discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(
            colour=discord.Color.green(),
            description=f'**{len(player.queue)} tracks**\n\n{queue_list}'
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

        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                title="→ Nothing Playing", 
                description="• Nothing is currently playing.", 
                color=discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        embed= discord.Embed(
            title = player.current.title,
            url = f"https://youtube.com/watch?v={player.current.identifier}",
            colour = discord.Colour.green()
        )
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

        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if not player.queue:
            embed = discord.Embed(
                title="→ Nothing Queued", 
                description="• Nothing is currently in the queue.", 
                color=discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed)

        if number > len(player.queue) or number < 1:
            return await interaction.response.send_message('Index has to be >=1 and <=queue size', ephemeral=True)

        index = number - 1
        removed = player.queue.pop(index)

        embed = discord.Embed(
            description = 'Removed **' + removed.title + f'** from the queue - [{interaction.user.mention}]',
            colour = discord.Colour.green()
        )
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def shuffle(
        self, 
        interaction: discord.Interaction
    ):
        "Plays the songs in the queue in a randomized order, until turned off"
        await self.ensure_before(interaction)

        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                title="→ Nothing Playing", 
                description="• Nothing is currently playing.", 
                color=discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        player.shuffle = not player.shuffle

        embed = discord.Embed(
            description = '🔀 | Shuffle ' + ('enabled' if player.shuffle else 'disabled') + f' - [{interaction.user.mention}]',
            colour = discord.Colour.green()
        )
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def repeat(
        self, 
        interaction: discord.Interaction
    ):
        "Repeats the song that is currently played, until turned off"
        await self.ensure_before(interaction)

        player = self.bot.lavalink.player_manager.get(interaction.guild.id)

        if not player.is_playing:
            embed = discord.Embed(
                title="→ Nothing Playing", 
                description="• Nothing is currently playing.", 
                color=discord.Color.green()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        player.repeat = not player.repeat

        embed = discord.Embed(
            description = '🔁 | Repeat ' + ('enabled' if player.repeat else 'disabled') + f' - [{interaction.user.mention}]',
            colour = discord.Colour.green()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))
