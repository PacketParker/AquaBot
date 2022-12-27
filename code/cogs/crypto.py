import discord
from discord.ext import commands, tasks
from discord import app_commands
from typing import Literal
from decimal import Decimal
import requests
from reader import APIKEY

color = 0xc48aff

price_dict = {'Bitcoin (BTC)':0, 'Ethereum (ETH)':0, 'Binance Coin (BNB)':0, 
    'Solana (SOL)':0, 'Cardano (ADA)':0, 'XRP (XRP)':0, 'Polkadot (DOT)':0,
    'Dogecoin (DOGE)':0, 'Avalanche (AVAX)':0, 'SHIBA INU (SHIB)':0, 
    'Terra (LUNA)':0, 'Litecoin (LTC)':0, 'Uniswap (UNI)':0, 'Chainlink (LINK)':0,
    'Polygon (MATIC)':0, 'Algorand (ALGO)':0, 'Bitcoin Cash (BCH)':0, 
    'VeChain (VET)':0, 'Stellar (XLM)':0, 'Internet Computer (ICP)':0}

price_change_dict = {'bitcoin_change':0, 'ethereum_change':0, 'binance_change':0, 
    'solana_change':0, 'cardano_change':0, 'xrp_change':0, 'polkadot_change':0,
    'dogecoin_change':0, 'avalanche_change':0, 'shiba_change':0, 
    'terra_change':0, 'litecoin_change':0, 'uniswap_change':0, 'chainlink_change':0,
    'polygon_change':0, 'algorand_change':0, 'bitcoin_cash_change':0, 
    'vechain_change':0, 'stellar_change':0, 'internet_computer_change':0}

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

