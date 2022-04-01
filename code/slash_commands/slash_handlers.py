import discord
from discord.ext import commands
from discord.ext.commands.errors import *
from datetime import datetime
from reader import InsufficientFundsException

color = 0xc48aff

class slash_handlers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.on_error = self.on_error

    async def on_error(self, interaction: discord.Interaction, command, error):
        error = getattr(error, 'original', error)

        if isinstance(error, CommandNotFound):
            return

        elif isinstance(error, ZeroDivisionError):
            return

        elif isinstance(error, AttributeError):
            return

        elif isinstance(error, discord.app_commands.errors.MissingPermissions):
            embed = discord.Embed(
                title = "→ Missing Permissions!",
                description = f"• {error}",
                colour = color
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, discord.app_commands.errors.CommandOnCooldown) and interaction.command.name != "slots":
            s = int(error.retry_after)
            s = s % (24 * 3600)
            h = s // 3600
            s %= 3600
            m = s // 60
            s %= 60

            embed = discord.Embed(
                title = "→ Command On Cooldown!",
                description = f"• Please wait another {h}hrs {m}min {s}sec before trying that command again.",
                colour = color
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, discord.app_commands.errors.CommandOnCooldown) and interaction.command.name == "slots":
            embed = discord.Embed(
                title = "→ Slots Cooldown!",
                description = "• To prevent spamming, the slots command in on a 4 second cooldown. Sorry for the inconvenience.",
                colour = color
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, InsufficientFundsException):
            embed = discord.Embed(
                title = "→ Insufficient Funds!",
                description = f"• You do not have enough money to use that command. You can use `/add` to add more money. You can also check your current balance with `/money`",
                colour = color
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, UnboundLocalError):
            await interaction.response.send_message(f"{interaction.user.mention}, your game timed out, no money was lost or gained.", ephemeral=True)
            
        elif not UnboundLocalError or InsufficientFundsException or AttributeError or ZeroDivisionError or CommandNotFound:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `/help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `/bug`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(f"Bot missing permissions \n{error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(slash_handlers(bot))
