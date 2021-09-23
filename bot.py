import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import json
import time
import random

log_channel_id = 889293946801516554

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')



async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['warns'] = 0
        users[f'{user.id}']['mod'] = []
        users[f'{user.id}']['reason'] = []
        users[f'{user.id}']['time'] = []
        users[f'{user.id}']['warn_id'] = []

async def add_warns(users, user, warns):
    users[f'{user.id}']['warns'] += warns

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, user:discord.Member, *, args):

    reason = ''.join(args) #to get the full reason
    with open('warns.json', 'r') as f:
        users = json.load(f)

    await update_data(users, user)
    await add_warns(users, user, 1)
    random_id = random.randint(10000, 99999)
    warndate = time.strftime("%A, %B %d %Y @ %H:%M:%S %p")
    users[f'{user.id}']['mod'].append(ctx.author.id)
    users[f'{user.id}']['reason'].append(reason)
    users[f'{user.id}']['time'].append(warndate)
    users[f'{user.id}']['warn_id'].append(random_id)


    await ctx.send(f"{user.mention} has been warned!")

    with open('warns.json', 'w') as f:
         json.dump(users, f, sort_keys=True, ensure_ascii=False, indent=4, default=str)


@bot.command()
@commands.has_permissions(administrator=True)
async def warnings(ctx, user:discord.Member):
    try:
        with open('warns.json', 'r') as f:
            users = json.load(f)

        warns = users[f'{user.id}']['warns']
        moderator = users[f'{user.id}']['mod']
        warn_reason = users[f'{user.id}']['reason']
        warn_time = users[f'{user.id}']['time']
        warn_id = users[f'{user.id}']['warn_id']


        await ctx.send(f"Warning count: {warns} Given by:{moderator} For:{warn_reason} At:{warn_time} IDs:{warn_id}")

    



    except:
        await ctx.send(f"{user.mention} doesn't have any warnings (yet).")

bot.run("ODg5MDI3MTI1Mjc1OTIyNDYy.YUbRBw.96QzGKIyYjyIwKNuXG-w2-i73rY")
