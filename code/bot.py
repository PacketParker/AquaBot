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

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix=get_prefix,
        activity = discord.Game(name="Ping Me For Help!"),
        intents = discord.Intents.defa
        )

    async def setup_hook(self):
        self.loop.create_task(initialise())
        for ext in os.listdir('./code/cogs'):
            if ext.endswith('.py'):
                await self.load_extension(f'cogs.{ext[:-3]}')

bot = MyBot()
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

if __name__ == '__main__':
    bot.run(TOKEN)
    asyncio.run(bot.db.close())