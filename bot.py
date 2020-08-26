import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = int(os.getenv('CHANNEL_ID'))

bot = commands.Bot(command_prefix='!')
bot.load_extension("cogs.mtgcog")
bot.load_extension("cogs.factoriocog")
bot.load_extension("cogs.economycog")

@bot.event
async def on_ready():
  channel = bot.get_channel(CHANNEL)
  print(channel.name)
  print(f'{bot.user} has connected to Discord!')
  # await channel.send('Connected successfully!')

bot.run(TOKEN)