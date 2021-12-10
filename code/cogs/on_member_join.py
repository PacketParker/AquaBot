import discord
from discord.ext import commands
from datetime import datetime

color = 0xc48aff

class Join_(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def setjoin(self,     
        ctx: commands.Context, 
        channel: discord.TextChannel=commands.Option(description="Channel where you want new member messages be sent")
    ):
        "Set the channel for new member messages"
        guild_id = ctx.author.guild.id
        join = channel
        channel_id = join.id
        cursor = await self.bot.db.execute("UPDATE join_channel SET channel_id = ? WHERE guild_id = ?", (channel_id, guild_id))
        await self.bot.db.commit()

        if cursor.rowcount == 0:
            cursor = await self.bot.db.execute("INSERT INTO join_channel (channel_id, guild_id) VALUES(?, ?)", (channel_id, guild_id))
            await self.bot.db.commit()

        embed = discord.Embed(
            title = "Join Channel Changed -",
            description = f"<#{channel_id}> has been assigned as the channel for new member message in {ctx.author.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @setjoin.error
    async def setjoin_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.ChannelNotFound):
            embed = discord.Embed(
                colour = color,
                title = "→ Channel Not Found!",
                description = f"• That channel wasn't found. Check your spelling, or simply just tag the channel you want to assign for new member messages. Example: `{ctx.prefix}setjoin #channel`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ No Channel Given!",
                description = f"• It seems you didn't provide a channel for me. Heres an example on how to use the command: `{ctx.prefix}setjoin #channel`, or do `{ctx.prefix}help` for help."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def deljoin(self, ctx: commands.Context):
        "Delete the new member channel so messages are no longer sent"
        guild_id = ctx.author.guild.id
        async with self.bot.db.execute("SELECT channel_id FROM join_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                await self.bot.db.execute(f"DELETE FROM join_channel WHERE guild_id = ?", (guild_id,))
                await self.bot.db.commit()
                embed = discord.Embed(
                    title = "New Member Message Channel Deleted -",
                    description = f"The new member message channel for {ctx.author.guild.name} has been deleted.",
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Join Channel Not Set!",
                    description = f"• The join channel is not set, therefore there is no channel I can delete."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed, ephemeral=True)


    @deljoin.error
    async def deljoin_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        else:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def joinchannel(self, ctx: commands.Context):
        "See the current channel set for new member messages"
        guild_id = ctx.author.guild.id

        async with self.bot.db.execute("SELECT channel_id FROM join_channel WHERE guild_id = ?", (guild_id,)) as cursor:
            data = await cursor.fetchone()
            if data:
                channel_id = data[0]
            else:
                embed = discord.Embed(
                    colour = color,
                    title = "→ Join Channel Not Set!",
                    description = f"• The join channel has not yet been set. Ask an admin to set it up using `{ctx.prefix}setjoin`."
                )
                embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                return await ctx.send(embed=embed, ephemeral=True)
                
        if channel_id == None or 0 and not data:
            embed = discord.Embed(
                colour = color,
                title = "→ Join Channel Not Set!",
                description = f"• The join channel has not yet been set. Ask an admin to set it up using `{ctx.prefix}setjoin`."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            return await ctx.send(embed=embed, ephemeral=True)

        embed = discord.Embed(
            title = f"New member message channel for {ctx.author.guild.name}",
            description= f'<#{channel_id}>'
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)


    @joinchannel.error
    async def joinchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage channels` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage channels` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ No Channel Set!",
                description = f"• It seems you haven't set a new member message channel yet. Please go do that with `{ctx.prefix}setjoin` before running this command."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                colour = color,
                title = "→ Error!",
                description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}contact`"
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)


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

            embed = discord.Embed(
                title = f"New Member",
                description = f"Welcome {member.mention} to `{member.guild}`. Thank you for joining our server!",
                colour = discord.Colour.random()
            )
            embed.set_footer(text="User joined at: " + datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            embed.set_thumbnail(url=member.avatar.url)

            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Join_(bot))