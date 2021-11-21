import nextcord
from nextcord.ext import commands
from yaml import add_path_resolver
from utils.helpers import *
from datetime import datetime

import hmac
import hashlib
import time
import base64
import requests
import asyncio

intents = nextcord.Intents.default()
intents.members = True

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

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff


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

response = requests.get(
    base_url + request_path,
    headers = headers
)



class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def prices(self, ctx):
        # Bitcoin - BTC
        # Ethereum - ETH
        # Binance Coin - BNB
        # Solana - SOL
        # Cardano - ADA
        # XRP - XRP
        # Polkadot - DOT
        # Dogecoin - DOGE
        # Avanlanche - AVAX
        # SHIBA INU - SHIB
        # Terra - LUNA
        # Litecoin - LTC
        # Uniswap - UNI
        # Chainlink - LINK
        # Polygon - MATIC
        # Algorand - ALGO
        # Bitcoin Cash - BCH
        # VeChain - VET
        # Stellar - XLM
        # Internet Computer - ICP
        embed = nextcord.Embed(
            title = "Current Crpytocurrency Price",
            description = "Prices are updated ever 60 seconds. \nLetters following the name within () are known as the ticker. \nExample: Bitcoin (BTC) - The ticker is BTC",
            colour = nextcord.Colour.gold()
        )

        for key in self.bot.price_dict:
            embed.add_field(name = f"{key}", value = f"{ctx.price_dict[key]}", inline=True)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Crypto(bot))