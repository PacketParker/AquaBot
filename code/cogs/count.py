from discord.ext import commands, tasks
import aiosqlite

class Count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.dump_count.start()


    @tasks.loop(seconds=10)
    async def dump_count(self):
        cur = await aiosqlite.connect("./code/count/count.db")
        count = await cur.execute("SELECT count FROM count")
        count = await count.fetchone()
        if count is None:
            await cur.execute("INSERT INTO count (count) VALUES (?)", (self.bot.count_hold,))
        else:
            await cur.execute("UPDATE count SET count = count + ?", (self.bot.count_hold,))
        self.bot.count_hold = 0
        await cur.commit()
        await cur.close()


    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction, command):
        self.bot.count_hold += 1


async def setup(bot):
	await bot.add_cog(Count(bot))