<h1 align="center">
  <br>
  <img src="AquaBot.png" width="250" alt="Aqua Bot Image"></a>
  <br>
  Aqua Bot<br>
</h1>

<h3 align="center">
    Multipurpse Discord bot made on d.py
</h3>

<p align="center">
  <a href="https://github.com/Rapptz/discord.py/">
     <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
  </a>
</p>

# Aqua Bot

Aqua Bot is a great multipurpose Discord bot that is open source and offers all features for free. A list of the features for Aqua Bot can be found below.

Aqua Bot is no longer under development and does not run anymore. Attention has been switched to the music only Discord bot, Guava, which can be found [here](https://github.com/packetparker/guava)

### Features
- Music - Play music from YouTube, Spotify, SoundCloud, Deezer, and Bandcamp
- Moderation - Kick, ban, mute, tempmute, warn, etc.
- Economy - Global leaderboard to show who has the most money, and buy ranks to show off to others
- Gambling - Gamble your money at the blackjack table or on the slot machines, or flip a coin
- Random - Get crypto price data, information on a users Discord account, etc.

<br>

## Selfhost

If you want to selfhost your own version of Aqua Bot, follow the instructions below.

Downlooad the code and install the necessary dependencies using pip (ex: `pip install -r requirements.txt`)

On first run, you will likely get a critical warning in your console, don't worry, this is excepted. It will automatically create a `config.ini` file for you in the root of the directory with all of the necessary configuration options.

Fill out all of the configuration options, ALL options must be filled out. For help on what each option does, look at the table below.

### BOT_INFO Configuration

Field | Description
--- | ---
TOKEN | The token for your bot
BONUS_COOLDOWN | Cooldown time, in hours, between uses of the `/add` command, which gives users $10,000
BOT_COLOR | Hex color code for the color used on most of the message embeds
BUG_CHANNEL_ID | Channel ID for the bug reporting channel
FEEDBACK_CHANNEL_ID | Channel ID for the feedback message channel

### CRYPTO_COMPARE Configuration
Field | Description
--- | ---
API_KEY | API key from your CryptoCompare account. Can be aquired [here](https://min-api.cryptocompare.com/).

### POSTGESQL Configuration
Field | Description
--- | ---
USERNAME | Username for login
PASSWORD | Password for login
HOST | Host for connecting to database
PORT | Port for connecting to database
DATABASE | Name of the database to be used

### LAVALINK Configuration
Field | Description
--- | ---
HOST | Host for connecting to Lavalink
PORT | Port for connecting to Lavalink
PASSWORD | Password for login

### SPOTIFY CONFIGURATION
Field | Description
--- | ---
CLIENT_ID | Client ID given to you from Spotify Developer Dashboard
CLIENT_SECRET | Client Secret, found in the same place

Once all options are properly configured, you must also setup a Lavalink server in order for the music features to work. For help on setting up a Lavalnk server, follow the docs [here](https://lavalink.dev/getting-started/).

Once your Lavalink server has been configured, you can now, finally, start the bot again by running the `bot.py` file and everything should work.

For support, feel free to contact `fiji3608` on Discord. Have fun coding!
