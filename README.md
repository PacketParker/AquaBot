# Guava

Guava is a great multipurpose Discord bot that is open source and offers all features for free. A list of the features for Guava can be found below.

If you want to invite Guava to your server, use [this link](https://pkrm.dev) - this link needs to be updated!

### Features
1. Music - Play music from YouTube, Spotify, SoundCloud, Deezer, and Bandcamp
2. Moderation - Kick, ban, mute, tempmute, warn, etc.
3. Economy - Global leaderboard to show who has the most money, and buy ranks to show off to others
4. Gambling - Gamble your money at the blackjack table or on the slot machines, or flip a coin
5. Random - Get crypto price data, information on a users Discord account, etc.

<br>

## Selfhost

If you want to selfhost your own version of Guava, follow the instructions below.

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

Once all options are properly configured, you must also setup a Lavalink server in order for the music features to work. For help on setting up a Lavalnk server, follow the docs [here](https://lavalink.dev/getting-started/).

Once your Lavalink server has been configured, you can now, finally, start the bot again by running the `bot.py` file and everything should work.

For support, feel free to contact `fiji3608` on Discord. Have fun coding!