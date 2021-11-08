import nextcord
from nextcord.ext import commands
import os
from utils.helpers import *
import aiosqlite
import asyncio

log_channel_id = 889293946801516554
intents = nextcord.Intents.default()
intents.members = True

async def initialise():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect("database/data.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS level_channel (guild_id int, channel_id int, PRIMARY KEY (guild_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS mute (guild_id int, role_id int, PRIMARY KEY (guild_id, role_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS join_channel (guild_id int, channel_id int, PRIMARY KEY (guild_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS warnings (warn_id int, guild_id int, user_id int, warning, warn_time, warned_by, PRIMARY KEY (warn_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS prefix (guild_id, prefix, PRIMARY KEY (guild_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER NOT NULL PRIMARY KEY, money INTEGER NOT NULL DEFAULT 0)")

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


bot = commands.Bot(
    command_prefix=get_prefix,
    owner_ids=OWNER_IDS,
    intents=intents
)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity = nextcord.Game(f"Ping Me For Help!"))
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}') 

    for filename in os.listdir('./cogs/economy'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.economy.{filename[:-3]}') 

bot.remove_command('help')
bot.loop.create_task(initialise())
bot.run("ODk1ODEyMDk2NDU2MDExNzg2.YV-ABw.JnHalLuRzYdjXodKmjCKHbdTLSk")
asyncio.run(bot.db.close())