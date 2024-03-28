import configparser
import re

from global_variables import LOG


pattern_1 = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
pattern_2 = "^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"

def validate_config(file_contents):
    config = configparser.ConfigParser()
    config.read_string(file_contents)

    errors = 0

    try:
        # Validate TOKEN
        if not config['BOT_INFO']['TOKEN']:
            LOG.critical("TOKEN has not been set.")
            errors += 1
        # Validate BONUS_COOLDOWN
        if not config['BOT_INFO']['BONUS_COOLDOWN']:
            LOG.critical("BONUS_COOLDOWN has not been set.")
            errors += 1

        else:
            try:
                int(config['BOT_INFO']['BONUS_COOLDOWN'])
            except ValueError:
                LOG.critical("BONUS_COOLDOWN must be an integer value.")
                errors += 1
        # Validate BOT_COLOR
        if not config['BOT_INFO']['BOT_COLOR']:
            LOG.critical("BOT_COLOR has not been set.")
            errors += 1

        elif not bool(re.match(pattern_1, config['BOT_INFO']['BOT_COLOR'])) and not bool(re.match(pattern_2, config['BOT_INFO']['BOT_COLOR'])):
            LOG.critical("BOT_COLOR is not a valid hex color.")
            errors += 1
        # Validate BUG_CHANNEL_ID
        if not config['BOT_INFO']['BUG_CHANNEL_ID']:
            LOG.critical("BUG_CHANNEL_ID has not been set.")
            errors += 1

        elif len(str(config['BOT_INFO']['BUG_CHANNEL_ID'])) != 19:
            LOG.critical("BUG_CHANNEL_ID is not a valid Discord text channel ID.")
            errors += 1

        else:
            try:
                int(config['BOT_INFO']['BUG_CHANNEL_ID'])
            except ValueError:
                LOG.critical("BUG_CHANNEL_ID should be an integer value, not a string.")
                errors += 1
        # Validate FEEDBACK_CHANNEL_ID
        if not config['BOT_INFO']['FEEDBACK_CHANNEL_ID']:
            LOG.critical("FEEDBACK_CHANNEL_ID has not been set.")
            errors += 1

        elif len(str(config['BOT_INFO']['FEEDBACK_CHANNEL_ID'])) != 19:
            LOG.critical("FEEDBACK_CHANNEL_ID is not a valid Discord text channel ID.")
            errors += 1

        else:
            try:
                int(config['BOT_INFO']['FEEDBACK_CHANNEL_ID'])
            except ValueError:
                LOG.critical("FEEDBACK_CHANNEL_ID should be an integer value, not a string.")
                errors += 1
        # Validate API_KEY
        if not config['CRYPTO_COMPARE']['API_KEY']:
            LOG.critical("API_KEY has not been set.")
            errors += 1
        # Validate USERNAME
        if not config['POSTGRESQL']['USERNAME']:
            LOG.critical("USERNAME has not been set.")
            errors += 1
        # Validate PASSWORD
        if not config['POSTGRESQL']['PASSWORD']:
            LOG.critical("PASSWORD has not been set.")
            errors += 1
        # Validate HOST
        if not config['POSTGRESQL']['HOST']:
            LOG.critical("HOST has not been set.")
            errors += 1
        # Validate PORT
        if not config['POSTGRESQL']['PORT']:
            LOG.critical("PORT has not been set.")
            errors += 1
        # Validate DATABASE
        if not config['POSTGRESQL']['DATABASE']:
            LOG.critical("DATABASE has not been set.")
            errors += 1

        # Validate LAVALINK
        # Validate HOST
        if not config['LAVALINK']['HOST']:
            LOG.critical("HOST has not been set.")
            errors += 1
        # Validate PORT
        if not config['LAVALINK']['PORT']:
            LOG.critical("PORT has not been set.")
            errors += 1
        # Validate PASSWORD
        if not config['LAVALINK']['PASSWORD']:
            LOG.critical("HOST has not been set.")
            errors += 1

        if errors > 0:
            LOG.info(f"Program exiting with {errors} critical {'errors' if errors > 1 else 'error'}")
            exit()

        else:
            LOG.info("Configuration checks passed. Starting bot.")


    except KeyError:
        LOG.critical("You are missing at least one of the configuration options from your config.ini file. In order to regenerate this file with all of the proper options, please delete it and re-run the `bot.py` file.")
        exit()


def create_config():
    try:
        with open('config.ini', 'r') as f:
            file_contents = f.read()
            validate_config(file_contents)

    except FileNotFoundError:
        config = configparser.ConfigParser()
        config['BOT_INFO'] = {
            'TOKEN': '',
            'BONUS_COOLDOWN': '',
            'BOT_COLOR': '',
            'BUG_CHANNEL_ID': '',
            'FEEDBACK_CHANNEL_ID': ''
        }

        config['CRYPTO_COMPARE'] = {
            'API_KEY': ''
        }

        config['POSTGRESQL'] = {
            'USERNAME': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            'DATABASE': ''
        }

        config['LAVALINK'] = {
            'HOST': '',
            'PORT': '',
            'PASSWORD': ''
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        LOG.error("Configuration file `config.ini` has been generated. Please fill out all of the necessary information. Refer to the docs for information on what a specific configuration option is.")
        exit()