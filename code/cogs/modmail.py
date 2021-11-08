from nextcord.ext import commands
from nextcord import utils
import nextcord
import asyncio
from datetime import datetime

log_channel_id = 889293946801516554
color = 0xc48aff

class ContactView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label='Bug Report', style=nextcord.ButtonStyle.red, row=1)
    async def bug_reports(self, message, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Bug Report Ticket Open",
            description = "Please send a detailed report of what bug you have encoutered. \n\nPlease also keep your DMs open and a staff member will get back to you as soon as possible",
            colour = nextcord.Colour.random()   
        )

        await interaction.response.edit_message(embed=embed)

    @nextcord.ui.button(label='Other Issues', style=nextcord.ButtonStyle.red, row=1)
    async def delete(self, message, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title = "Issue Ticket Open",
            description = "Please send a detailed report of what you need help with, or what questions you have about the bot. \n\nPlease also keep your DMs open and a staff member will get back to you as soon as possible",
            colour = nextcord.Colour.random()   
        )

        await interaction.response.edit_message(embed=embed)


class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, nextcord.DMChannel):
            guild = self.bot.get_guild(889027208964874240)
            categ = utils.get(guild.categories, name = "Tickets")
            if not categ:
                overwrites = {
                    guild.default_role : nextcord.PermissionOverwrite(read_messages = False),
                    guild.me : nextcord.PermissionOverwrite(read_messages = True)
                }
                categ = await guild.create_category(name = "Tickets", overwrites = overwrites)

            channel = utils.get(categ.channels, topic = str(message.author.id))
            if not channel:
                channel = await categ.create_text_channel(name = f"{message.author.name}#{message.author.discriminator}", topic = str(message.author.id))
                await channel.send("<@&896911715512487987>")
                embed = nextcord.Embed(
                    description = f"**New Ticket Created By: {message.author.mention}**"
                )
                await channel.send(embed=embed)

            await channel.send(f"{message.content} - [{message.author}]")

        elif isinstance(message.channel, nextcord.TextChannel):
            if message.content.startswith("$"):
                pass
            else:
                topic = message.channel.topic
                if topic:
                    member = message.guild.get_member(int(topic))
                    if member:
                        await member.send(f"{message.content} - [{message.author} ({message.author.top_role})]")


    @commands.command()
    async def contact(self, ctx):
        view = ContactView()
        embed = nextcord.Embed(
            title = "Please choose from one of the options below",
            colour = nextcord.Colour.random()
        )            
        await ctx.message.author.send(embed=embed, view=view)   


    @contact.error
    async def contact_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(
                colour = color,
                title = "→ DMs Turned Off!",
                description="• You are not currently accepting direct messages. Please change this setting, and try again."
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
    async def close(self, ctx):
        if ctx.channel.category.name == "Tickets":
            log = self.bot.get_channel(log_channel_id)
            await ctx.send("Deleting the channel in 5 seconds!")
            await asyncio.sleep(5)
            await ctx.channel.delete()
            embed = nextcord.Embed(
                title = f"{ctx.author} has just closed a ticket",
                colour = nextcord.Colour.magenta()
            )
            await log.send(embed=embed)


def setup(bot):
	bot.add_cog(ModMail(bot))