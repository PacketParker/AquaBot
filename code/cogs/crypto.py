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

mktcap_dict = {'Bitcoin (BTC)':0, 'Ethereum (ETH)':0, 'Binance Coin (BNB)':0, 
    'Solana (SOL)':0, 'Cardano (ADA)':0, 'XRP (XRP)':0, 'Polkadot (DOT)':0,
    'Dogecoin (DOGE)':0, 'Avalanche (AVAX)':0, 'SHIBA INU (SHIB)':0, 
    'Terra (LUNA)':0, 'Litecoin (LTC)':0, 'Uniswap (UNI)':0, 'Chainlink (LINK)':0,
    'Polygon (MATIC)':0, 'Algorand (ALGO)':0, 'Bitcoin Cash (BCH)':0, 
    'VeChain (VET)':0, 'Stellar (XLM)':0, 'Internet Computer (ICP)':0}

high_dict = {'Bitcoin (BTC)':0, 'Ethereum (ETH)':0, 'Binance Coin (BNB)':0, 
    'Solana (SOL)':0, 'Cardano (ADA)':0, 'XRP (XRP)':0, 'Polkadot (DOT)':0,
    'Dogecoin (DOGE)':0, 'Avalanche (AVAX)':0, 'SHIBA INU (SHIB)':0, 
    'Terra (LUNA)':0, 'Litecoin (LTC)':0, 'Uniswap (UNI)':0, 'Chainlink (LINK)':0,
    'Polygon (MATIC)':0, 'Algorand (ALGO)':0, 'Bitcoin Cash (BCH)':0, 
    'VeChain (VET)':0, 'Stellar (XLM)':0, 'Internet Computer (ICP)':0}

