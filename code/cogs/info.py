import time
import discord
from discord.ext import commands
import datetime
from discord import app_commands

from global_variables import BOT_COLOR


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


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
        "Get information about the bot. i.e. number of servers, creation date, etc."

        embed = discord.Embed(
            title=f"Bot Information",
            color=BOT_COLOR
        )
        #embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Servers: ", value = f"`{len(self.bot.guilds):,}`"),
        embed.add_field(name="Account name: ", value=f"`{str(self.bot.user.name)}`")
        embed.add_field(name="Discord ID: ", value=f"`{str(self.bot.user.id)}`")
        embed.add_field(name="Bot created at: ", value=f"`{self.bot.user.created_at.strftime('%Y-%m-%d')}`"),
        embed.set_footer(text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))