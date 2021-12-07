from discord.ext import commands
import discord
from datetime import datetime

color = 0xc48aff

class ContactView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Bug Report', style=discord.ButtonStyle.red, row=1)
    async def bug_reports(self, message, interaction: discord.Interaction):
        embed = discord.Embed(
            title = "Bug Report Ticket Open",
            description = "Please send a detailed report of what bug you have encoutered. \n\nPlease also keep your DMs open and a staff member will get back to you as soon as possible",
            colour = discord.Colour.random()   
        )

        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label='Other Issues', style=discord.ButtonStyle.red, row=1)
    async def delete(self, message, interaction: discord.Interaction):
        embed = discord.Embed(
            title = "Issue Ticket Open",
            description = "Please send a detailed report of what you need help with, or what questions you have about the bot. \n\nPlease also keep your DMs open and a staff member will get back to you as soon as possible",
            colour = discord.Colour.random()   
        )

        await interaction.response.edit_message(embed=embed)


class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def contact(self, ctx):
        "Contact the bot owner to report any issues"
        embed = discord.Embed(
            title = "Disabled",
            description = f"Modmail/Contact feature has been temporarily deisabled while I work on ironing out the bugs. For any urgent issues, please join the support server and ping the owner. Do `{ctx.prefix}invite` to get the invite.",
            colour = discord.Colour.random()
        )            
        await ctx.send(embed=embed, ephemeral=True)   


    @contact.error
    async def contact_error(self, ctx, error):
        embed = discord.Embed(
            colour = color,
            title = "→ Error!",
            description = f"• An error occured, try running `{ctx.prefix}help` to see how to use the command. \nIf you believe this is an error, please contact the bot developer through `{ctx.prefix}invite`"
        )
        embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        await ctx.send(embed=embed, ephemeral=True)


def setup(bot):
	bot.add_cog(ModMail(bot))