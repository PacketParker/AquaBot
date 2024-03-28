import aiosqlite
import random
from typing import Tuple, List

from global_variables import CONNECTION


async def init_database():
    cur = CONNECTION.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id BIGINT, user_id BIGINT, exp BIGINT, PRIMARY KEY (guild_id, user_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS mute (guild_id BIGINT, role_id BIGINT, PRIMARY KEY (guild_id, role_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS tempmute (guild_id BIGINT, user_id BIGINT, role_id BIGINT, time TIMESTAMP, PRIMARY KEY (guild_id, user_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS warnings (warn_id BIGINT, guild_id BIGINT, user_id BIGINT, warning TEXT, warn_time DATE, warned_by BIGINT, PRIMARY KEY (warn_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS economy (user_id BIGINT NOT NULL PRIMARY KEY, money BIGINT NOT NULL DEFAULT 0)")
    cur.execute("CREATE TABLE IF NOT EXISTS profile (user_id BIGINT, rank_name TEXT, rank_int BIGINT, UNIQUE (user_id, rank_name, rank_int))")
    CONNECTION.commit()

    cur = await aiosqlite.connect("code/count/count.db")
    await cur.execute("CREATE TABLE IF NOT EXISTS count (count INTEGER)")
    await cur.commit()
    await cur.close()


Entry = Tuple[int, int]

class Database:
    def __init__(self, bot):
        self.bot = bot

    async def get_entry(self, user_id: int) -> Entry:
        cur = CONNECTION.cursor()
        cur.execute("SELECT * FROM economy WHERE user_id = %s", (user_id,))
        result = cur.fetchone()
        if result:
            return result
        return await self.new_entry(user_id)

    async def new_entry(self, user_id: int) -> Entry:
        try:
            cur = CONNECTION.cursor()
            cur.execute("INSERT INTO economy(user_id, money) VALUES(%s, %s)", (user_id, 0))
            CONNECTION.commit()
            return await self.get_entry(user_id)
        except:
            return await self.get_entry(user_id)

    async def remove_entry(self, user_id: int) -> None:
        cur = CONNECTION.cursor()
        cur.execute("DELETE FROM economy WHERE user_id = %s", (user_id,))
        CONNECTION.commit()

    async def set_money(self, user_id: int, money: int) -> Entry:
        cur = CONNECTION.cursor()
        cur.execute("UPDATE economy SET money = %s WHERE user_id = %s", (money, user_id))
        CONNECTION.commit()
        return await self.get_entry(user_id)

    async def add_money(self, user_id: int, money_to_add: int) -> Entry:
        money = (await self.get_entry(user_id))[1]
        total = money + money_to_add
        if total < 0:
            total = 0
        await self.set_money(user_id, total)
        return await self.get_entry(user_id)

    async def random_entry(self) -> Entry:
        cur = CONNECTION.cursor()
        cur.execute("SELECT * FROM economy")
        return random.choice(cur.fetchall())

    async def top_entries(self, n: int=0) -> List[Entry]:
        cur = CONNECTION.cursor()
        cur.execute("SELECT * FROM economy ORDER BY money DESC")
        return cur.fetchmany(n) if n else cur.fetchall()