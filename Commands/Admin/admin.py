import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def change_status_bot(self, ctx, *, activity='placeholder'):
        activity = discord.Game(f'{activity}')
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        await ctx.send(f'Changed activity to {activity}.')
    
    @commands.command()
    @commands.is_owner()
    async def stop_bot(self, ctx):
        emoji = '\N{THUMBS UP SIGN}'
        message = ctx.message
        await message.add_reaction(emoji)
        await ctx.bot.logout()

def setup(bot):
    bot.add_cog(Admin(bot))