low_dict = {'Bitcoin (BTC)':0, 'Ethereum (ETH)':0, 'Binance Coin (BNB)':0, 
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

        try:
            btc_high = float(response.json()['RAW']['BTC']['USD']['HIGH24HOUR'])
            eth_high = float(response.json()['RAW']['ETH']['USD']['HIGH24HOUR'])
            bnb_high = float(response.json()['RAW']['BNB']['USD']['HIGH24HOUR'])
            sol_high = float(response.json()['RAW']['SOL']['USD']['HIGH24HOUR'])
            ada_high = float(response.json()['RAW']['ADA']['USD']['HIGH24HOUR'])
            xrp_high = float(response.json()['RAW']['XRP']['USD']['HIGH24HOUR'])
            dot_high = float(response.json()['RAW']['DOT']['USD']['HIGH24HOUR'])
            doge_high = float(response.json()['RAW']['DOGE']['USD']['HIGH24HOUR'])
            avax_high = float(response.json()['RAW']['AVAX']['USD']['HIGH24HOUR'])
            shib_high = float(response.json()['RAW']['SHIB']['USD']['HIGH24HOUR'])
            luna_high = float(response.json()['RAW']['LUNA']['USD']['HIGH24HOUR'])
            ltc_high = float(response.json()['RAW']['LTC']['USD']['HIGH24HOUR'])
            uni_high = float(response.json()['RAW']['UNI']['USD']['HIGH24HOUR'])
            link_high = float(response.json()['RAW']['LINK']['USD']['HIGH24HOUR'])
            matic_high = float(response.json()['RAW']['MATIC']['USD']['HIGH24HOUR'])
            algo_high = float(response.json()['RAW']['ALGO']['USD']['HIGH24HOUR'])
            bch_high = float(response.json()['RAW']['BCH']['USD']['HIGH24HOUR'])
            vet_high =  float(response.json()['RAW']['VET']['USD']['HIGH24HOUR'])
            xlm_high = float(response.json()['RAW']['XLM']['USD']['HIGH24HOUR'])
            icp_high = float(response.json()['RAW']['ICP']['USD']['HIGH24HOUR'])
        except TypeError:
            btc_high = 0
            eth_high = 0
            bnb_high = 0
            sol_high = 0
            ada_high = 0
            xrp_high = 0
            dot_high = 0
            doge_high = 0
            avax_high = 0
            shib_high = 0
            luna_high = 0
            ltc_high = 0
            uni_high = 0
            link_high = 0
            matic_high = 0
            algo_high = 0
            bch_high = 0
            vet_high = 0
            xlm_high = 0
            icp_high = 0

        try:
            btc_low = float(response.json()['RAW']['BTC']['USD']['LOW24HOUR'])
            eth_low = float(response.json()['RAW']['ETH']['USD']['LOW24HOUR'])
            bnb_low = float(response.json()['RAW']['BNB']['USD']['LOW24HOUR'])
            sol_low = float(response.json()['RAW']['SOL']['USD']['LOW24HOUR'])
            ada_low = float(response.json()['RAW']['ADA']['USD']['LOW24HOUR'])
            xrp_low = float(response.json()['RAW']['XRP']['USD']['LOW24HOUR'])
            dot_low = float(response.json()['RAW']['DOT']['USD']['LOW24HOUR'])
            doge_low = float(response.json()['RAW']['DOGE']['USD']['LOW24HOUR'])
            avax_low = float(response.json()['RAW']['AVAX']['USD']['LOW24HOUR'])
            shib_low = float(response.json()['RAW']['SHIB']['USD']['LOW24HOUR'])
            luna_low = float(response.json()['RAW']['LUNA']['USD']['LOW24HOUR'])
            ltc_low = float(response.json()['RAW']['LTC']['USD']['LOW24HOUR'])
            uni_low = float(response.json()['RAW']['UNI']['USD']['LOW24HOUR'])
            link_low = float(response.json()['RAW']['LINK']['USD']['LOW24HOUR'])
            matic_low = float(response.json()['RAW']['MATIC']['USD']['LOW24HOUR'])
            algo_low = float(response.json()['RAW']['ALGO']['USD']['LOW24HOUR'])
            bch_low = float(response.json()['RAW']['BCH']['USD']['LOW24HOUR'])
            vet_low =  float(response.json()['RAW']['VET']['USD']['LOW24HOUR'])
            xlm_low = float(response.json()['RAW']['XLM']['USD']['LOW24HOUR'])
            icp_low = float(response.json()['RAW']['ICP']['USD']['LOW24HOUR'])
        except TypeError:
            btc_low = 0
            eth_low = 0
            bnb_low = 0
            sol_low = 0
            ada_low = 0
            xrp_low = 0
            dot_low = 0
            doge_low = 0
            avax_low = 0
            shib_low = 0
            luna_low = 0
            ltc_low = 0
            uni_low = 0
            link_low = 0
            matic_low = 0
            algo_low = 0
            bch_low = 0
            vet_low = 0
            xlm_low = 0
            icp_low = 0

        try:
            btc_mktcap = float(response.json()['RAW']['BTC']['USD']['MKTCAP'])
            eth_mktcap = float(response.json()['RAW']['ETH']['USD']['MKTCAP'])
            bnb_mktcap = float(response.json()['RAW']['BNB']['USD']['MKTCAP'])
            sol_mktcap = float(response.json()['RAW']['SOL']['USD']['MKTCAP'])
            ada_mktcap = float(response.json()['RAW']['ADA']['USD']['MKTCAP'])
            xrp_mktcap = float(response.json()['RAW']['XRP']['USD']['MKTCAP'])
            dot_mktcap = float(response.json()['RAW']['DOT']['USD']['MKTCAP'])
            doge_mktcap = float(response.json()['RAW']['DOGE']['USD']['MKTCAP'])
            avax_mktcap = float(response.json()['RAW']['AVAX']['USD']['MKTCAP'])
            shib_mktcap = float(response.json()['RAW']['SHIB']['USD']['MKTCAP'])
            luna_mktcap = float(response.json()['RAW']['LUNA']['USD']['MKTCAP'])
            ltc_mktcap = float(response.json()['RAW']['LTC']['USD']['MKTCAP'])
            uni_mktcap = float(response.json()['RAW']['UNI']['USD']['MKTCAP'])
            link_mktcap = float(response.json()['RAW']['LINK']['USD']['MKTCAP'])
            matic_mktcap = float(response.json()['RAW']['MATIC']['USD']['MKTCAP'])
            algo_mktcap = float(response.json()['RAW']['ALGO']['USD']['MKTCAP'])
            bch_mktcap = float(response.json()['RAW']['BCH']['USD']['MKTCAP'])
            vet_mktcap =  float(response.json()['RAW']['VET']['USD']['MKTCAP'])
            xlm_mktcap = float(response.json()['RAW']['XLM']['USD']['MKTCAP'])
            icp_mktcap = float(response.json()['RAW']['ICP']['USD']['MKTCAP'])
        except TypeError:
            btc_mktcap = 0
            eth_mktcap = 0
            bnb_mktcap = 0
            sol_mktcap = 0
            ada_mktcap = 0
            xrp_mktcap = 0
            dot_mktcap = 0
            doge_mktcap = 0
            avax_mktcap = 0
            shib_mktcap = 0
            luna_mktcap = 0
            ltc_mktcap = 0
            uni_mktcap = 0
            link_mktcap = 0
            matic_mktcap = 0
            algo_mktcap = 0
            bch_mktcap = 0
            vet_mktcap = 0
            xlm_mktcap = 0
            icp_mktcap = 0


        update_price_dict = {'Bitcoin (BTC)':round(btc_price, 2), 'Ethereum (ETH)':round(eth_price, 2), 'Binance Coin (BNB)':round(bnb_price, 2), 
        'Solana (SOL)':round(sol_price, 2), 'Cardano (ADA)':round(ada_price, 2), 'XRP (XRP)':round(xrp_price, 2), 'Polkadot (DOT)':round(dot_price, 2),
        'Dogecoin (DOGE)':round(doge_price, 3), 'Avalanche (AVAX)':round(avax_price, 2), 'SHIBA INU (SHIB)':round(shib_price, 8), 
        'Terra (LUNA)':round(luna_price, 2), 'Litecoin (LTC)':round(ltc_price, 2), 'Uniswap (UNI)':round(uni_price, 2), 'Chainlink (LINK)':round(link_price, 2),
        'Polygon (MATIC)':round(matic_price, 2), 'Algorand (ALGO)':round(algo_price, 2), 'Bitcoin Cash (BCH)':round(bch_price, 2), 
        'VeChain (VET)':round(vet_price, 2), 'Stellar (XLM)':round(xlm_price, 2), 'Internet Computer (ICP)':round(icp_price, 2)}

        update_price_change_dict = {'Bitcoin (BTC)':round(btc_change, 2), 'Ethereum (ETH)':round(eth_change, 2), 'Binance Coin (BNB)':round(bnb_change, 2), 
        'Solana (SOL)':round(sol_change, 2), 'Cardano (ADA)':round(ada_change, 2), 'XRP (XRP)':round(xrp_change, 2), 'Polkadot (DOT)':round(dot_change, 2),
        'Dogecoin (DOGE)':round(doge_change, 2), 'Avalanche (AVAX)':round(avax_change, 2), 'SHIBA INU (SHIB)':round(shib_change, 2), 
        'Terra (LUNA)':round(luna_change, 2), 'Litecoin (LTC)':round(ltc_change, 2), 'Uniswap (UNI)':round(uni_change, 2), 'Chainlink (LINK)':round(link_change, 2),
        'Polygon (MATIC)':round(matic_change, 2), 'Algorand (ALGO)':round(algo_change, 2), 'Bitcoin Cash (BCH)':round(bch_change, 2), 
        'VeChain (VET)':round(vet_change, 2), 'Stellar (XLM)':round(xlm_change, 2), 'Internet Computer (ICP)':round(icp_change, 2)}

        update_high_dict = {'Bitcoin (BTC)':round(btc_high, 2), 'Ethereum (ETH)':round(eth_high, 2), 'Binance Coin (BNB)':round(bnb_high, 2), 
        'Solana (SOL)':round(sol_high, 2), 'Cardano (ADA)':round(ada_high, 2), 'XRP (XRP)':round(xrp_high, 2), 'Polkadot (DOT)':round(dot_high, 2),
        'Dogecoin (DOGE)':round(doge_high, 3), 'Avalanche (AVAX)':round(avax_high, 2), 'HIBA INU (SHIB)':round(shib_high, 8), 
        'Terra (LUNA)':round(luna_high, 2), 'Litecoin (LTC)':round(ltc_high, 2), 'Uniswap (UNI)':round(uni_high, 2), 'Chainlink (LINK)':round(link_high, 2),
        'Polygon (MATIC)':round(matic_high, 2), 'Algorand (ALGO)':round(algo_high, 2), 'Bitcoin Cash (BCH)':round(bch_high, 2), 
        'VeChain (VET)':round(vet_high, 2), 'Stellar (XLM)':round(xlm_high, 2), 'Internet Computer (ICP)':round(icp_high, 2)}

        update_low_dict = {'Bitcoin (BTC)':round(btc_low, 2), 'Ethereum (ETH)':round(eth_low, 2), 'Binance Coin (BNB)':round(bnb_low, 2), 
        'Solana (SOL)':round(sol_low, 2), 'Cardano (ADA)':round(ada_low, 2), 'XRP (XRP)':round(xrp_low, 2), 'Polkadot (DOT)':round(dot_low, 2),
        'Dogecoin (DOGE)':round(doge_low, 3), 'Avalanche (AVAX)':round(avax_low, 2), 'HIBA INU (SHIB)':round(shib_low, 8), 
        'Terra (LUNA)':round(luna_low, 2), 'Litecoin (LTC)':round(ltc_low, 2), 'Uniswap (UNI)':round(uni_low, 2), 'Chainlink (LINK)':round(link_low, 2),
        'Polygon (MATIC)':round(matic_low, 2), 'Algorand (ALGO)':round(algo_low, 2), 'Bitcoin Cash (BCH)':round(bch_low, 2), 
        'VeChain (VET)':round(vet_low, 2), 'Stellar (XLM)':round(xlm_low, 2), 'Internet Computer (ICP)':round(icp_low, 2)}

        update_mktcap_dict = {'Bitcoin (BTC)':round(btc_mktcap, 2), 'Ethereum (ETH)':round(eth_mktcap, 2), 'Binance Coin (BNB)':round(bnb_mktcap, 2), 
        'Solana (SOL)':round(sol_mktcap, 2), 'Cardano (ADA)':round(ada_mktcap, 2), 'XRP (XRP)':round(xrp_mktcap, 2), 'Polkadot (DOT)':round(dot_mktcap, 2),
        'Dogecoin (DOGE)':round(doge_mktcap, 2), 'Avalanche (AVAX)':round(avax_mktcap, 2), 'HIBA INU (SHIB)':round(shib_mktcap, 2), 
        'Terra (LUNA)':round(luna_mktcap, 2), 'Litecoin (LTC)':round(ltc_mktcap, 2), 'Uniswap (UNI)':round(uni_mktcap, 2), 'Chainlink (LINK)':round(link_mktcap, 2),
        'Polygon (MATIC)':round(matic_mktcap, 2), 'Algorand (ALGO)':round(algo_mktcap, 2), 'Bitcoin Cash (BCH)':round(bch_mktcap, 2), 
        'VeChain (VET)':round(vet_mktcap, 2), 'Stellar (XLM)':round(xlm_mktcap, 2), 'Internet Computer (ICP)':round(icp_mktcap, 2)}


        price_dict.update(update_price_dict)
        price_change_dict.update(update_price_change_dict)
        high_dict.update(update_high_dict)
        low_dict.update(update_low_dict)
        mktcap_dict.update(update_mktcap_dict)


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
            embed.add_field(name = f"{key}", value = f"```${price_dict[key]:,}```", inline=True)

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

        icon_name = connect_icon_dict.get(currency)
        color = connect_color_dict.get(currency)

        embed = discord.Embed(
            title = currency,
            description = "Information is updated every 60 seconds",
            colour = color
        )
        embed.add_field(name = "Current Price -", value = f"```${price_dict.get(currency):,}```", inline=True)
        embed.add_field(name = "24 Hour Change -", value = f"```{price_change_dict.get(currency):,}%```", inline=True)
        embed.add_field(name = "24 Hour High -", value = f"```${high_dict.get(currency):,}```", inline=False)
        embed.add_field(name = "24 Hour Low -", value = f"```${low_dict.get(currency):,}```", inline=True)
        embed.add_field(name = "Market Cap -", value = f"```${mktcap_dict.get(currency):,}```", inline=False)
        file = discord.File(f"./code/utils/crypto_icons/{icon_name}.png", filename = f"{icon_name}.png")
        embed.set_thumbnail(url = f"attachment://{icon_name}.png")

        await interaction.response.send_message(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(Crypto(bot))