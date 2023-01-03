import discord
from discord.ext import commands, tasks
from discord import app_commands
from typing import Literal
from decimal import Decimal
import requests
from reader import APIKEY

color = 0xc48aff

master_dict = {'Bitcoin (BTC)':'0:0:0:0:0:0', 'Ethereum (ETH)':'0:0:0:0:0:0', 
    'Binance Coin (BNB)':'0:0:0:0:0:0', 'Solana (SOL)':'0:0:0:0:0:0', 'Cardano (ADA)':'0:0:0:0:0:0', 
    'XRP (XRP)':'0:0:0:0:0:0', 'Polkadot (DOT)':'0:0:0:0:0:0','Dogecoin (DOGE)':'0:0:0:0:0:0', 
    'Avalanche (AVAX)':'0:0:0:0:0:0', 'SHIBA INU (SHIB)':'0:0:0:0:0:0', 'Terra (LUNA)':'0:0:0:0:0:0', 
    'Litecoin (LTC)':'0:0:0:0:0:0', 'Uniswap (UNI)':'0:0:0:0:0:0', 'Chainlink (LINK)':'0:0:0:0:0:0',
    'Polygon (MATIC)':'0:0:0:0:0:0', 'Algorand (ALGO)':'0:0:0:0:0:0', 'Bitcoin Cash (BCH)':'0:0:0:0:0:0', 
    'VeChain (VET)':'0:0:0:0:0:0', 'Stellar (XLM)':'0:0:0:0:0:0', 'Internet Computer (ICP)':'0:0:0:0:0:0'}

currencies = ['Bitcoin (BTC)', 'Ethereum (ETH)', 'Binance Coin (BNB)', 'Solana (SOL)', 
    'Cardano (ADA)', 'XRP (XRP)', 'Polkadot (DOT)', 'Dogecoin (DOGE)', 'Avalanche (AVAX)', 
    'SHIBA INU (SHIB)', 'Terra (LUNA)', 'Litecoin (LTC)', 'Uniswap (UNI)', 'Chainlink (LINK)', 
    'Polygon (MATIC)', 'Algorand (ALGO)', 'Bitcoin Cash (BCH)', 'VeChain (VET)', 'Stellar (XLM)', 
    'Internet Computer (ICP)']

connect_color_dict = {'Bitcoin (BTC)':0xf7931a, 'Ethereum (ETH)':0x627eea, 
    'Binance Coin (BNB)':0xf3ba2f, 'Solana (SOL)':0x27dcb8, 'Cardano (ADA)':0x3cc8c8, 
    'XRP (XRP)':0x00aae4, 'Polkadot (DOT)':0xf0047f,'Dogecoin (DOGE)':0xc3a634, 
    'Avalanche (AVAX)':0xe84142, 'SHIBA INU (SHIB)':0xe93b24, 'Terra (LUNA)':0x5494f8, 
    'Litecoin (LTC)':0x345d9d, 'Uniswap (UNI)':0xff027d, 'Chainlink (LINK)':0x335dd2,
    'Polygon (MATIC)':0x2bbdf7, 'Algorand (ALGO)':0x000000, 'Bitcoin Cash (BCH)':0x8dc351, 
    'VeChain (VET)':0x15bdff, 'Stellar (XLM)':0x14b6e7, 'Internet Computer (ICP)':0xf15a24}

