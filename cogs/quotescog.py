import os
import psycopg2
import random
from discord.ext import commands
from dotenv import load_dotenv

HOSTNAME = os.getenv('HOSTNAME')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

class QuotesCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='get-quote', help='Fetch a random quote')
  async def get_quote(self, ctx):
    conn = psycopg2.connect(
      host=HOSTNAME,
      user="postgres",
      password=PASSWORD,
      dbname=DATABASE
    )

    cur = conn.cursor()

    cur.execute("SELECT * FROM quotes;")
    quotes = cur.fetchall()
    index = random.randint(0, len(quotes)) - 1
    quote = quotes[index][1]
    user = self.bot.get_user(int(quotes[index][2])).name
    await ctx.send(quote + '    -' + user)
    cur.close()
    conn.close()

  @commands.command(name='quote', help='Save a quote!')
  async def quote(self, ctx, user, quote):
    id = str(ctx.message.mentions[0].id)
    conn = psycopg2.connect(
      host=HOSTNAME,
      user="postgres",
      password=PASSWORD,
      dbname=DATABASE
    )

    cur = conn.cursor()
    cur.execute("INSERT INTO quotes (quote, user_id) VALUES (%s, %s);", (quote, id))
    conn.commit()
    cur.close()
    conn.close()

def setup(bot):
  bot.add_cog(QuotesCog(bot))