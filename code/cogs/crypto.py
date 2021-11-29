import discord
from discord.ext import commands
from utils.helpers import *
from datetime import datetime

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff


class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def prices(self, ctx):
        "See the current crypto prices"
        embed = discord.Embed(
            title = "Current Crpytocurrency Price",
            description = f"**In order to see more information on a specific cryptocurrency, do `{ctx.prefix}crypto <ticker>` to show price, percentage change, and more.** \n\nPrices are updated every 60 seconds. \nLetters following the name within () are known as the ticker. \nExample: Bitcoin (BTC) - The ticker is BTC",
            colour = discord.Colour.gold()
        )

        for key in ctx.bot.price_dict:
            embed.add_field(name = f"{key}", value = f"{ctx.bot.price_dict[key]:,}", inline=True)

        await ctx.send(embed=embed)


    @commands.command()
    async def crypto(self, 
        ctx, 
        ticker: str=commands.Option(description="Ticker for crypto you want expanded information on")
    ):
        "Send more information on a certain cryptocurrency"
        if ticker == None:
            embed = discord.Embed(
                colour = color,
                title = "→ No Ticker Provided!",
                description=f"• You must provide a ticker in order to use this command. Example: `{ctx.prefix}crypto btc`"
            )
            await ctx.send(embed=embed)

        ticker = str(ticker)

        if ticker.lower() == "btc":
            embed = discord.Embed(
                title = "Bitcoin",
                description = "Information is updated every 60 seconds",
                colour = 0xf7931a
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Bitcoin (BTC)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('bitcoin_change'):,}%")
            file = discord.File("./utils/crypto_icons/bitcoin.png", filename = "bitcoin.png")
            embed.set_thumbnail(url = "attachment://bitcoin.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "eth":
            embed = discord.Embed(
                title = "Ethereum",
                description = "Information is updated every 60 seconds",
                colour = 0x627eea
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Ethereum (ETH)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('ethereum_change'):,}%")
            file = discord.File("./utils/crypto_icons/ethereum.png", filename = "ethereum.png")
            embed.set_thumbnail(url = "attachment://ethereum.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "bnb":
            embed = discord.Embed(
                title = "Binance Coin",
                description = "Information is updated every 60 seconds",
                colour = 0xf3ba2f
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Binance Coin (BNB)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('binance_coin_change'):,}%")
            file = discord.File("./utils/crypto_icons/binance_coin.png", filename = "binance_coin.png")
            embed.set_thumbnail(url = "attachment://binance_coin.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "sol":
            embed = discord.Embed(
                title = "Solana",
                description = "Information is updated every 60 seconds",
                colour = 0x27dcb8
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Solana (SOL)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('solana_change'):,}%")
            file = discord.File("./utils/crypto_icons/solana.png", filename = "solana.png")
            embed.set_thumbnail(url = "attachment://solana.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "ada":
            embed = discord.Embed(
                title = "Cardana",
                description = "Information is updated every 60 seconds",
                colour = 0x3cc8c8
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Cardano (ADA)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('cardano_change'):,}%")
            file = discord.File("./utils/crypto_icons/cardano.png", filename = "cardano.png")
            embed.set_thumbnail(url = "attachment://cardano.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "xrp":
            embed = discord.Embed(
                title = "XRP",
                description = "Information is updated every 60 seconds",
                colour = 0x00aae4
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('XRP (XRP)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('xrp_change'):,}%")
            file = discord.File("./utils/crypto_icons/xrp.png", filename = "xrp.png")
            embed.set_thumbnail(url = "attachment://xrp.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "dot":
            embed = discord.Embed(
                title = "Polkadot",
                description = "Information is updated every 60 seconds",
                colour = 0xf0047f
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Polkadot (DOT)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('polkadot_change'):,}%")
            file = discord.File("./utils/crypto_icons/polkadot.png", filename = "polkadot.png")
            embed.set_thumbnail(url = "attachment://polkadot.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "doge":
            embed = discord.Embed(
                title = "Dogecoin",
                description = "Information is updated every 60 seconds",
                colour = 0xc3a634
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Dogecoin (DOGE)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('dogecoin_change'):,}%")
            file = discord.File("./utils/crypto_icons/dogecoin.png", filename = "dogecoin.png")
            embed.set_thumbnail(url = "attachment://dogecoin.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "avax":
            embed = discord.Embed(
                title = "Avalanche",
                description = "Information is updated every 60 seconds",
                colour = 0xe84142
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Avalanche (AVAX)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('avalanche_change'):,}%")
            file = discord.File("./utils/crypto_icons/avalanche.png", filename = "avalanche.png")
            embed.set_thumbnail(url = "attachment://avalanche.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "shib":
            embed = discord.Embed(
                title = "SHIBA INU",
                description = "Information is updated every 60 seconds",
                colour = 0xe93b24
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('SHIBA INU (SHIB)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('shiba_inu_change'):,}%")
            file = discord.File("./utils/crypto_icons/shiba_inu.png", filename = "shiba_inu.png")
            embed.set_thumbnail(url = "attachment://shiba_inu.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "luna":
            embed = discord.Embed(
                title = "Terra",
                description = "Information is updated every 60 seconds",
                colour = 0x5494f8
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Terra (LUNA)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('terra_change'):,}%")
            file = discord.File("./utils/crypto_icons/terra.png", filename = "terra.png")
            embed.set_thumbnail(url = "attachment://terra.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "ltc":
            embed = discord.Embed(
                title = "Litecoin",
                description = "Information is updated every 60 seconds",
                colour = 0x345d9d
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Litecoin (LTC)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('litecoin_change'):,}%")
            file = discord.File("./utils/crypto_icons/litecoin.png", filename = "litecoin.png")
            embed.set_thumbnail(url = "attachment://litecoin.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "uni":
            embed = discord.Embed(
                title = "Uniswap",
                description = "Information is updated every 60 seconds",
                colour = 0xff027d
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Uniswap (UNI)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('uniswap_change'):,}%")
            file = discord.File("./utils/crypto_icons/uniswap.png", filename = "uniswap.png")
            embed.set_thumbnail(url = "attachment://uniswap.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "link":
            embed = discord.Embed(
                title = "Chainlink",
                description = "Information is updated every 60 seconds",
                colour = 0x335dd2
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Chainlink (LINK)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('chainlink_change'):,}%")
            file = discord.File("./utils/crypto_icons/chainlink.png", filename = "chainlink.png")
            embed.set_thumbnail(url = "attachment://chainlink.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "matic":
            embed = discord.Embed(
                title = "Polygon",
                description = "Information is updated every 60 seconds",
                colour = 0x2bbdf7
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Polygon (MATIC)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('polygon_change'):,}%")
            file = discord.File("./utils/crypto_icons/polygon.png", filename = "polygon.png")
            embed.set_thumbnail(url = "attachment://polygon.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "algo":
            embed = discord.Embed(
                title = "Algorand",
                description = "Information is updated every 60 seconds",
                colour = 0x000000
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Algorand (ALGO)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('algorand_change'):,}%")
            file = discord.File("./utils/crypto_icons/algorand.png", filename = "algorand.png")
            embed.set_thumbnail(url = "attachment://algorand.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "bch":
            embed = discord.Embed(
                title = "Bitcoin Cash",
                description = "Information is updated every 60 seconds",
                colour = 0x8dc351
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Bitcoin Cash (BCH)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('bitcoin_cash_change'):,}%")
            file = discord.File("./utils/crypto_icons/bitcoin_cash.png", filename = "bitcoin_cash.png")
            embed.set_thumbnail(url = "attachment://bitcoin_cash.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "vet":
            embed = discord.Embed(
                title = "VeChain",
                description = "Information is updated every 60 seconds",
                colour = 0x15bdff
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('VeChain (VET)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('vechain_change'):,}%")
            file = discord.File("./utils/crypto_icons/vechain.png", filename = "vechain.png")
            embed.set_thumbnail(url = "attachment://vechain.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "xlm":
            embed = discord.Embed(
                title = "Stellar",
                description = "Information is updated every 60 seconds",
                colour = 0x14b6e7
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Stellar (XLM)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('stellar_change'):,}%")
            file = discord.File("./utils/crypto_icons/stellar.png", filename = "stellar.png")
            embed.set_thumbnail(url = "attachment://stellar.png")

            await ctx.send(embed=embed, file=file)

        if ticker.lower() == "icp":
            embed = discord.Embed(
                title = "Internet Computer",
                description = "Information is updated every 60 seconds",
                colour = 0xf15a24
            )
            embed.add_field(name = "Current Price -", value = f"${ctx.bot.price_dict.get('Internet Computer (ICP)'):,}")
            embed.add_field(name = "24 Hour Change -", value = f"{ctx.bot.price_change_dict.get('internet_computer_change'):,}%")
            file = discord.File("./utils/crypto_icons/internet_computer.png", filename = "internet_computer.png")
            embed.set_thumbnail(url = "attachment://internet_computer.png")

            await ctx.send(embed=embed, file=file)


    @crypto.error
    async def crypto_error(self, ctx, error):
        embed = discord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Crypto(bot))