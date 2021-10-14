import random
import sqlite3
from functools import wraps
from typing import Tuple, List

Entry = Tuple[int, int]

class ID:
    """A wrapper for the economy database"""
    def __init__(self):
        self.open()

    def open(self):
        """Initializes the database"""
        self.conn = sqlite3.connect('database/id.db', isolation_level=None)
        self.conn.execute('PRAGMA journal_mode = wal2')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS id (
            guild_id INTEGER NOT NULL PRIMARY KEY,
            mute_id INTEGER NULL,
            channel_id INTEGER NULL
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

    def mute_get_entry(self, guild_id: int, mute_id: int) -> Entry:
        self.cur.execute(
            "SELECT * FROM id WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )
        result = self.cur.fetchone()
        if result: return result
        return self.mute_new_entry(guild_id, mute_id)

    def mute_get_entry_for_commands(self, guild_id: int) -> Entry:
        self.cur.execute(
            "SELECT * FROM id WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )
        result = self.cur.fetchone()
        if result: return result

    @_commit
    def mute_new_entry(self, guild_id: int, mute_id: int) -> Entry:
        try:
            self.cur.execute(
                "INSERT INTO id(guild_id, mute_id) VALUES(?,?)",
                (guild_id, mute_id)
            )
            return self.mute_get_entry(guild_id, mute_id)
        except sqlite3.IntegrityError:
            return self.mute_get_entry(guild_id, mute_id)

    @_commit
    def mute_remove_entry(self, guild_id: int) -> None:
        self.cur.execute(
            "DELETE FROM id WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )

    @_commit
    def set_mute(self, guild_id: int, mute_id: int) -> Entry:
        self.cur.execute(
            "UPDATE id SET mute_id=? WHERE guild_id=?",
            (mute_id, guild_id)
        )
        return self.mute_get_entry(guild_id, mute_id)

    @_commit
    def set_role(self, guild_id: int, mute_id: int) -> Entry:
        self.set_mute(guild_id, mute_id)
        return self.mute_get_entry(guild_id, mute_id)


##BEGIN THE ON_MEMBER_JOIN CODE

    def channel_get_entry(self, guild_id: int, channel_id: int) -> Entry:
        self.cur.execute(
            "SELECT * FROM id WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )
        result = self.cur.fetchone()
        if result: return result
        return self.channel_new_entry(guild_id, channel_id)

    def channel_get_entry_for_commands(self, guild_id: int) -> Entry:
        self.cur.execute(
            "SELECT * FROM id WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )
        result = self.cur.fetchone()
        if result: return result

    @_commit
    def channel_new_entry(self, guild_id: int, channel_id: int) -> Entry:
        try:
            self.cur.execute(
                "INSERT INTO id(guild_id, channel_id) VALUES(?,?)",
                (guild_id, channel_id)
            )
            return self.channel_get_entry(guild_id, channel_id)
        except sqlite3.IntegrityError:
            return self.channel_get_entry(guild_id, channel_id)

    @_commit
    def channel_remove_entry(self, guild_id: int) -> None:
        self.cur.execute(
            "DELETE FROM id WHERE guild_id=:guild_id",
            {'guild_id': guild_id}
        )

    @_commit
    def set_channel_for_channel(self, guild_id: int, channel_id: int) -> Entry:
        self.cur.execute(
            "UPDATE id SET channel_id=? WHERE guild_id=?",
            (channel_id, guild_id)
        )
        return self.channel_get_entry(guild_id, channel_id)

    @_commit
    def set_channel(self, guild_id: int, channel_id: int) -> Entry:
        self.set_channel_for_channel(guild_id, channel_id)
        return self.channel_get_entry(guild_id, channel_id)