import time
import discord
from discord.ext import commands
import datetime
from discord import app_commands
from reader import BOT_COLOR

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command()
    async def invite(
        self,
        interaction: discord.Interaction
    ):
        "Get the invite link for the bot"
        embed = discord.Embed(
            title = "Invite Me To Your Server!",
            description = "Here's the invite for [Aqua Bot](https://discord.com/api/oauth2/authorize?client_id=889027125275922462&permissions=8&scope=bot%20applications.commands)",
            color=BOT_COLOR
        )
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    @app_commands.describe(member="Member whose information you want to view")
    async def userinfo(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        "Send account information for the given user"

        embed = discord.Embed(
            title=f"User Information For {member}",
            color=BOT_COLOR
        )

        roles = [role for role in member.roles]
        roles = f" ".join([f"{role.mention}, " for role in roles])

        embed.set_thumbnail(url = member.avatar.url)
        embed.add_field(name="Account name: ", value=f"`{str(member)}`")
        embed.add_field(name="Discord ID: ", value=f"`{str(member.id)}`")
        embed.add_field(name="Nickname: ", value=f"`{member.nick}`" or "`No nickname!`")
        embed.add_field(name="Account created at: ", value=f"`{member.created_at.strftime('%Y-%m-%d')}`")
        embed.add_field(name="Joined server at: ", value=f"`{member.joined_at.strftime('%Y-%m-%d')}`")

        if member.bot is True:
            embed.add_field(name="Discord bot? ", value="`🤖 = ✅`")
        else:
            embed.add_field(name="Discord bot?", value="`🤖 = ❌`")

        embed.add_field(name="Top role: ", value=f"{member.top_role.mention}")
        embed.add_field(name="Roles: ", inline=False, value=roles)
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")

        try:
            await interaction.response.send_message(embed=embed)

        except discord.errors.HTTPException:
            embed.remove_field(7)
            await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def botinfo(
        self,
        interaction: discord.Interaction
    ):
        "Get information about the bot. i.e. creator, creation data, etc."

        embed = discord.Embed(
            title=f"Bot Information",
            color=BOT_COLOR
        )
        #embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Bot Creator: ", value="`Fiji#3608`"),
        embed.add_field(name="Servers: ", value = f"`{len(self.bot.guilds):,}`"),
        embed.add_field(name="Account name: ", value=f"`{str(self.bot.user.name)}`")
        embed.add_field(name="Discord ID: ", value=f"`{str(self.bot.user.id)}`")
        embed.add_field(name="Bot created at: ", value=f"`{self.bot.user.created_at.strftime('%Y-%m-%d')}`"),
        embed.add_field(name="Aqua Bot Code: ", value="[GitHub Link](https://github.com/Fiji05/AquaBot)")
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def vote(
        self,
        interaction: discord.Interaction
    ):
        "Get link to vote for the bot on top.gg"
        embed = discord.Embed(
            title="Vote for me on top.gg! Voting awards you $10,000!",
            description="[Click here to vote](https://top.gg/bot/889027125275922462)",
            color=BOT_COLOR
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def new(
        self,
        interaction: discord.Interaction
    ):
        "See all of the new changes in the bot"
        embed = discord.Embed(
            title = "Change Log - 2023-02-01",
            description = "Below are all of the changes that have been made to the bot since the last update.",
            color=BOT_COLOR
        )
        embed.add_field(name="New `Give` Command", value="The command, `/give`, has been added, which allows you to give an amount of your money to another member.")
        embed.add_field(name="Slots Redesign", value="The slots game has been redesigned with the help of <@356582138633519114>. Thank you!")
        embed.add_field(name="Embed Color", value="Many of the embed colors are no longer randomized, and have instead been changed to follow the color of the Bot's PFP.")
        embed.add_field(name="Bug Fixes", value="General bug fixes have been applied in order to better the bot's performance.")
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Info(bot))