import nextcord
from nextcord.ext import commands, tasks
import os
from utils.helpers import *
import aiosqlite
import asyncio

import hmac
import hashlib
import time
import base64
import requests
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
    await bot.db.execute("CREATE TABLE IF NOT EXISTS counter (bot_id int, count int, PRIMARY KEY (bot_id))")
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

    update.start()

api_key = "ca75c18a5eb09f6d3e2b691f176fcbb2dc46c0f3226818a1f5f5e026939303be"
secret = "83f9a8c0a33b9a6c652c6b8342beb43050c69b2cfea13664de3f438e7333fb9df527ad60a311515947b6bd58752c50542f53144edd3c3442e317bdece2234cd9"

nonce = int(time.time() * 1000)
base_url = "https://dev-api.shrimpy.io"
request_path = "/v1/exchanges/binance/ticker"

method = "GET"
prehash_string = ''.join([request_path, method, str(nonce), ('')])

secret_key = base64.b64decode(secret)
prehash_string = prehash_string.encode('ascii')

signature = hmac.new(secret_key, prehash_string, hashlib.sha256)
signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')

headers = {
    'Content-Type': 'application/json',
    'DEV-SHRIMPY-KEY': api_key,
    'DEV-SHRIMPY-API-NONCE': str(nonce),
    'DEV-SHRIMPY-API-SIGNATURE': signature_b64
}

bot.price_dict = {'Bitcoin':f'0', 'Ethereum':f'0', 'Binance Coin':f'0', 
'Solana':f'0', 'Cardano':f'0', 'XRP':f'0', 'Polkadot':f'0',
'Dogecoin':f'0', 'Avalanche':f'0', 'SHIBA INU':f'0', 
'Terra':f'0', 'Litecoin':f'0', 'Uniswap':f'0', 'Chainlink':f'0',
'Polygon':f'0', 'Algorand':f'0', 'Bitcoin Cash':f'0', 
'VeChain':f'0', 'Stellar':f'0', 'Internet Computer':f'0'}

@tasks.loop(seconds=60)
async def update():
    response = requests.get(
        base_url + request_path,
        headers = headers
    )

    btc_price = response.json()[1].get('priceUsd')
    eth_price = response.json()[0].get('priceUsd')
    bnb_price = response.json()[3].get('priceUsd')
    sol_price = response.json()[176].get('priceUsd')
    ada_price = response.json()[64].get('priceUsd')
    xrp_price = response.json()[41].get('priceUsd')
    dot_price = response.json()[222].get('priceUsd')
    doge_price = response.json()[143].get('priceUsd')
    avax_price = response.json()[250].get('priceUsd')
    shib_price = response.json()[362].get('priceUsd')
    luna_price = response.json()[226].get('priceUsd')
    ltc_price = response.json()[2].get('priceUsd')
    uni_price = response.json()[240].get('priceUsd')
    link_price = response.json()[20].get('priceUsd')
    matic_price = response.json()[135].get('priceUsd')
    algo_price = response.json()[142].get('priceUsd')
    bch_price = response.json()[162].get('priceUsd')
    vet_price = response.json()[121].get('priceUsd')
    xlm_price = response.json()[67].get('priceUsd')
    icp_price = response.json()[364].get('priceUsd')

    update_dict = {'Bitcoin (BTC) -':f'{btc_price}', 'Ethereum (ETH) -':f'{eth_price}', 'Binance Coin (BNB) -':f'{bnb_price}', 
    'Solana (SOL) -':f'{sol_price}', 'Cardano (ADA) -':f'{ada_price}', 'XRP (XRP) -':f'{xrp_price}', 'Polkadot (DOT) -':f'{dot_price}',
    'Dogecoin (DOGE) -':f'{doge_price}', 'Avalanche (AVAX) -':f'{avax_price}', 'SHIBA INU (SHIB) -':f'{shib_price}', 
    'Terra (LUNA) -':f'{luna_price}', 'Litecoin (LTC) -':f'{ltc_price}', 'Uniswap (UNI) -':f'{uni_price}', 'Chainlink (LINK) -':f'{link_price}',
    'Polygon (MATIC) -':f'{matic_price}', 'Algorand (ALGO) -':f'{algo_price}', 'Bitcoin Cash (BCH) -':f'{bch_price}', 
    'VeChain (VET) -':f'{vet_price}', 'Stellar (XLM) -':f'{xlm_price}', 'Internet Computer (ICP) -':f'{icp_price}'}

    bot.price_dict.update(update_dict)


bot.remove_command('help')
bot.loop.create_task(initialise())
bot.run("ODk1ODEyMDk2NDU2MDExNzg2.YV-ABw.JnHalLuRzYdjXodKmjCKHbdTLSk")
asyncio.run(bot.db.close())