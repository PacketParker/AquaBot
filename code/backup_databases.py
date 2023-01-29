from reader import CONNECTION_STRING
import psycopg2

"""NOTE: Definately not the greatest way to create a backup for a database, especially not for
large ones, however, it works for now. It also works for both windows and linux since it just uses
the psycopg2 library. Other options did not work for windows because of their use of libraries
which are unsupported on windows/are unix only."""

# Use psycopg2 to connect to the database and create a local backup of everything
connection = psycopg2.connect(CONNECTION_STRING)
cur = connection.cursor()
cur.execute("SELECT * FROM guildData")
guildData = cur.fetchall()
cur.execute("SELECT * FROM mute")
mute = cur.fetchall()
cur.execute("SELECT * FROM tempmute")
tempmute = cur.fetchall()
cur.execute("SELECT * FROM warnings")
warnings = cur.fetchall()
cur.execute("SELECT * FROM economy")
economy = cur.fetchall()
cur.execute("SELECT * FROM profile")
profile = cur.fetchall()
cur.close()
connection.close()

# Write the data to a backup file
with open("backup.sql", "w") as f:
      f.write("DROP TABLE IF EXISTS guildData; CREATE TABLE guildData (guild_id BIGINT, user_id BIGINT, exp BIGINT, PRIMARY KEY (guild_id, user_id));")
      for row in guildData:
            f.write(f"INSERT INTO guildData VALUES ({row[0]}, {row[1]}, {row[2]});")
      f.write("DROP TABLE IF EXISTS mute; CREATE TABLE mute (guild_id BIGINT, role_id BIGINT, PRIMARY KEY (guild_id, role_id));")
      for row in mute:
            f.write(f"INSERT INTO mute VALUES ({row[0]}, {row[1]});")
      f.write("DROP TABLE IF EXISTS tempmute; CREATE TABLE tempmute (guild_id BIGINT, user_id BIGINT, role_id BIGINT, time TIMESTAMP, PRIMARY KEY (guild_id, user_id));")
      for row in tempmute:
            f.write(f"INSERT INTO tempmute VALUES ({row[0]}, {row[1]}, {row[2]}, '{row[3]}');")
      f.write("DROP TABLE IF EXISTS warnings; CREATE TABLE warnings (warn_id BIGINT, guild_id BIGINT, user_id BIGINT, warning TEXT, warn_time DATE, warned_by BIGINT, PRIMARY KEY (warn_id));")
      for row in warnings:
            f.write(f"INSERT INTO warnings VALUES ({row[0]}, {row[1]}, {row[2]}, '{row[3]}', '{row[4]}', {row[5]});")
      f.write("DROP TABLE IF EXISTS economy; CREATE TABLE economy (guild_id BIGINT, user_id BIGINT, balance BIGINT, PRIMARY KEY (guild_id, user_id));")
      for row in economy:
            f.write(f"INSERT INTO economy VALUES ({row[0]}, {row[1]});")
      f.write("DROP TABLE IF EXISTS profile; CREATE TABLE profile (guild_id BIGINT, user_id BIGINT, bio TEXT, PRIMARY KEY (guild_id, user_id));")
      for row in profile:
            f.write(f"INSERT INTO profile VALUES ({row[0]}, {row[1]}, '{row[2]}');")