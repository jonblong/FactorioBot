import os
import time
import datetime
import asyncio
import discord
import scrython
from datetime import timezone
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

async def check_factorio_stats():
  await client.wait_until_ready()
  channel = client.get_channel(747152188631154748)

  while not client.is_closed():
    if get_play_time() != 'NONE':
      await channel.send(get_play_time())
    await asyncio.sleep(3600)

def get_play_time():
  playing = []
  for member in client.guilds[0].members:
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

@client.event
async def on_ready():
  channel = client.get_channel(747152188631154748)
  print(channel.name)
  print(f'{client.user} has connected to Discord!')
  await channel.send('Connected successfully!')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$cracktorio'):
    msg = get_play_time()
    if msg != 'NONE':
      await message.channel.send(msg)
    else:
      await message.channel.send("Everyone is clean.")

client.loop.create_task(check_factorio_stats())
client.run(TOKEN)