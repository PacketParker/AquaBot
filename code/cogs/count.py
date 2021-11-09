import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions
from nextcord.utils import get
from aiohttp import request

log_channel_id = 889293946801516554

black = 0x000000
color = 0xc48aff

class Count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        async with self.bot.db.execute("SELECT count FROM counter WHERE bot_id = ?", (self.bot.user.id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                count = data[0]
                await self.bot.db.execute("UPDATE counter SET count = ? WHERE bot_id = ?", (count+1, self.bot.user.id))
                await self.bot.db.commit()

            else:
                await self.bot.db.execute("INSERT INTO counter (bot_id, count) VALUES(?, ?)", (self.bot.user.id, 0))
                await self.bot.db.commit()

                async with self.bot.db.execute("SELECT count FROM counter WHERE bot_id = ?", (self.bot.user.id,)) as cursor:
                    data = await cursor.fetchone()
                    count = data[0]
                    await self.bot.db.execute("UPDATE counter SET count = ? WHERE bot_id = ?", (count+1, self.bot.user.id))
                    await self.bot.db.commit()


    @commands.command()
    @commands.is_owner()
    async def count(self, ctx):
        async with self.bot.db.execute("SELECT count FROM counter WHERE bot_id = ?", (self.bot.user.id,)) as cursor:
            data = await cursor.fetchone()
            count = data[0]

        await ctx.send(f"{count:,}")


def setup(bot):
    bot.add_cog(Count(bot))