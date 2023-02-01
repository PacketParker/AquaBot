import time
import discord
from discord.ext import commands
import datetime
from discord import app_commands
from reader import BOT_COLOR

color = 0xc48aff

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
            title = "Change Log - 12/27/2022",
            description = "Below are all of the changes that have been made to the bot since the last update.",
            color=BOT_COLOR
        )

        embed.add_field(name="Work", value = "You now use the `/work` command in order to gain a randomized amount of money (1,000-5,000) every 2 minutes.", inline=True)
        embed.add_field(name="Add Increase", value = "When you use the `/add` command you now get $10,000 rather than $2,500.", inline=True)
        embed.add_field(name="Coinflip", value = "You can now bet your money on a coinflip with the `/coinflip` command.", inline=True)
        embed.add_field(name="Spotify Support", value="You can now play spotify songs/playlists with the `/play` command.")
        embed.add_field(name="Music Redesign", value="The music system has been completely redesigned and now provides better theming and more information.")
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Info(bot))