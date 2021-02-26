import discord
from discord.ext import commands

class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def ticket(self, ctx):
        pass
    
    @ticket.command()
    async def create(self, ctx):
        await ctx.send('Check your dm\'s....')
        msg = await ctx.author.send('What is your ticket?')
        def check(message):
            return message.author == ctx.author and message.channel == msg.channel
        content = await self.bot.wait_for('message', check=check)
        await ctx.author.send('Ok, i\'ve sent your ticket to every admin')
        for member in ctx.guild.members:
            for permission_set in member.guild_permissions:
                if permission_set[0].lower() == 'administrator' and permission_set[1] is True:
                    await member.send(f'{ctx.author} just made a ticket: {content}\nPlease respond to it by replying to this message with your response')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        pass

def setup(bot):
    bot.add_cog(Modmail(bot))
