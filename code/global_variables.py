import configparser
import logging
from colorlog import ColoredFormatter
import psycopg2
import discord

log_level = logging.DEBUG
log_format = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

logging.root.setLevel(log_level)
formatter = ColoredFormatter(log_format)

stream = logging.StreamHandler()
stream.setLevel(log_level)
stream.setFormatter(formatter)

LOG = logging.getLogger('pythonConfig')
LOG.setLevel(log_level)
LOG.addHandler(stream)


with open('config.ini', 'r')as f:
    file_contents = f.read()

config = configparser.ConfigParser()
config.read_string(file_contents)

BOT_TOKEN = config['BOT_INFO']['TOKEN']
BONUS_COOLDOWN = int(config['BOT_INFO']['BONUS_COOLDOWN'])
BOT_COLOR = discord.Color(int((config['BOT_INFO']['BOT_COLOR']).replace('#', ""), 16))
BUG_CHANNEL_ID = int(config['BOT_INFO']['BUG_CHANNEL_ID'])
FEEDBACK_CHANNEL_ID = int(config['BOT_INFO']['FEEDBACK_CHANNEL_ID'])

CRYPTO_COMPARE_API_KEY = config['CRYPTO_COMPARE']['API_KEY']

username = config['POSTGRESQL']['USERNAME']
password = config['POSTGRESQL']['PASSWORD']
host = config['POSTGRESQL']['HOST']
port = config['POSTGRESQL']['PORT']
database = config['POSTGRESQL']['DATABASE']
connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
CONNECTION = psycopg2.connect(connection_string)

LAVALINK_HOST = config['LAVALINK']['HOST']
LAVALINK_PORT = config['LAVALINK']['PORT']
LAVALINK_PASSWORD = config['LAVALINK']['PASSWORD']