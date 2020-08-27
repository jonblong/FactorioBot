import os
import psycopg2
from discord.ext import commands
from dotenv import load_dotenv

HOSTNAME = os.getenv('HOSTNAME')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

class EconomyCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='give', help='Gives a unit of currency to a user.')
  async def give(self, ctx, name, amount: int):
    id = str(ctx.message.mentions[0].id)
    conn = psycopg2.connect(
      host=HOSTNAME,
      user="postgres",
      password=PASSWORD,
      dbname=DATABASE
    )

    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM currency WHERE user_id LIKE %s);", (id,))
    if not cur.fetchone():
      print(cur.execute("INSERT INTO currency (user_id, points) VALUES (%s, %s);", (id, amount)))
      print(cur.execute("SELECT * FROM currency;"))
    else:
      cur.execute("SELECT points FROM currency WHERE user_id LIKE %s;", (id,))
      current_num = cur.fetchone()[0]
      cur.execute("UPDATE currency SET points = %s WHERE user_id LIKE %s;", (current_num + amount, id))
    conn.commit()
    cur.close()
    conn.close()

  @commands.command(name='get', help='Gets currency')
  async def get(self, ctx, name):
    id = str(ctx.message.mentions[0].id)
    conn = psycopg2.connect(
      host=HOSTNAME,
      user="postgres",
      password=PASSWORD,
      dbname=DATABASE
    )

    cur = conn.cursor()

    cur.execute("SELECT EXISTS(SELECT 1 FROM currency WHERE user_id LIKE %s);", (id,))
    no = cur.fetchone()[0]
    print(no)
    if not no:
      cur.execute("INSERT INTO currency (user_id, points) VALUES (%s, %s);", (id, 0))
      conn.commit()

    cur.execute("SELECT points FROM currency WHERE user_id LIKE %s;", (id,))
    points = cur.fetchone()[0]
    print(points)
    await ctx.send(points)
    cur.close()
    conn.close()

  @commands.command(name='leaderboard', help='Shows')
  async def leaderboard(self, ctx, name):
    leaderboard = ""
    conn = psycopg2.connect(
      host=HOSTNAME,
      user="postgres",
      password=PASSWORD,
      dbname=DATABASE
    )

    cur = conn.cursor()
    cur.execute("SELECT user_id, points FROM currency;")
    results = cur.fetchall()
    for user in results:
      name = self.bot.get_user(int(user[0])).name
      points = user[1]
      leaderboard += f'{name}: points\n'

    await ctx.send(leaderboard)

    cur.close()
    conn.close()

def setup(bot):
  bot.add_cog(EconomyCog(bot))
