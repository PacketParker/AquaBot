import random
import sqlite3
from functools import wraps
from typing import Tuple, List

Entry = Tuple[int, int]

class Database:
    def __init__(self):
        self.open()

    def open(self):
        """Initializes the database"""
        self.conn = sqlite3.connect('database/database.db', isolation_level=None)
        self.conn.execute('PRAGMA journal_mode = wal2')
        self.curMute = self.conn.cursor()
        self.curMute.execute("""CREATE TABLE IF NOT EXISTS mute (
            guild_id INTEGER NOT NULL PRIMARY KEY,
            mute_id INTEGER NULL
        )""")
        self.curJoin = self.conn.cursor()
        self.curJoin.execute("""CREATE TABLE IF NOT EXISTS channel (
            guild_id INTEGER NOT NULL PRIMARY KEY,
            channel_id INTEGER NULL
        )""")
        self.curEconomy = self.conn.cursor()
        self.curEconomy.execute("""CREATE TABLE IF NOT EXISTS economy (
            user_id INTEGER NOT NULL PRIMARY KEY,
            money INTEGER NOT NULL DEFAULT 0
        )""")

    def close(self):
        """Safely closes the database"""
        if self.conn:
            self.conn.commit()
            self.curMute.close()
            self.curJoin.close()
            self.curEconomy.close()
            self.conn.close()

    def _commit(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.conn.commit()
            return result
        return wrapper

    def mute_get_entry(self, guild_id: int, mute_id: int) -> Entry:
        self.curMute.execute(
            "SELECT * FROM mute WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )
        result = self.curMute.fetchone()
        if result: return result
        return self.mute_new_entry(guild_id, mute_id)

    def mute_get_entry_for_commands(self, guild_id: int) -> Entry:
        self.curMute.execute(
            "SELECT * FROM mute WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )
        result = self.curMute.fetchone()
        if result: return result

    @_commit
    def mute_new_entry(self, guild_id: int, mute_id: int) -> Entry:
        try:
            self.curMute.execute(
                "INSERT INTO mute(guild_id, mute_id) VALUES(?,?)",
                (guild_id, mute_id)
            )
            return self.mute_get_entry(guild_id, mute_id)
        except sqlite3.IntegrityError:
            return self.mute_get_entry(guild_id, mute_id)

    @_commit 
    def mute_remove_entry(self, guild_id: int) -> None:
        self.curMute.execute(
            "DELETE FROM mute WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )

    @_commit
    def set_mute(self, guild_id: int, mute_id: int) -> Entry:
        self.curMute.execute(
            "UPDATE mute SET mute_id=? WHERE guild_id=?",
            (mute_id, guild_id)
        )
        return self.mute_get_entry(guild_id, mute_id)

    @_commit
    def set_role(self, guild_id: int, mute_id: int) -> Entry:
        self.set_mute(guild_id, mute_id)
        return self.mute_get_entry(guild_id, mute_id)


##BEGIN THE ON_MEMBER_JOIN CODE


    def channel_get_entry(self, guild_id: int, channel_id: int) -> Entry:
        self.curJoin.execute(
            "SELECT * FROM channel WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )
        result = self.curJoin.fetchone()
        if result: return result
        return self.channel_new_entry(guild_id, channel_id)

    def channel_get_entry_for_commands(self, guild_id: int) -> Entry:
        self.curJoin.execute(
            "SELECT * FROM channel WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )
        result = self.curJoin.fetchone()
        if result: return result

    @_commit
    def channel_new_entry(self, guild_id: int, channel_id: int) -> Entry:
        try:
            self.curJoin.execute(
                "INSERT INTO channel(guild_id, channel_id) VALUES(?,?)",
                (guild_id, channel_id)
            )
            return self.channel_get_entry(guild_id, channel_id)
        except sqlite3.IntegrityError:
            return self.channel_get_entry(guild_id, channel_id)

    @_commit
    def channel_remove_entry(self, guild_id: int) -> None:
        self.curJoin.execute(
            "DELETE FROM channel WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )

    @_commit
    def set_channel_for_channel(self, guild_id: int, channel_id: int) -> Entry:
        self.curJoin.execute(
            "UPDATE channel SET channel_id=? WHERE guild_id=?",
            (channel_id, guild_id)
        )
        return self.channel_get_entry(guild_id, channel_id)

    @_commit
    def set_channel(self, guild_id: int, channel_id: int) -> Entry:
        self.set_channel_for_channel(guild_id, channel_id)
        return self.channel_get_entry(guild_id, channel_id)


##BEGIN ECONOMY CODE


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

