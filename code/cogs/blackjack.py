import asyncio
import os
import random
from typing import List, Tuple
import discord
from discord.ext import commands
from PIL import Image
from economy_schema import Database
from discord import app_commands
from reader import InsufficientFundsException

Entry = Tuple[int, int]
color = 0xc48aff

class Card:
    suits = ["clubs", "diamonds", "hearts", "spades"]
    def __init__(self, suit: str, value: int, down=False):
        self.suit = suit
        self.value = value
        self.down = down
        self.symbol = self.name[0].upper()

    @property
    def name(self) -> str:
        """The name of the card value."""
        if self.value <= 10: return str(self.value)
        else: return {
            11: 'jack',
            12: 'queen',
            13: 'king',
            14: 'ace',
        }[self.value]

    @property
    def image(self):
        return (
            f"{self.symbol if self.name != '10' else '10'}"\
            f"{self.suit[0].upper()}.png" \
            if not self.down else "red_back.png"
        )

    def flip(self):
        self.down = not self.down
        return self

    def __str__(self) -> str:
        return f'{self.name.title()} of {self.suit.title()}'

    def __repr__(self) -> str:
        return str(self)


class Blackjack(commands.Cog):
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

    @staticmethod
    def hand_to_images(hand: List[Card]) -> List[Image.Image]:
        return ([
            Image.open(f'./code/utils/cards/{card.image}')
            for card in hand
        ])

    @staticmethod
    def center(*hands: Tuple[Image.Image]) -> Image.Image:
        """Creates blackjack table with cards placed"""
        bg: Image.Image = Image.open('./code/utils/table.png')
        bg_center_x = bg.size[0] // 2
        bg_center_y = bg.size[1] // 2

        img_w = hands[0][0].size[0]
        img_h = hands[0][0].size[1]

        start_y = bg_center_y - (((len(hands)*img_h) + \
            ((len(hands) - 1) * 15)) // 2)
        for hand in hands:
            start_x = bg_center_x - (((len(hand)*img_w) + \
                ((len(hand) - 1) * 10)) // 2)
            for card in hand:
                bg.alpha_composite(card, (start_x, start_y))
                start_x += img_w + 10
            start_y += img_h + 15
        return bg

    def output(self, name, *hands: Tuple[List[Card]]) -> None:
        self.center(*map(self.hand_to_images, hands)).save(f'./code/players/tables/{name}.png')

    @staticmethod
    def calc_hand(hand: List[List[Card]]) -> int:
        """Calculates the sum of the card values and accounts for aces"""
        non_aces = [c for c in hand if c.symbol != 'A']
        aces = [c for c in hand if c.symbol == 'A']
        sum = 0
        for card in non_aces:
            if not card.down:
                if card.symbol in 'JQK': sum += 10
                else: sum += card.value
        for card in aces:
            if not card.down:
                if sum <= 10: sum += 11
                else: sum += 1
        return sum


    @app_commands.command()
    @app_commands.describe(bet='Amount of money to bet')
    async def blackjack(
        self,
        interaction: discord.Interaction,
        bet: int
    ):
        "Bet your money on a blackjack game vs. the dealer"

        if f"{interaction.user.id}.png" in os.listdir("./code/players/tables"):
            await interaction.response.send_message(f"{interaction.user.mention}, It appears you have a game already running in this server or another, please finish that game before starting a new one.", ephemeral=True)

        else:
            await self.check_bet(interaction, bet)
            deck = [Card(suit, num) for num in range(2,15) for suit in Card.suits]
            random.shuffle(deck) # Generate deck and shuffle it

            player_hand: List[Card] = []
            dealer_hand: List[Card] = []

            player_hand.append(deck.pop())
            dealer_hand.append(deck.pop())
            player_hand.append(deck.pop())
            dealer_hand.append(deck.pop().flip())

            player_score = self.calc_hand(player_hand)
            dealer_score = self.calc_hand(dealer_hand)

            async def out_table(**kwargs) -> discord.Interaction:
                self.output(f'{interaction.user.id}', dealer_hand, player_hand)
                embed = discord.Embed(**kwargs)
                file = discord.File(
                    f"./code/players/tables/{interaction.user.id}.png", filename=f"{interaction.user.id}.png"
                )
                embed.set_image(url=f"attachment://{interaction.user.id}.png")
                try:
                    msg = await interaction.response.send_message(file=file, embed=embed)
                except:
                    msg = await interaction.edit_original_response(attachments=[file], embed=embed)
                    reac = await interaction.original_response()
                    await reac.clear_reactions()
                return msg

            standing = False

            while True:
                player_score = self.calc_hand(player_hand)
                dealer_score = self.calc_hand(dealer_hand)
                if player_score == 21:  # win condition
                    await self.economy.add_money(interaction.user.id, bet*2)
                    result = (f"Blackjack! - you win ${bet*2}", 'won')
                    break
                elif player_score > 21:  # losing condition
                    await self.economy.add_money(interaction.user.id, bet*-1)
                    result = (f"Player busts - you lose ${bet}", 'lost')
                    break
                msg = await out_table(
                    title="Your Turn",
                    description=f"Your hand: {player_score}\n" \
                        f"Dealer's hand: {dealer_score}"
                )

                reac = await interaction.original_response()
                await reac.add_reaction("🇭")
                await reac.add_reaction("🇸")

                buttons = {"🇭", "🇸"}

                try:
                    reaction, _ = await self.bot.wait_for(
                        'reaction_add', check=lambda reaction, user:user == interaction.user and reaction.emoji in buttons, timeout=60
                    )
                except asyncio.TimeoutError:
                    os.remove(f'./code/players/tables/{interaction.user.id}.png')
                    await interaction.followup.send(f"{interaction.user.mention} your game timed out. No money was lost or gained.")
                    return

                if str(reaction.emoji) == "🇭":
                    player_hand.append(deck.pop())
                    continue
                elif str(reaction.emoji) == "🇸":
                    standing = True
                    break

            if standing:
                dealer_hand[1].flip()
                player_score = self.calc_hand(player_hand)
                dealer_score = self.calc_hand(dealer_hand)

                while dealer_score < 17:  # dealer draws until 17 or greater
                    dealer_hand.append(deck.pop())
                    dealer_score = self.calc_hand(dealer_hand)

                if dealer_score == 21:  # winning/losing conditions
                    await self.economy.add_money(interaction.user.id, bet*-1)
                    result = (f"Dealer blackjack - you lose ${bet}", 'lost')
                elif dealer_score > 21:
                    await self.economy.add_money(interaction.user.id, bet*2)
                    result = (f"Dealer busts - you win ${bet*2}", 'won')
                elif dealer_score == player_score:
                    result = (f"Tie - you keep your money", 'kept')
                elif dealer_score > player_score:
                    await self.economy.add_money(interaction.user.id, bet*-1)
                    result = (f"You lose ${bet}", 'lost')
                elif dealer_score < player_score:
                    await self.economy.add_money(interaction.user.id, bet*2)
                    result = (f"You win ${bet*2}", 'won')

            color = (
                discord.Color.red() if result[1] == 'lost'
                else discord.Color.green() if result[1] == 'won'
                else discord.Color.blue()
            )

            if result[1] == 'won':
                description=(
                    f"**You won ${bet*2:,}**\nYour hand: {player_score}\n" +
                    f"Dealer's hand: {dealer_score}"
                )

            elif result[1] == 'lost':
                description=(
                    f"**You lost ${bet:,}**\nYour hand: {player_score}\n" +
                    f"Dealer's hand: {dealer_score}"
                )

            msg = await out_table(
                title=result[0],
                color=color,
            )
            os.remove(f'./code/players/tables/{interaction.user.id}.png')


async def setup(bot: commands.Bot):
    await bot.add_cog(Blackjack(bot))