connect_icon_dict = {'Bitcoin (BTC)':'bitcoin', 'Ethereum (ETH)':'ethereum', 
    'Binance Coin (BNB)':'binance', 'Solana (SOL)':'solana', 'Cardano (ADA)':'cardano', 
    'XRP (XRP)':'xrp', 'Polkadot (DOT)':'polkadot','Dogecoin (DOGE)':'dogecoin', 
    'Avalanche (AVAX)':'avalanche', 'SHIBA INU (SHIB)':'shiba', 'Terra (LUNA)':'terra', 
    'Litecoin (LTC)':'litecoin', 'Uniswap (UNI)':'uniswap', 'Chainlink (LINK)':'chainlink',
    'Polygon (MATIC)':'polygon', 'Algorand (ALGO)':'algorand', 'Bitcoin Cash (BCH)':'bitcoin_cash', 
    'VeChain (VET)':'vechain', 'Stellar (XLM)':'stellar', 'Internet Computer (ICP)':'internet_computer'}

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    async def cog_load(self):
        self.update_crypto.start()


    def update_dicts_for_currency(self, response, cut_currency, currency):
        round_num = 8 if cut_currency == 'SHIB' else 3 if cut_currency == 'DOGE' else 3 if cut_currency == 'VET' else 3 if cut_currency == 'XLM' else 2
        market = response.json()['RAW'][cut_currency]['USD']['LASTMARKET']
        price = round(Decimal(response.json()['RAW'][cut_currency]['USD']['PRICE']), round_num)
        change_24h = round(Decimal(response.json()['RAW'][cut_currency]['USD']['CHANGEPCT24HOUR']), 2)
        high = round(Decimal(response.json()['RAW'][cut_currency]['USD']['HIGH24HOUR']), round_num)
        low = round(Decimal(response.json()['RAW'][cut_currency]['USD']['LOW24HOUR']), round_num)
        mktcap = round(Decimal(response.json()['RAW'][cut_currency]['USD']['MKTCAP']), 2)

        master_dict[currency] = f'{market}:{price}:{change_24h}:{high}:{low}:{mktcap}'

    @tasks.loop(seconds=60)
    async def update_crypto(self):
        response = requests.get(
            f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,BNB,SOL,ADA,XRP,DOT,DOGE,AVAX,SHIB,LUNA,LTC,UNI,LINK,MATIC,ALGO,BCH,VET,XLM,ICP&tsyms=USD&api_key={APIKEY}'
        )

        for currency in currencies:
            cut_currency = currency[currency.find("(")+1:currency.find(")")]
            self.update_dicts_for_currency(response, cut_currency, currency)


    @app_commands.command()
    async def prices(
        self, 
        interaction: discord.Interaction,
    ):
        "See the current crypto prices"

        embed = discord.Embed(
            title = "Current Crpytocurrency Price",
            description = f"**In order to see more information on a specific cryptocurrency, do `/crypto <ticker>` to show price, percentage change, and more.** \n\nPrices are updated every 60 seconds. \nLetters following the name within () are known as the ticker. \nExample: Bitcoin (BTC) - The ticker is BTC",
            colour = discord.Colour.gold()
        )

        for key in master_dict:
            price = master_dict[key].split(':')[1]
            embed.add_field(name = f"{key}", value = f"```${Decimal(price):,}```", inline=True)

        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    @app_commands.describe(currency="Pick what cryptocurrency you want to see more information on.")
    async def crypto(
        self, 
        interaction: discord.Interaction,
        currency: Literal['Bitcoin (BTC)', 'Ethereum (ETH)', 'Binance Coin (BNB)', 'Solana (SOL)', 
        'Cardano (ADA)', 'XRP (XRP)', 'Polkadot (DOT)', 'Dogecoin (DOGE)', 'Avalanche (AVAX)', 
        'SHIBA INU (SHIB)', 'Terra (LUNA)', 'Litecoin (LTC)', 'Uniswap (UNI)', 'Chainlink (LINK)', 
        'Polygon (MATIC)', 'Algorand (ALGO)', 'Bitcoin Cash (BCH)', 'VeChain (VET)', 'Stellar (XLM)', 
        'Internet Computer (ICP)']
    ):
        "Send more information on a certain cryptocurrency"

        icon_name = connect_icon_dict.get(currency)
        color = connect_color_dict.get(currency)
        market = master_dict[currency].split(':')[0]
        price = master_dict[currency].split(':')[1]
        price_change = master_dict[currency].split(':')[2]
        high = master_dict[currency].split(':')[3]
        low = master_dict[currency].split(':')[4]
        mktcap = master_dict[currency].split(':')[5]

        embed = discord.Embed(
            title = currency,
            description = "Information is updated every 60 seconds",
            colour = color
        )
        embed.add_field(name = "Market", value = f"```{market}```")
        embed.add_field(name = "Current Price", value = f"```${Decimal(price):,}```")
        embed.add_field(name = "24 Hour Change", value = f"```{Decimal(price_change):,}%```")
        embed.add_field(name = "24 Hour High", value = f"```${Decimal(high):,}```")
        embed.add_field(name = "24 Hour Low", value = f"```${Decimal(low):,}```")
        embed.add_field(name = "Market Cap", value = f"```${Decimal(mktcap):,}```")
        file = discord.File(f"./code/utils/crypto_icons/{icon_name}.png", filename = f"{icon_name}.png")
        embed.set_thumbnail(url = f"attachment://{icon_name}.png")

        await interaction.response.send_message(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(Crypto(bot))