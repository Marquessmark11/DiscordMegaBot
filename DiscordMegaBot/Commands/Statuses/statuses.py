import discord
from discord.ext import commands, tasks
from itertools import cycle

status = cycle(["with your mom", "with you", "with the chat", "the development of this bot"])

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @tasks.loop(seconds=19)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(next(status)))

def setup(bot):
    bot.add_cog(Status(bot))
