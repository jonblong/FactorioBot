# bot.py
import os
import time
import datetime
import discord
from datetime import timezone
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
  start_time = time.time()
  print(CHANNEL_ID)
  channel = client.get_channel(747152188631154748)
  print(channel.name)
  print(f'{client.user} has connected to Discord!')
  while True:
    for member in client.guilds[0].members:
      if member.activity and member.activity.name == "Factorio":
        time_played = (datetime.datetime.now(tz=timezone.utc) - member.activity.created_at.replace(tzinfo = timezone.utc))
        hours = time_played.seconds // 3600
        minutes = (time_played.seconds // 60) % 60

        await channel.send(f'{member.nick} has been playing Factorio for {hours} hours and {minutes} minutes. His friends and family are beginning to worry.')
        if hours >= 4:
          await channel.send('https://www.youtube.com/watch?v=EdstMCqTJw8')

    time.sleep(3600.0 - ((time.time() - start_time) % 3600.0))

client.run(TOKEN)
