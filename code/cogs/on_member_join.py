import nextcord
from nextcord.ext import commands
from datetime import datetime

log_channel_id = 889293946801516554
color = 0xc48aff

class Join_(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def setjoin(self, ctx: commands.Context, *, channel_name: nextcord.TextChannel):
        guild_id = ctx.author.guild.id
        join = channel_name
        channel_id = join.id
        cursor = await self.bot.db.execute("UPDATE join_channel SET channel_id = ? WHERE guild_id = ?", (channel_id, guild_id))
        await self.bot.db.commit()

        if cursor.rowcount == 0:
            cursor = await self.bot.db.execute("INSERT INTO join_channel (channel_id, guild_id) VALUES(?, ?)", (channel_id, guild_id))
            await self.bot.db.commit()

        embed = nextcord.Embed(
            title = "Join Channel Changed -",
            description = f"<#{channel_id}> has been assigned as the channel for new member message in {ctx.author.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @setjoin.error
    async def setjoin_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        elif isinstance(error, commands.ChannelNotFound):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Channel Not Found!",
                description = f"• That channel wasn't found. Check your spelling, or simply just tag the channel you want to assign for new member messages. Example: `{ctx.prefix}setjoin #channel`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Channel Given!",
                description = f"• It seems you didn't provide a channel for me. Heres an example on how to use the command: `{ctx.prefix}setjoin #channel`, or do `{ctx.prefix}help` for help."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def deljoin(self, ctx: commands.Context):
        guild_id = ctx.author.guild.id
        async with self.bot.db.execute("SELECT channel_id FROM join_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                await self.bot.db.execute(f"DELETE FROM join_channel WHERE guild_id = ?", (guild_id,))
                await self.bot.db.commit()
                embed = nextcord.Embed(
                    title = "New Member Message Channel Deleted -",
                    description = f"The new member message channel for {ctx.author.guild.name} has been deleted.",
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await ctx.send(embed=embed)

            else:
                embed = nextcord.Embed(
                    colour = color,
                    title = "→ Join Channel Not Set!",
                    description = f"• The join channel is not set, therefore there is no channel I can delete."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed)


    @deljoin.error
    async def deljoin_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        embed = nextcord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def joinchannel(self, ctx: commands.Context):
        guild_id = ctx.author.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM join_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = nextcord.Embed(
                    colour = color,
                    title = "→ Join Channel Not Set!",
                    description = f"• The join channel has not yet been set. Ask an admin to set it up using `{ctx.prefix}setjoin`."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed)
                
        if channel_id == None or 0 and not data:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Join Channel Not Set!",
                description = f"• The join channel has not yet been set. Ask an admin to set it up using `{ctx.prefix}setjoin`."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed)

        embed = nextcord.Embed(
            title = f"New member message channel for {ctx.author.guild.name}",
            description= f'<#{channel_id}>'
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @joinchannel.error
    async def joinchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = nextcord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)

        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(
                colour = color,
                title = "→ No Channel Set!",
                description = f"• It seems you haven't set a new member message channel yet. Please go do that with `{ctx.prefix}setjoin` before running this command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = member.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM join_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]

                if channel_id == 0:
                    return

                if channel_id == None:
                    return

                if channel_id == "NULL":
                    return

            elif not data:
                return
 
            channel = self.bot.get_channel(channel_id)

            embed = nextcord.Embed(
                title = f"New Member",
                description = f"Welcome {member.mention} to `{member.guild}`. Thank you for joining our server!",
                colour = nextcord.Colour.random()
            )
            embed.set_footer(text="User joined at: " + datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            embed.set_thumbnail(url=member.avatar.url)

            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Join_(bot))