import bisect
import os
import random
import discord
from discord.ext import commands
from economy_schema import Database
from PIL import Image
from reader import InsufficientFundsException
from discord import app_commands

color = 0xc48aff

class Slots(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = Database(bot)

    async def check_bet(
        self,
        interaction: discord.Interaction,
        bet
    ):
        bet = int(bet)
        if bet <= 0:
            raise commands.errors.BadArgument()
        current = (await self.economy.get_entry(interaction.user.id))[1]
        if bet > current:
            raise InsufficientFundsException()


    #Usage: slots [bet]
    @app_commands.command()
    @app_commands.checks.cooldown(1, 4)
    @app_commands.describe(bet='Amount of money to bet')
    async def slots(
        self,
        interaction: discord.Interaction,
        bet: int
    ):
        "Bet a specified amount of money on the slot machines"

        await self.check_bet(interaction, bet)
        facade = Image.open(f'./code/utils/slot-face.png').convert('RGBA')
        reel = Image.open(f'./code/utils/slot-reel.png').convert('RGBA')

        rw, rh = reel.size
        item = 180
        items = rh//item

        s1 = random.randint(1, items-1)
        s2 = random.randint(1, items-1)
        s3 = random.randint(1, items-1)

        win_rate = 1/100

        if random.random() < win_rate:
            symbols_weights = [3.5, 7, 15, 25, 55]
            x = round(random.random()*100, 1)
            pos = bisect.bisect(symbols_weights, x)
            s1 = pos + (random.randint(1, (items/6)-1) * 6)
            s2 = pos + (random.randint(1, (items/6)-1) * 6)
            s3 = pos + (random.randint(1, (items/6)-1) * 6)
            # ensure no reel hits the last symbol
            s1 = s1 - 6 if s1 == items else s1
            s2 = s2 - 6 if s2 == items else s2
            s3 = s3 - 6 if s3 == items else s3

        images = []
        speed = 6
        for i in range(1, (item//speed)+1):
            bg = Image.new('RGBA', facade.size, color=(255,255,255))
            bg.paste(reel, (25 + rw*0, 100-(speed * i * s1)))
            bg.paste(reel, (25 + rw*1, 100-(speed * i * s2))) # dont ask me why this works, but it took me hours
            bg.paste(reel, (25 + rw*2, 100-(speed * i * s3)))
            bg.alpha_composite(facade)
            images.append(bg)

        fp = './code/players/reels/'+str(interaction.user.id)+'.gif'
        images[0].save(
            fp,
            save_all=True,
            append_images=images[1:], # append all images after first to first
            duration=50  # duration of each slide (ms)
        )

        # win logic
        result = ('lost', bet)
        await self.economy.add_money(interaction.user.id, bet*-1)
        # (1+s1)%6 gets the symbol 0-5 inclusive
        if (1+s1)%6 == (1+s2)%6 == (1+s3)%6:
            symbol = (1+s1)%6
            reward = [4, 80, 40, 25, 10, 5][symbol] * bet
            result = ('won', reward)
            await self.economy.add_money(interaction.user.id, reward)

        embed = discord.Embed(
            title=(
                f'You {result[0]} {result[1]:,} dollars'+
                ('.' if result[0] == 'lost' else '!') # happy or sad based on outcome
            ),
            description=(
                'You now have ' +
                f'**{(await self.economy.get_entry(interaction.user.id))[1]:,}** ' +
                'dollars.'
            ),
            color=(
                discord.Color.red() if result[0] == "lost"
                else discord.Color.green()
            )
        )

        file = discord.File(fp, filename=f'{interaction.user.id}.gif')
        embed.set_image(url=f"attachment://{interaction.user.id}.gif")
        await interaction.response.send_message(
            file=file,
            embed=embed
        )

        file.close()
        os.remove(f'./code/players/reels/{interaction.user.id}.gif')


async def setup(bot: commands.Bot):
    await bot.add_cog(Slots(bot))