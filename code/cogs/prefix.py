import discord
from discord.ext import commands
from datetime import datetime

color = 0xc48aff

class Prefix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def setprefix(self, 
        ctx: commands.Context,
        *, 
        prefix: str or int=commands.Option(description="New prefix for the bot")
    ):
        "Give the bot a new prefix for your server"
        guild_id = ctx.author.guild.id

        if prefix == None:
            await ctx.send(f"{ctx.author.mention}, you did not give a prefix for me to change to. Please do something like this - `{ctx.prefix}setprefix hh`", ephemeral=True)

        cursor = await self.bot.db.execute("UPDATE prefix SET prefix = ? WHERE guild_id = ?", (prefix, guild_id))
        await self.bot.db.commit()

        if cursor.rowcount == 0:
            cursor = await self.bot.db.execute("INSERT INTO prefix (prefix, guild_id) VALUES(?, ?)", (prefix, guild_id))
            await self.bot.db.commit()

        embed = discord.Embed(
            title = "Prefix Changed -",
            description = f"Prefix has been changed to `{prefix}` for {ctx.author.guild.name}",
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed)

    
    @setprefix.error
    async def setprefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Permissions!",
                description="• You are missing the `manage messages` permission."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        elif isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                colour = color,
                title = "→ Bot Missing Permissions!",
                description = "• I am missing `manage messages` permission. \nAsk an admin to fix this issue."
            )
            embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = color,
                title = "→ Missing Required Argument!",
                description = f"• {error}"
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


def setup(bot):
    bot.add_cog(Prefix(bot))