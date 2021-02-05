import discord
from discord.ext import commands
import time, datetime, humanize
start = time.time()

class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief='Shows how long the bot has been on (in human time)')
    async def uptime(self, ctx):
        embed = discord.Embed(title='Uptime', color = discord.Color.random(), description=self.bot.uptime_delta_humanized())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Uptime(bot))
