from discord.ext import commands

class UserCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.dm_only()
    @commands.is_owner()
    async def users(self, ctx: commands.Context):
        members = 0

        for guild in self.bot.guilds:
            members += guild.member_count

        await ctx.author.send(f"Total users: `{members:,}`")


async def setup(bot):
	await bot.add_cog(UserCount(bot))