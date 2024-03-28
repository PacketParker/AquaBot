import discord
from discord.ext import commands
from discord.ext.commands.errors import *

from bot import InsufficientFundsException
from global_variables import BOT_COLOR


class slash_handlers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.on_error = self.on_error

    async def on_error(self, interaction: discord.Interaction, error):
        error = getattr(error, 'original', error)

        if isinstance(error, CommandNotFound):
            return

        elif isinstance(error, ZeroDivisionError):
            return

        elif isinstance(error, AttributeError):
            return

        elif isinstance(error, InsufficientFundsException):
            embed = discord.Embed(
                title="Insufficient Funds!",
                description=f"You do not have enough money to use that command. You can use `/add` to add more money. You can also check your current balance with `/profile`",
                color=BOT_COLOR
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, BadArgument):
            embed = discord.Embed(
                title="Bad Argument!",
                description=f"The arguments you provided in the command are invalid. Please try again.",
                color=BOT_COLOR
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, discord.app_commands.errors.MissingPermissions):
            embed = discord.Embed(
                title="Missing Permissions!",
                description=f"{error}",
                color=BOT_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, discord.app_commands.errors.BotMissingPermissions):
            embed = discord.Embed(
                title="Bot Missing Permissions!",
                description=f"{error}",
                color=BOT_COLOR
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
                title="Command On Cooldown!",
                description=f"Please wait another {h}hrs {m}min {s}sec before trying that command again.",
                color=BOT_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, discord.app_commands.errors.CommandOnCooldown) and interaction.command.name == "slots":
            embed = discord.Embed(
                title="Slots Cooldown!",
                description="To prevent spamming, the slots command in on a 4 second cooldown. Sorry for the inconvenience.",
                color=BOT_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, UnboundLocalError):
            await interaction.response.send_message(f"{interaction.user.mention}, your game timed out, no money was lost or gained.", ephemeral=True)

        elif isinstance(error, discord.errors.Forbidden) and interaction.command.name in ('kick', 'ban', 'softban'):
            embed = discord.Embed(
                title="Forbidden Error",
                description=f"Moderation actions cannot be performed on the bot, or on members above the bot (like owners or administrators), please try again on users below me.",
                color=BOT_COLOR
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, discord.errors.Forbidden) and interaction.command.name in ('mute', 'tempmute', 'unmute'):
            embed = discord.Embed(
                title="Forbidden Error",
                description=f"I cannot mute or unmute members with a role that is above mine. Please double check that my roles are listed above your servers muted role.",
                color=BOT_COLOR
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)


        elif isinstance(error, discord.errors.Forbidden) and interaction.command.name == 'purge':
            embed = discord.Embed(
                title="Permissions Error",
                description=f"It appears im missing the `manage messages` permissions needed to be able to run the `purge` command..",
                color=BOT_COLOR
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            raise error

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        return


async def setup(bot: commands.Bot):
    await bot.add_cog(slash_handlers(bot))
