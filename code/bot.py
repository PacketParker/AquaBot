import discord
from discord.ext import commands
import os
import aiosqlite
import asyncio
from decimal import *
from reader import TOKEN, DEFAULT_PREFIX

async def initialise():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect("code/database/data.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS level_channel (guild_id int, channel_id int, PRIMARY KEY (guild_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS mute (guild_id int, role_id int, PRIMARY KEY (guild_id, role_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS join_channel (guild_id int, channel_id int, PRIMARY KEY (guild_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS warnings (warn_id int, guild_id int, user_id int, warning, warn_time, warned_by, PRIMARY KEY (warn_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS prefix (guild_id, prefix, PRIMARY KEY (guild_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER NOT NULL PRIMARY KEY, money INTEGER NOT NULL DEFAULT 0)")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS profile (user_id int, rank_name, rank_int int, UNIQUE (user_id, rank_name, rank_int))")

async def get_prefix(bot, message):
    if not message.guild:    
        prefix = DEFAULT_PREFIX
        return prefix
    else:
        try:
            async with bot.db.execute("SELECT prefix FROM prefix WHERE guild_id = ?", (message.guild.id,)) as cursor:
                data = await cursor.fetchone()
                if data:
                    prefix = data[0]
                else:
                    prefix = DEFAULT_PREFIX
                    
            if prefix == None and not data:
                prefix = DEFAULT_PREFIX
            
            return prefix
        except:
            prefix = DEFAULT_PREFIX
            return prefix

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix=get_prefix,
        status = discord.Game(f"Ping Me For Help!"),
        intents = intents
        )

    async def setup_hook(self):
        self.loop.create_task(initialise())
        for ext in os.listdir('./code/slash_commands'):
            if ext.endswith('.py'):
                await self.load_extension(f'slash_commands.{ext[:-3]}')


bot = MyBot()
bot.remove_command('help')

@bot.listen()
async def on_message(message):
    if not message.guild:
        return

    if message.author.bot is True:
        return

    prefix = await get_prefix(bot, message)
    command_list = {f'{prefix}add', f'{prefix}profile', f'{prefix}shop', f'{prefix}blackjack', f'{prefix}help',
    f'{prefix}slots', f'{prefix}coinflip', f'{prefix}money', f'{prefix}leaderboard', f'{prefix}warn', 
    f'{prefix}delwarn', f'{prefix}warnings', f'{prefix}mute', f'{prefix}tempmute', f'{prefix}unmute', 
    f'{prefix}purge', f'{prefix}kick', f'{prefix}ban', f'{prefix}softban', f'{prefix}contact', 
    f'{prefix}prices', f'{prefix}crypto', f'{prefix}covid', f'{prefix}invite', f'{prefix}track', 
    f'{prefix}serverinfo', f'{prefix}whois', f'{prefix}botinfo', f'{prefix}vote', f'{prefix}play', 
    f'{prefix}skip', f'{prefix}queue', f'{prefix}remove', f'{prefix}stop', f'{prefix}clear', 
    f'{prefix}repeat', f'{prefix}shuffle', f'{prefix}np', f'{prefix}pause', f'{prefix}resume', 
    f'{prefix}setlevel', f'{prefix}lvlreset', f'{prefix}dellevel', f'{prefix}new',
    f'{prefix}lvlchannel', f'{prefix}setmute', f'{prefix}delmute', f'{prefix}muterole', f'{prefix}setjoin', 
    f'{prefix}deljoin', f'{prefix}joinchannel', f'{prefix}level', f'{prefix}lvlboard', f'{prefix}ping',
    f'{prefix}q', f'{prefix}nowplaying', f'{prefix}cf'}

    setprefix = message.content.lower().startswith(f'{prefix}setprefix')
    if prefix is False:
        return
        
    if setprefix is True:
        embed = discord.Embed(
            title = f"Slash Command Update!",
            description = f"**Server prefix cannot be changed, as all command are restricted to ONLY the slash commands style, therefore no prefix is needed.**",
            colour = discord.Colour.blurple()    
        )
        await message.reply(embed=embed)


    output = any(message.content.lower().startswith(i) for i in command_list)
    if output is False:
        return
    
    elif output is True:
        embed = discord.Embed(
            title = f"All commands are now slash commands!",
            description = f"**Use `/help` in order to get help on what commands are available.**",
            colour = discord.Colour.blurple()    
        )
        await message.reply(embed=embed)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


bot.run(TOKEN)
asyncio.run(bot.db.close())