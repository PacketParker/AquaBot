import discord
from discord.ext import commands, tasks
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
from aiohttp import request
from decimal import *

#TODO SLOTS AND BLACKJACK ARE BROKEN WITHIN SLASH COMMANDS


#BEFORE UPLOAD TO MAIN BOT FOLLOW THESE STEPS:
    #Change prefix in main file and in config.yml
    #Change token in main file andi n config.yml
    #Add main bots token to line 74 of music.py

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
    status = discord.Game(f"Ping Me For Help!"),
    owner_ids=OWNER_IDS,
    intents = discord.Intents(
    guild_reactions=True,
    guild_messages=True,
    guilds=True,
    integrations=True,
    voice_states=True,
    dm_reactions=True,
    guild_typing=True,
    dm_messages=True,
    dm_typing=True,
    webhooks=True,
    members=True,
    invites=True,
    emojis=True,
    bans=True,
    ),
    slash_commands=True,
    slash_command_guilds = [891743644938297395]
)

bot.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}') 

for filename in os.listdir('./cogs/economy'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.economy.{filename[:-3]}') 

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


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

bot.price_dict = {'Bitcoin (BTC)':0, 'Ethereum (ETH)':0, 'Binance Coin (BNB)':0, 
    'Solana (SOL)':0, 'Cardano (ADA)':0, 'XRP (XRP)':0, 'Polkadot (DOT)':0,
    'Dogecoin (DOGE)':0, 'Avalanche (AVAX)':0, 'SHIBA INU (SHIB)':0, 
    'Terra (LUNA)':0, 'Litecoin (LTC)':0, 'Uniswap (UNI)':0, 'Chainlink (LINK)':0,
    'Polygon (MATIC)':0, 'Algorand (ALGO)':0, 'Bitcoin Cash (BCH)':0, 
    'VeChain (VET)':0, 'Stellar (XLM)':0, 'Internet Computer (ICP)':0}

bot.price_change_dict = {'bitcoin_change':0, 'ethereum_change':0, 'binance_coin_change':0, 
    'solana_change':0, 'cardano_change':0, 'xrp_change':0, 'polkadot_change':0,
    'dogecoin_change':0, 'avalanche_change':0, 'shib_inu_change':0, 
    'terra_change':0, 'litecoin_change':0, 'uniswap_change':0, 'chainlink_change':0,
    'polygon_change':0, 'algorand_change':0, 'bitcoin_cash_change':0, 
    'vechain_change':0, 'stellar_change':0, 'internet_computer_change':0}

@tasks.loop(seconds=60)
async def update_crypto():
    response = requests.get(
        base_url + request_path,
        headers = headers
    )

    try:
        btc_price = float(response.json()[1].get('priceUsd'))
        eth_price = float(response.json()[0].get('priceUsd'))
        bnb_price = float(response.json()[3].get('priceUsd'))
        sol_price = float(response.json()[176].get('priceUsd'))
        ada_price = float(response.json()[64].get('priceUsd'))
        xrp_price = float(response.json()[41].get('priceUsd'))
        dot_price = float(response.json()[222].get('priceUsd'))
        doge_price = float(response.json()[143].get('priceUsd'))
        avax_price = float(response.json()[250].get('priceUsd'))
        shib_price = Decimal(response.json()[362].get('priceUsd'))
        luna_price = float(response.json()[226].get('priceUsd'))
        ltc_price = float(response.json()[2].get('priceUsd'))
        uni_price = float(response.json()[240].get('priceUsd'))
        link_price = float(response.json()[20].get('priceUsd'))
        matic_price = float(response.json()[135].get('priceUsd'))
        algo_price = float(response.json()[142].get('priceUsd'))
        bch_price = float(response.json()[162].get('priceUsd'))
        vet_price = float(response.json()[121].get('priceUsd'))
        xlm_price = float(response.json()[67].get('priceUsd'))
        icp_price = float(response.json()[364].get('priceUsd'))
    except TypeError:
        btc_price = 0
        eth_price = 0
        bnb_price = 0
        sol_price = 0
        ada_price = 0
        xrp_price = 0
        dot_price = 0
        doge_price = 0
        avax_price = 0
        shib_price = 0
        luna_price = 0
        ltc_price = 0
        uni_price = 0
        link_price = 0
        matic_price = 0
        algo_price = 0
        bch_price = 0
        vet_price = 0
        xlm_price = 0
        icp_price = 0

    try:
        btc_change = float(response.json()[1].get('percentChange24hUsd'))
        eth_change = float(response.json()[0].get('percentChange24hUsd'))
        bnb_change = float(response.json()[3].get('percentChange24hUsd'))
        sol_change = float(response.json()[176].get('percentChange24hUsd'))
        ada_change = float(response.json()[64].get('percentChange24hUsd'))
        xrp_change = float(response.json()[41].get('percentChange24hUsd'))
        dot_change = float(response.json()[222].get('percentChange24hUsd'))
        doge_change = float(response.json()[143].get('percentChange24hUsd'))
        avax_change = float(response.json()[250].get('percentChange24hUsd'))
        shib_change = float(response.json()[362].get('percentChange24hUsd'))
        luna_change = float(response.json()[226].get('percentChange24hUsd'))
        ltc_change = float(response.json()[2].get('percentChange24hUsd'))
        uni_change = float(response.json()[240].get('percentChange24hUsd'))
        link_change = float(response.json()[20].get('percentChange24hUsd'))
        matic_change = float(response.json()[135].get('percentChange24hUsd'))
        algo_change = float(response.json()[142].get('percentChange24hUsd'))
        bch_change = float(response.json()[162].get('percentChange24hUsd'))
        vet_change = float(response.json()[121].get('percentChange24hUsd'))
        xlm_change = float(response.json()[67].get('percentChange24hUsd'))
        icp_change = float(response.json()[364].get('percentChange24hUsd'))
    except TypeError:
        btc_change = 0
        eth_change = 0
        bnb_change = 0
        sol_change = 0
        ada_change = 0
        xrp_change = 0
        dot_change = 0
        doge_change = 0
        avax_change = 0
        shib_change = 0
        luna_change = 0
        ltc_change = 0
        uni_change = 0
        link_change = 0
        matic_change = 0
        algo_change = 0
        bch_change = 0
        vet_change = 0
        xlm_change = 0
        icp_change = 0

    update_price_dict = {'Bitcoin (BTC)':round(btc_price, 2), 'Ethereum (ETH)':round(eth_price, 2), 'Binance Coin (BNB)':round(bnb_price, 2), 
    'Solana (SOL)':round(sol_price, 2), 'Cardano (ADA)':round(ada_price, 2), 'XRP (XRP)':round(xrp_price, 2), 'Polkadot (DOT)':round(dot_price, 2),
    'Dogecoin (DOGE)':round(doge_price, 4), 'Avalanche (AVAX)':round(avax_price, 2), 'SHIBA INU (SHIB)':shib_price, 
    'Terra (LUNA)':round(luna_price, 2), 'Litecoin (LTC)':round(ltc_price, 2), 'Uniswap (UNI)':round(uni_price, 2), 'Chainlink (LINK)':round(link_price, 2),
    'Polygon (MATIC)':round(matic_price, 2), 'Algorand (ALGO)':round(algo_price, 2), 'Bitcoin Cash (BCH)':round(bch_price, 2), 
    'VeChain (VET)':round(vet_price, 2), 'Stellar (XLM)':round(xlm_price, 2), 'Internet Computer (ICP)':round(icp_price, 2)}

    update_price_change_dict = {'bitcoin_change':round(btc_change, 2), 'ethereum_change':round(eth_change, 2), 'binance_coin_change':round(bnb_change, 2), 
    'solana_change':round(sol_change, 2), 'cardano_change':round(ada_change, 2), 'xrp_change':round(xrp_change, 2), 'polkadot_change':round(dot_change, 2),
    'dogecoin_change':round(doge_change, 2), 'avalanche_change':round(avax_change, 2), 'shib_inu_change':round(shib_change, 2), 
    'terra_change':round(luna_change, 2), 'litecoin_change':round(ltc_change, 2), 'uniswap_change':round(uni_change, 2), 'chainlink_change':round(link_change, 2),
    'polygon_change':round(matic_change, 2), 'algorand_change':round(algo_change, 2), 'bitcoin_cash_change':round(bch_change, 2), 
    'vechain_change':round(vet_change, 2), 'stellar_change':round(xlm_change, 2), 'internet_computer_change':round(icp_change, 2)}

    bot.price_dict.update(update_price_dict)
    bot.price_change_dict.update(update_price_change_dict)


bot.covid_dict = {':microbe: Total cases':0, ':skull_crossbones: Total deaths':0, 
':syringe: Total recovered':0, ':radioactive: Total active cases':0, ':map: Total affected countries':0}

URL = "https://disease.sh/v3/covid-19/all"

@tasks.loop(seconds=300)
async def update_covid():
    async with request("GET", URL, headers={}) as response:
        if response.status == 200:
            data = await response.json()
            cases = int(data["cases"])
            deaths = int(data["deaths"])
            recovered = int(data["recovered"])
            active = int(data["active"])
            countries = int(data["affectedCountries"])
        
        else:
            cases = 0
            deaths = 0
            recovered = 0
            active = 0
            countries = 0

        update_crypto_dict = {':microbe: Total cases':cases, ':skull_crossbones: Total deaths':deaths, 
        ':syringe: Total recovered':recovered, ':radioactive: Total active cases':active, 
        ':map: Total affected countries':countries}

        bot.covid_dict.update(update_crypto_dict)


@bot.command()
async def new(ctx):
    "See all of the new changes in the bot"
    embed = discord.Embed(
        title = "Change Log",
        description = "Here is everything that has changed on the 12/7 update \n *Note - in order to get slash commands working in you server, you must reinvite the bot with the new link provided in the `invite` command",
        colour = discord.Colour.og_blurple()
    )

    embed.add_field(name = "Slash Commands", value = "All commands have now been transfered to work in both message style commands, and the new slash commands option. This change is due to the upcoming transfer to slash commands that discord is forcing developers into come April 2022. All command that require user input - any text that the user inputs after the command itself, like $play (song name) - will only be available in the slash command format after the April deadline. I have gone ahead and transfered ALL commands over to slash commands, however, in order to help you get used to the new format.", inline=True)
    embed.add_field(name = "Shop", value = "A shop has also been added, which is viewable under the `shop` command. Currently you are able to buy global ranks through the bot, however, there will be more things added soon. For any suggestion, feel free to join the official support server - link available through the `invite` command - and ping the owner with your suggestion.", inline=True)
    embed.add_field(name = "Crypto", value = "A new feature has been added to view the current prices of the top 20 cryptocurrencies, this is available through the `prices` command. You can also see more in depth information (currently only the 24 hour change percentage) through the `crypto` command. As with the shop, suggestions are encouraged, so please join the official support server with the `invite` command, and ping the owner with you suggestions.", inline=False)
    embed.add_field(name = "Bugs", value = "As always we've worked hard to make sure all of the bugs have been ironed out, however, if you find any bug please report it to us in the official support server.", inline=True)
    embed.add_field(name = "12/20 - Small Update", value = "Blackjack earnings have been doubled, have fun.", inline=False)
    embed.add_field(name = "\u200b", value = "Thank you all for using Aqua Bot!", inline=False)


    await ctx.send(embed=embed)


update_covid.start()
update_crypto.start()
bot.loop.create_task(initialise())
bot.run("ODk1ODEyMDk2NDU2MDExNzg2.YV-ABw.N3JAvRe0ZlmYL-KTLCGTXRuCnvE")
asyncio.run(bot.db.close())