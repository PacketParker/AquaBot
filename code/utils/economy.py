import random
import aiosqlite
from functools import wraps
from typing import Tuple, List

Entry = Tuple[int, int]

class Database:
    def __init__(self, bot):
        self.bot = bot

    async def get_entry(self, user_id: int) -> Entry:    
        async with self.bot.db.execute("SELECT * FROM economy WHERE user_id=:user_id", {'user_id': user_id}) as cursor:
            result = await cursor.fetchone()
            if result: 
                return result
            return await self.new_entry(user_id)

    async def new_entry(self, user_id: int) -> Entry:
        try:
            await self.bot.db.execute("INSERT INTO economy(user_id, money) VALUES(?,?)", (user_id, 0))
            await self.bot.db.commit()
            return await self.get_entry(user_id)
        except aiosqlite.IntegrityError:
            return await self.get_entry(user_id)

    async def remove_entry(self, user_id: int) -> None:
        await self.bot.db.execute("DELETE FROM economy WHERE user_id=:user_id", {'user_id': user_id})
        await self.bot.db.commit()

    async def set_money(self, user_id: int, money: int) -> Entry:
        await self.bot.db.execute("UPDATE economy SET money=? WHERE user_id=?", (money, user_id))
        await self.bot.db.commit()
        return await self.get_entry(user_id)

    async def add_money(self, user_id: int, money_to_add: int) -> Entry:
        money = (await self.get_entry(user_id))[1]
        total = money + money_to_add
        if total < 0:
            total = 0
        await self.set_money(user_id, total)
        await self.bot.db.commit()
        return await self.get_entry(user_id)

    async def random_entry(self) -> Entry:
        async with self.bot.db.execute("SELECT * FROM economy") as cursor:
            return random.choice(await cursor.fetchall())

    async def top_entries(self, n: int=0) -> List[Entry]:
        async with self.bot.db.execute("SELECT * FROM economy ORDER BY money DESC") as cursor:
            return(await cursor.fetchmany(n) if n else await cursor.fetchall())