connect_change_dict = {'Bitcoin (BTC)':'bitcoin_change', 'Ethereum (ETH)':'ethereum_change', 
    'Binance Coin (BNB)':'binance_change', 'Solana (SOL)':'solana_change', 
    'Cardano (ADA)':'cardano_change', 'XRP (XRP)':'xrp_change', 'Polkadot (DOT)':'polkadot_change',
    'Dogecoin (DOGE)':'dogecoin_change', 'Avalanche (AVAX)':'avalanche_change', 
    'SHIBA INU (SHIB)':'shiba_change', 'Terra (LUNA)':'terra_change', 'Litecoin (LTC)':'litecoin_change', 
    'Uniswap (UNI)':'uniswap_change', 'Chainlink (LINK)':'chainlink_change',
    'Polygon (MATIC)':'polygon_change', 'Algorand (ALGO)':'algorand_change', 
    'Bitcoin Cash (BCH)':'bitcoin_cash_change', 'VeChain (VET)':'vechain_change', 
    'Stellar (XLM)':'stellar_change', 'Internet Computer (ICP)':'internet_computer_change'}

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    async def cog_load(self):
        self.update_crypto.start()

    @tasks.loop(seconds=60)
    async def update_crypto(self):
        response = requests.get(
            f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,BNB,SOL,ADA,XRP,DOT,DOGE,AVAX,SHIB,LUNA,LTC,UNI,LINK,MATIC,ALGO,BCH,VET,XLM,ICP&tsyms=USD&api_key={APIKEY}'
        )

        try:
            btc_price = float(response.json()['RAW']['BTC']['USD']['PRICE'])
            eth_price = float(response.json()['RAW']['ETH']['USD']['PRICE'])
            bnb_price = float(response.json()['RAW']['BNB']['USD']['PRICE'])
            sol_price = float(response.json()['RAW']['SOL']['USD']['PRICE'])
            ada_price = float(response.json()['RAW']['ADA']['USD']['PRICE'])
            xrp_price = float(response.json()['RAW']['XRP']['USD']['PRICE'])
            dot_price = float(response.json()['RAW']['DOT']['USD']['PRICE'])
            doge_price = float(response.json()['RAW']['DOGE']['USD']['PRICE'])
            avax_price = float(response.json()['RAW']['AVAX']['USD']['PRICE'])
            shib_price = Decimal(response.json()['RAW']['SHIB']['USD']['PRICE'])
            luna_price = float(response.json()['RAW']['LUNA']['USD']['PRICE'])
            ltc_price = float(response.json()['RAW']['LTC']['USD']['PRICE'])
            uni_price = float(response.json()['RAW']['UNI']['USD']['PRICE'])
            link_price = float(response.json()['RAW']['LINK']['USD']['PRICE'])
            matic_price =float(response.json()['RAW']['MATIC']['USD']['PRICE'])
            algo_price = float(response.json()['RAW']['ALGO']['USD']['PRICE'])
            bch_price = float(response.json()['RAW']['BCH']['USD']['PRICE'])
            vet_price = float(response.json()['RAW']['VET']['USD']['PRICE'])
            xlm_price = float(response.json()['RAW']['XLM']['USD']['PRICE'])
            icp_price = float(response.json()['RAW']['ICP']['USD']['PRICE'])
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
            btc_change = float(response.json()['RAW']['BTC']['USD']['CHANGEPCT24HOUR'])
            eth_change = float(response.json()['RAW']['ETH']['USD']['CHANGEPCT24HOUR'])
            bnb_change = float(response.json()['RAW']['BNB']['USD']['CHANGEPCT24HOUR'])
            sol_change = float(response.json()['RAW']['SOL']['USD']['CHANGEPCT24HOUR'])
            ada_change = float(response.json()['RAW']['ADA']['USD']['CHANGEPCT24HOUR'])
            xrp_change = float(response.json()['RAW']['XRP']['USD']['CHANGEPCT24HOUR'])
            dot_change = float(response.json()['RAW']['DOT']['USD']['CHANGEPCT24HOUR'])
            doge_change = float(response.json()['RAW']['DOGE']['USD']['CHANGEPCT24HOUR'])
            avax_change = float(response.json()['RAW']['AVAX']['USD']['CHANGEPCT24HOUR'])
            shib_change = float(response.json()['RAW']['SHIB']['USD']['CHANGEPCT24HOUR'])
            luna_change = float(response.json()['RAW']['LUNA']['USD']['CHANGEPCT24HOUR'])
            ltc_change = float(response.json()['RAW']['LTC']['USD']['CHANGEPCT24HOUR'])
            uni_change = float(response.json()['RAW']['UNI']['USD']['CHANGEPCT24HOUR'])
            link_change = float(response.json()['RAW']['LINK']['USD']['CHANGEPCT24HOUR'])
            matic_change = float(response.json()['RAW']['MATIC']['USD']['CHANGEPCT24HOUR'])
            algo_change = float(response.json()['RAW']['ALGO']['USD']['CHANGEPCT24HOUR'])
            bch_change = float(response.json()['RAW']['BCH']['USD']['CHANGEPCT24HOUR'])
            vet_change =  float(response.json()['RAW']['VET']['USD']['CHANGEPCT24HOUR'])
            xlm_change = float(response.json()['RAW']['XLM']['USD']['CHANGEPCT24HOUR'])
            icp_change = float(response.json()['RAW']['ICP']['USD']['CHANGEPCT24HOUR'])
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
        'Dogecoin (DOGE)':round(doge_price, 3), 'Avalanche (AVAX)':round(avax_price, 2), 'SHIBA INU (SHIB)':round(shib_price, 8), 
        'Terra (LUNA)':round(luna_price, 2), 'Litecoin (LTC)':round(ltc_price, 2), 'Uniswap (UNI)':round(uni_price, 2), 'Chainlink (LINK)':round(link_price, 2),
        'Polygon (MATIC)':round(matic_price, 2), 'Algorand (ALGO)':round(algo_price, 2), 'Bitcoin Cash (BCH)':round(bch_price, 2), 
        'VeChain (VET)':round(vet_price, 2), 'Stellar (XLM)':round(xlm_price, 2), 'Internet Computer (ICP)':round(icp_price, 2)}

        update_price_change_dict = {'bitcoin_change':round(btc_change, 2), 'ethereum_change':round(eth_change, 2), 'binance_change':round(bnb_change, 2), 
        'solana_change':round(sol_change, 2), 'cardano_change':round(ada_change, 2), 'xrp_change':round(xrp_change, 2), 'polkadot_change':round(dot_change, 2),
        'dogecoin_change':round(doge_change, 2), 'avalanche_change':round(avax_change, 2), 'shiba_change':round(shib_change, 2), 
        'terra_change':round(luna_change, 2), 'litecoin_change':round(ltc_change, 2), 'uniswap_change':round(uni_change, 2), 'chainlink_change':round(link_change, 2),
        'polygon_change':round(matic_change, 2), 'algorand_change':round(algo_change, 2), 'bitcoin_cash_change':round(bch_change, 2), 
        'vechain_change':round(vet_change, 2), 'stellar_change':round(xlm_change, 2), 'internet_computer_change':round(icp_change, 2)}

        price_dict.update(update_price_dict)
        price_change_dict.update(update_price_change_dict)


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

        for key in price_dict:
            embed.add_field(name = f"{key}", value = f"```{price_dict[key]:,}```", inline=True)

        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    @app_commands.describe(currency="3 letter ticker for the cryptocurrency")
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

        connection = connect_change_dict.get(currency)
        icon_name = connect_icon_dict.get(currency)
        color = connect_color_dict.get(currency)

        embed = discord.Embed(
            title = currency,
            description = "Information is updated every 60 seconds",
            colour = color
        )
        embed.add_field(name = "Current Price -", value = f"${price_dict.get(currency):,}")
        embed.add_field(name = "24 Hour Change -", value = f"{price_change_dict.get(connection):,}%")
        file = discord.File(f"./code/utils/crypto_icons/{icon_name}.png", filename = f"{icon_name}.png")
        embed.set_thumbnail(url = f"attachment://{icon_name}.png")

        await interaction.response.send_message(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(Crypto(bot))