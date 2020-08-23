# bot.py
import os
import time
import datetime
import asyncio
import discord
from datetime import timezone
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

async def check_factorio_stats():
  global channel
  await client.wait_until_ready()
  channel = client.get_channel(747152188631154748)

  while not client.is_closed():
    playing = []
    for member in client.guilds[0].members:
      if member.activity and member.activity.name == "Factorio":
        time_played = (datetime.datetime.now(tz=timezone.utc) - member.activity.created_at.replace(tzinfo = timezone.utc))
        hours = time_played.seconds // 3600
        minutes = (time_played.seconds // 60) % 60

        playing.append(f'{member.nick}: {hours} hours and {minutes} minutes')
    str = 'Current fiends:'
    for ch in playing:
      str = str + '\n' + '   ' + ch
    await send(str)
    await asyncio.sleep(60)    

@client.event
async def on_ready():
  global channel
  start_time = time.time()
  channel = client.get_channel(747152188631154748)
  print(channel.name)
  print(f'{client.user} has connected to Discord!')
  await channel.send('Connected successfully!')

client.loop.create_task(check_factorio_stats())
client.run(TOKEN)