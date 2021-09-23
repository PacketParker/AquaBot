import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import json

log_channel_id = 889293946801516554

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
                


with open('reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []

@bot.command(pass_context = True)
@commands.has_permissions(manage_roles=True, ban_members=True)
async def warn(ctx,user:discord.User,*reason:str):
  if not reason:
    await ctx.send("Please provide a reason")
    return
  reason = ' '.join(reason)
  for current_user in report['users']:
    if current_user['name'] == user.name:
      current_user['reasons'].append(reason)
      break
  else:
    report['users'].append({
      'name':user.name,
      'reasons': [reason,]
    })
  with open('reports.json','w+') as f:
    json.dump(report,f)

@bot.command(pass_context = True)
async def warnings(ctx,user:discord.User):
  for current_user in report['users']:
    if user.name == current_user['name']:
      await ctx.send(f"{user.name} has been reported {len(current_user['reasons'])} times : {','.join(current_user['reasons'])}")
      break
  else:
    await ctx.send(f"{user.name} has never been reported") 


bot.run("ODg5MDI3MTI1Mjc1OTIyNDYy.YUbRBw.96QzGKIyYjyIwKNuXG-w2-i73rY")
