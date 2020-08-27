import os
import datetime
from discord.ext import commands
from datetime import timezone
from dotenv import load_dotenv

load_dotenv()
GUILD = int(os.getenv('GUILD_ID'))

def get_time_played(created_at):
  time_played = (datetime.datetime.now(tz=timezone.utc) - created_at)
  hours = time_played.seconds // 3600
  hrsstr = str(hours)
  if len(hrsstr) == 1: hrsstr = '0' + hrsstr

  minutes = (time_played.seconds // 60) % 60
  minstr = str(minutes)
  if len(minstr) == 1: minstr = '0' + minstr

  seconds = time_played.seconds % (24 * 3600)

  return f'{hours}:{minstr}'

class FactorioCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='playing', help='See how long your friends have been playing Factorio.')
  async def playing(self, ctx):
    guild = self.bot.get_guild(GUILD)
    crack = ""
    for member in guild.members:
      if member.activity:
        crack += f'{member.name} - {member.activity.name} {" " * (30 - len(member.name) - len(member.activity.name))} {get_time_played(member.activity.created_at.replace(tzinfo = timezone.utc))}\n'

    if len(crack) > 0:
      crack = "```" + crack + "```"
      await ctx.send(crack)
    else:
      await ctx.send("Everyone is clean!")

def setup(bot):
    bot.add_cog(FactorioCog(bot))