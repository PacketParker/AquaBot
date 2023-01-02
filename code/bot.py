import discord
from discord.ext import commands, tasks
import os
import psycopg2
from decimal import *
import aiosqlite
from reader import TOKEN, CONNECTION_STRING, CLIENT_ID, CLIENT_SECRET
import requests

CONNECTION = psycopg2.connect(CONNECTION_STRING)

async def initialise():
    cur = CONNECTION.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id BIGINT, user_id BIGINT, exp BIGINT, PRIMARY KEY (guild_id, user_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS mute (guild_id BIGINT, role_id BIGINT, PRIMARY KEY (guild_id, role_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS tempmute (guild_id BIGINT, user_id BIGINT, role_id BIGINT, time TIMESTAMP, PRIMARY KEY (guild_id, user_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS warnings (warn_id BIGINT, guild_id BIGINT, user_id BIGINT, warning TEXT, warn_time DATE, warned_by BIGINT, PRIMARY KEY (warn_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS economy (user_id BIGINT NOT NULL PRIMARY KEY, money BIGINT NOT NULL DEFAULT 0)")
    cur.execute("CREATE TABLE IF NOT EXISTS profile (user_id BIGINT, rank_name TEXT, rank_int BIGINT, UNIQUE (user_id, rank_name, rank_int))")
    CONNECTION.commit()
    
    cur = await aiosqlite.connect("code/count/count.db")
    await cur.execute("CREATE TABLE IF NOT EXISTS count (count INTEGER)")
    await cur.commit()
    await cur.close()

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix='***',
        activity = discord.Game(name="Ping Me For Help!"),
        intents = discord.Intents.default()
    )

    async def setup_hook(self):
        await initialise()
        get_access_token.start()
        for ext in os.listdir('./code/cogs'):
            if ext.endswith('.py'):
                await self.load_extension(f'cogs.{ext[:-3]}')

bot = MyBot()
bot.count_hold = 0
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@tasks.loop(minutes=45)
async def get_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(auth_url, data=data)
    access_token = response.json()['access_token']
    bot.access_token = access_token

if __name__ == '__main__':
    bot.run(TOKEN)