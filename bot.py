import os
import time
import datetime
import asyncio
import discord
import requests
from datetime import timezone
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = int(os.getenv('CHANNEL_ID'))

bot = commands.Bot(command_prefix='!')

async def check_factorio_stats():
  await bot.wait_until_ready()
  channel = bot.get_channel(CHANNEL)

  while not bot.is_closed():
    if get_play_time() != 'NONE':
      await channel.send(get_play_time())
    await asyncio.sleep(3600)

def get_play_time():
  playing = []
  for member in bot.guilds[0].members:
    if member.activity and member.activity.name == "Factorio":
      time_played = (datetime.datetime.now(tz=timezone.utc) - member.activity.created_at.replace(tzinfo = timezone.utc))
      hours = time_played.seconds // 3600
      minutes = (time_played.seconds // 60) % 60

      playing.append(f'{member.nick}: {hours} hours and {minutes} minutes')
  str = 'Current fiends:'
  for ch in playing:
    str = str + '\n' + '     ' + ch
  
  if len(playing) > 0:
    return str
  else:
    return 'NONE'

@bot.event
async def on_ready():
  channel = bot.get_channel(CHANNEL)
  print(channel.name)
  print(f'{bot.user} has connected to Discord!')
  await channel.send('Connected successfully!')

@bot.command(name='cracktorio', help='See which of your friends are scratching the itch.')
async def cracktorio(ctx):
  await ctx.send(get_play_time())

@bot.command(name='mtg', help='Find a MTG card')
async def mtg(ctx, *name):
  terms = ""
  for term in name:
    terms = terms + term + '+'

  response = requests.get('https://api.scryfall.com/cards/named?fuzzy=%s'%terms)
  if response.status_code == 200:
    await ctx.send(response.json()['image_uris']['png'])
  else: 
    await ctx.send("Card not found!")

bot.loop.create_task(check_factorio_stats())
bot.run(TOKEN)