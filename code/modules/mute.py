import random
import sqlite3
from functools import wraps
from typing import Tuple, List

Entry = Tuple[int, int]

class Mute:
    """A wrapper for the economy database"""
    def __init__(self):
        self.open()

    def open(self):
        """Initializes the database"""
        self.conn = sqlite3.connect('mute.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS mute (
            mute_guild_id INTEGER NOT NULL PRIMARY KEY,
            mute_id INTEGER NULL
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

    def get_entry(self, mute_guild_id: int, mute_id: int) -> Entry:
        self.cur.execute(
            "SELECT * FROM mute WHERE mute_guild_id=:mute_guild_id",
            {'mute_guild_id': mute_guild_id}
        )
        result = self.cur.fetchone()
        if result: return result
        return self.new_entry(mute_guild_id, mute_id)

    def get_entry_for_whatmute(self, mute_guild_id: int) -> Entry:
        self.cur.execute(
            "SELECT * FROM mute WHERE mute_guild_id=:mute_guild_id",
            {'mute_guild_id': mute_guild_id}
        )
        result = self.cur.fetchone()
        if result: return result

    def get_entry_for_mute(self, mute_guild_id: int) -> Entry:
        self.cur.execute(
            "SELECT * FROM mute WHERE mute_guild_id=:mute_guild_id",
            {'mute_guild_id': mute_guild_id}
        )
        result = self.cur.fetchone()
        if result: return result

    @_commit
    def new_entry(self, mute_guild_id: int, mute_id: int) -> Entry:
        try:
            self.cur.execute(
                "INSERT INTO mute(mute_guild_id, mute_id) VALUES(?,?)",
                (mute_guild_id, mute_id)
            )
            return self.get_entry(mute_guild_id, mute_id)
        except sqlite3.IntegrityError:
            return self.get_entry(mute_guild_id, mute_id)

    @_commit
    def remove_entry(self, mute_guild_id: int) -> None:
        self.cur.execute(
            "DELETE FROM mute WHERE mute_guild_id=:mute_guild_id",
            {'mute_guild_id': mute_guild_id}
        )

    @_commit
    def set_mute(self, mute_guild_id: int, mute_id: int) -> Entry:
        self.cur.execute(
            "UPDATE mute SET mute_id=? WHERE mute_guild_id=?",
            (mute_id, mute_guild_id)
        )
        return self.get_entry(mute_guild_id, mute_id)

    @_commit
    def set_role(self, mute_guild_id: int, mute_id: int) -> Entry:
        self.set_mute(mute_guild_id, mute_id)
        return self.get_entry(mute_guild_id, mute_id)
