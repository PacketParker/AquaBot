import random
import sqlite3
from functools import wraps
from typing import Tuple, List

Entry = Tuple[int, int]

class Join:
    """A wrapper for the economy database"""
    def __init__(self):
        self.open()

    def open(self):
        """Initializes the database"""
        self.conn = sqlite3.connect('database/join.db', isolation_level=None)
        self.conn.execute('PRAGMA journal_mode = wal2')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS join (
            join_guild_id INTEGER NOT NULL PRIMARY KEY,
            join_id INTEGER NULL
        )""")

    def close(self):
        """Safely closes the database"""
        if self.conn:
            self.conn.commit()
            self.cur.close()
            self.conn.close()

    def _commit(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.conn.commit()
            return result
        return wrapper

    def get_entry(self, join_guild_id: int, join_id: int) -> Entry:
        self.cur.execute(
            "SELECT * FROM join WHERE join_guild_id=:join_guild_id",
            {'join_guild_id': join_guild_id}
        )
        result = self.cur.fetchone()
        if result: return result
        return self.new_entry(join_guild_id, join_id)

    def get_entry_for_commands(self, join_guild_id: int) -> Entry:
        self.cur.execute(
            "SELECT * FROM join WHERE join_guild_id=:join_guild_id",
            {'join_guild_id': join_guild_id}
        )
        result = self.cur.fetchone()
        if result: return result

    @_commit
    def new_entry(self, join_guild_id: int, join_id: int) -> Entry:
        try:
            self.cur.execute(
                "INSERT INTO join(join_guild_id, join_id) VALUES(?,?)",
                (join_guild_id, join_id)
            )
            return self.get_entry(join_guild_id, join_id)
        except sqlite3.IntegrityError:
            return self.get_entry(join_guild_id, join_id)

    @_commit
    def remove_entry(self, join_guild_id: int) -> None:
        self.cur.execute(
            "DELETE FROM join WHERE join_guild_id=:join_guild_id",
            {'join_guild_id': join_guild_id}
        )

    @_commit
    def set_channel_for_channel(self, join_guild_id: int, join_id: int) -> Entry:
        self.cur.execute(
            "UPDATE join SET join_id=? WHERE join_guild_id=?",
            (join_id, join_guild_id)
        )
        return self.get_entry(join_guild_id, join_id)

    @_commit
    def set_channel(self, join_guild_id: int, join_id: int) -> Entry:
        self.set_channel_for_channel(join_guild_id, join_id)
        return self.get_entry(join_guild_id, join_id)
