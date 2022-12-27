from discord.ext import commands
import aiosqlite

class Count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction, command):
        cur = await aiosqlite.connect("code/count/count.db")
        await cur.execute("UPDATE count SET count = count + 1")
        await cur.commit()


async def setup(bot):
	await bot.add_cog(Count(bot))