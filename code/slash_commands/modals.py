from discord.ext import commands
import discord
from discord import app_commands

color = 0xc48aff

class bug_report(discord.ui.Modal, title='Report a bug'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    name = discord.ui.TextInput(
        label='Discord name & tag', 
        placeholder='EX: Fiji#3608...',
    )
    command = discord.ui.TextInput(
        label='Command with error',
        placeholder='EX: blackjack...',
        required=True
    )
    report = discord.ui.TextInput(
        label='A detailed report of the bug',
        style=discord.TextStyle.long,
        placeholder='Type your report here...',
        required=True,
        max_length=500,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your bug report. We will get back to you as soon as possible', ephemeral=True)
        channel = self.bot.get_channel(952349683945205760)

        embed = discord.Embed(
            title = "Bug Report",
            description = f"Submitted by {self.name}",
            color = discord.Color.blurple()
        )
        embed.add_field(name = "Command with issue:", value = f"{self.command}", inline=False)
        embed.add_field(name = "Report:", value = f"{self.report}", inline=False)

        await channel.send(embed=embed)


class feedback_form(discord.ui.Modal, title='Give feedback about Aqua Bot'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    name = discord.ui.TextInput(
        label='Discord name & tag', 
        placeholder='EX: Fiji#3608...',
    )
    positive = discord.ui.TextInput(
        label='What do you like about the bot?',
        style=discord.TextStyle.long,
        placeholder='Your response here...',
        required=True,
        max_length = 500
    )
    negative = discord.ui.TextInput(
        label='What should be changed about the bot?',
        style=discord.TextStyle.long,
        placeholder='Your response here...',
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thank you for your feedback. We love hearing from users!', ephemeral=True)
        channel = self.bot.get_channel(952349715767373844)

        embed = discord.Embed(
            title = "Bot Feedback",
            description = f"Submitted by {self.name}",
            color = discord.Color.blurple()
        )
        embed.add_field(name = "Positive:", value = f"{self.positive}", inline=False)
        embed.add_field(name = "Negative:", value = f"{self.negative}", inline=False)

        await channel.send(embed=embed)


class modals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def bug(self, interaction: discord.Interaction):
        "Send a bug report to the developer"
        await interaction.response.send_modal(bug_report(self.bot))


    @app_commands.command()
    async def feedback(self, interaction: discord.Interaction):
        "Send bot feeback to the developer"
        await interaction.response.send_modal(feedback_form(self.bot))

async def setup(bot):
	await bot.add_cog(modals(bot))