import nextcord
from nextcord.ext import commands, tasks
import os
from utils.helpers import *
import aiosqlite
import asyncio
import math

log_channel_id = 889293946801516554
intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=PREFIX,
    owner_ids=OWNER_IDS,
    intents=intents
)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to nextcord!')
    await bot.change_presence(activity = nextcord.Game("$help"))
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}') 

async def initialise():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect("database/data.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS level_channel (guild_id int, channel_id int, PRIMARY KEY (guild_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS mute (guild_id int, role_id int, PRIMARY KEY (guild_id, role_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS join_message (guild_id int, channel_id int, PRIMARY KEY (guild_id))")


bot.remove_command('help')
bot.loop.create_task(initialise())
bot.run("ODk1ODEyMDk2NDU2MDExNzg2.YV-ABw.JnHalLuRzYdjXodKmjCKHbdTLSk")
asyncio.run(bot.db.close())

