import bisect
import os
import random

import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.errors import BadArgument
from modules.economy import Economy
from modules.helpers import *
from PIL import Image
from datetime import datetime
from modules.helpers import PREFIX, InsufficientFundsException

color = 0xc48aff

class Slots(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = Economy()

    def check_bet(self, ctx: commands.Context, bet: int=DEFAULT_BET):
        bet = int(bet)
        if bet <= 0:
            raise commands.errors.BadArgument()
        current = self.economy.get_entry(ctx.author.id)[2]
        if bet > current:
            raise InsufficientFundsException(current, bet)


    #Slot machine, bet must be 1-3
    #Usage: $slots [bet]
    @commands.command()
    @commands.cooldown(1, 1.5, commands.BucketType.user)
    async def slots(self, ctx: commands.Context, bet: int=1):
        self.check_bet(ctx, bet=bet)
        path = os.path.join(ABS_PATH, 'modules/')
        facade = Image.open(f'{path}slot-face.png').convert('RGBA')
        reel = Image.open(f'{path}slot-reel.png').convert('RGBA')

        rw, rh = reel.size
        item = 180
        items = rh//item

        s1 = random.randint(1, items-1)
        s2 = random.randint(1, items-1)
        s3 = random.randint(1, items-1)

        win_rate = 12/100

        if random.random() < win_rate:
            symbols_weights = [3.5, 7, 15, 25, 55] # 
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

        fp = str(id(ctx.author.id))+'.gif'
        images[0].save(
            fp,
            save_all=True,
            append_images=images[1:], # append all images after first to first
            duration=50  # duration of each slide (ms)
        )

        # win logic
        result = ('lost', bet)
        self.economy.add_credits(ctx.author.id, bet*-1)       
        # (1+s1)%6 gets the symbol 0-5 inclusive
        if (1+s1)%6 == (1+s2)%6 == (1+s3)%6:
            symbol = (1+s1)%6
            reward = [4, 80, 40, 25, 10, 5][symbol] * bet
            result = ('won', reward)
            self.economy.add_credits(ctx.author.id, reward)

        embed = make_embed(
            title=(
                f'You {result[0]} {result[1]} credits'+
                ('.' if result[0] == 'lost' else '!') # happy or sad based on outcome
            ),
            description=(
                'You now have ' +
                f'**{self.economy.get_entry(ctx.author.id)[2]}** ' +
                'credits.'
            ),
            color=(
                nextcord.Color.red() if result[0] == "lost"
                else nextcord.Color.green()
            )
        )

        file = nextcord.File(fp, filename=fp)
        embed.set_image(url=f"attachment://{fp}") # none of this makes sense to me :)
        await ctx.send(
            file=file,
            embed=embed
        )

        os.remove(fp)


    @commands.command()
    #Purchase credits. Each credit is worth ${DEFAULT_BET}.
    #usage: 'buyc [amount of credits]'
    async def buyc(self, ctx: commands.Context, *, amount_to_buy: int=0):
        user_id = ctx.author.id
        profile = self.economy.get_entry(user_id)
        cost = amount_to_buy * DEFAULT_BET
        if amount_to_buy == 0:
            embed = nextcord.Embed(
                colour = color,
                title = "No amount given!",
                description = "Please provide an amount of credits that you would want to buy. \nExample: `$buyc <amount>`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif profile[1] >= cost and amount_to_buy != 0:
            self.economy.add_money(user_id, cost*-1)
            self.economy.add_credits(user_id, amount_to_buy)
            await ctx.send(f"You just purchased {amount_to_buy} credits.")
            await ctx.invoke(self.bot.get_command('money'))
        else:
            embed = nextcord.Embed(
                colour = color,
                title = "Not enough money!",
                description = "It seems you don't have enough money to buy a credit. Try doing `$add`, or play some blackjack to get more money."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @buyc.error
    async def buyc_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `$help buyc` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    #Sell credits. Each credit is worth ${DEFAULT_BET}.
    #usage: sellc [amount of credits]
    async def sellc(self, ctx: commands.Context, *, amount_to_sell: int=0):
        user_id = ctx.author.id
        profile = self.economy.get_entry(user_id)
        if amount_to_sell == 0:
            embed = nextcord.Embed(
                colour = color,
                title = "No amount given!",
                description = "Please provide an amount of credits that you would want to sell. \nExample: `$sellc <amount>`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif profile[2] >= amount_to_sell and amount_to_sell != 0:
            self.economy.add_credits(user_id, amount_to_sell*-1)
            self.economy.add_money(user_id, amount_to_sell*DEFAULT_BET)
            await ctx.send(f"You just sold {amount_to_sell} credits.")
            await ctx.invoke(self.bot.get_command('money'))
        else:
            embed = nextcord.Embed(
                colour = color,
                title = "No credits!",
                description = "It seems you don't have any credits to sell. Try buying some credits using `$buyc <amount>`, then play some slots and earn more."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @sellc.error
    async def sellc_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `$help sellc` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `$contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Slots(bot))