<img src="./code/utils/AquaBot.png" width="125"/>

# Aqua Bot

Aqua Bot is a great multipurpose Discord bot that offers music with compatibility for Spotify/YouTube/SoundCloud, gambling, an economy system, and even more features. Aqua Bot is no longer in development, but feel free to run it yourself.

Setup: <br>
1. Create a bot at https://discord.com/developers and make sure to get the bot token. 
2. Create a Discord server and make a channel for the feedback and bug messages (can be the same or different channels). After this, make sure to get the channel IDs.
3. Create an account on [Crypto Compare](https://min-api.cryptocompare.com/) and get your free API key.
4. Create PostgreSQL server and create a database. Make sure to note the username, password, host, port, and database name.
5. Create a regular Spotify account and then sign into the developer console [here](https://developer.spotify.com/dashboard/). Then, create an app and get a Spotify ID and secret key.
6. Now, rename the `config.yml.example` to just `config.yml` and fill in all of the necessary information.
7. Open a console and navigate to this folder, and run the command `pip install -r requirements.txt`
8. Now, you must start a lavalink server in order for music functionality. If you do not want to have music functionality, skip to `step 10`
9. Setup a lavalink server, if you are unsure how to do this, you can follow a guide like [this](https://darrennathanael.com/post/how-to-lavalink/). Or, you can connect to a public lavalink server, such as one listed [here](https://lavalink-list.darrennathanael.com/).
<br><br>
Note that if you use a public lavalink server, you must change the login credentials in the `/code/cogs/music.py` file - lines 30-32 and 71.
10. Now you can navigate to the `code` folder and run the bot.py file. On first run your bot will unpack a few zip files, these are dependencies for the gambling features. Then, your bot will connect to Discord and should start.
11. At this point, you will have to sync the slash commands from your bot with Discord. In order to do this you should first sync them to one of your servers specifically by DM'ing the bot `***sync [guild id]`. If you are able to run the commands in your server, then you are ready to sync the commands globally by DM'ing the bot `***sync`. The commands will take ~1 hour to sync globally, then you are completely done with setup. Congratulations!

If you would like to contribute to this project, you can submit a pull request for review.

Thank you for checking out Aqua Bot, have fun coding!

