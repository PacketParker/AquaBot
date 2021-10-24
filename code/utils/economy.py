import random
import sqlite3
from functools import wraps
from typing import Tuple, List

Entry = Tuple[int, int]

class Database:
    def __init__(self):
        self.open()

    def open(self):
        self.conn = sqlite3.connect('database/data.db', isolation_level=None)
        self.conn.execute('PRAGMA journal_mode = wal2')
        self.curEconomy = self.conn.cursor()
        self.curEconomy.execute("""CREATE TABLE IF NOT EXISTS economy (
            user_id INTEGER NOT NULL PRIMARY KEY,
            money INTEGER NOT NULL DEFAULT 0
        )""")


    def close(self):
        """Safely closes the database"""
        if self.conn:
            self.conn.commit()
            self.curEconomy.close()
            self.conn.close()

    def _commit(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.conn.commit()
            return result
        return wrapper

    def get_entry(self, user_id: int) -> Entry:
        self.curEconomy.execute(
            "SELECT * FROM economy WHERE user_id=:user_id",
            {'user_id': user_id}
        )
        result = self.curEconomy.fetchone()
        if result: return result
        return self.new_entry(user_id)

    @_commit
    def new_entry(self, user_id: int) -> Entry:
        try:
            self.curEconomy.execute(
                "INSERT INTO economy(user_id, money) VALUES(?,?)",
                (user_id, 0)
            )
            return self.get_entry(user_id)
        except sqlite3.IntegrityError:
            return self.get_entry(user_id)

    @_commit
    def remove_entry(self, user_id: int) -> None:
        self.curEconomy.execute(
            "DELETE FROM economy WHERE user_id=:user_id",
            {'user_id': user_id}
        )

    @_commit
    def set_money(self, user_id: int, money: int) -> Entry:
        self.curEconomy.execute(
            "UPDATE economy SET money=? WHERE user_id=?",
            (money, user_id)
        )
        return self.get_entry(user_id)

    @_commit
    def add_money(self, user_id: int, money_to_add: int) -> Entry:
        money = self.get_entry(user_id)[1]
        total = money + money_to_add
        if total < 0:
            total = 0
        self.set_money(user_id, total)
        return self.get_entry(user_id)

    def random_entry(self) -> Entry:
        self.curEconomy.execute("SELECT * FROM economy")
        return random.choice(self.curEconomy.fetchall())

    def top_entries(self, n: int=0) -> List[Entry]:
        self.curEconomy.execute("SELECT * FROM economy ORDER BY money DESC")
        return (self.curEconomy.fetchmany(n) if n else self.curEconomy.fetchall())