from nextcord.ext import commands
import nextcord

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


    @count.error
    async def count_error(self, ctx, error):
        embed = nextcord.Embed(
            colour = color,
            title = "→ You Are Not The Owner!",
            description = f"• You can not run that command because you are not the bot owner."
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Count(bot))