import discord
from discord.ext import commands
import time, datetime, humanize, random
start = time.time()

class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def uptime(self, ctx):
        #end = time.time()
        #difference = end - start
        #self.bot.uptime_seconds = difference
        #delta = datetime.timedelta(seconds = difference)
        #self.bot.uptime_delta = delta
        #humandelta = humanize.naturaldelta(delta)
        #self.bot.humanized_uptime_delta = humandelta
        embed = discord.Embed(title='Uptime', color = random.randint(100000, 999999), description=self.bot.uptime_delta_humanized())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Uptime(bot))
    
