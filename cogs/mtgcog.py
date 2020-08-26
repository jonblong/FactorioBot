import requests
from discord.ext import commands

def terms_to_url(terms):
    search = "https://api.scryfall.com/cards/named?fuzzy="
    count = 0

    for term in terms:
      if count > 0: search += '+'
      search += term
      count += 1

    return search

class MtgCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='mtg', help='Find a MTG card')
  async def mtg(self, ctx, *name):
    response = requests.get(terms_to_url(name))

    if response.status_code == 200:
      image = response.json()['image_uris']['png']
      await ctx.send(image)
    else:
      await ctx.send("Card not found!")

def setup(bot):
    bot.add_cog(MtgCog(bot))