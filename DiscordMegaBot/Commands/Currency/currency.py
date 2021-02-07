import discord
from discord.ext import commands
import json
import random
import os

currency_db_path = './Commands/Currency/currency.json'
class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def isInDatabase(self, member:discord.Member):
        with open(currency_db_path, 'r') as f:
            currency = json.load(f)
        
        try:
            entry = currency[str(member.id)]
            return True
        except KeyError:
            return False
    
    @commands.command()
    async def bal(self, ctx):
        with open(currency_db_path, 'r') as f:
            currency = json.load(f)
        
        try:
            embed = discord.Embed(title='Balance', color=random.randint(100000, 999999), description=currency[str(ctx.author.id)])
            await ctx.send(embed=embed)
        except KeyError:
            embed = discord.Embed(title='Balance', color=random.randint(100000, 999999), description='0')
            await ctx.send(embed=embed)
    
    @commands.command()
    async def steal(self, ctx, member:discord.Member):
        if member.id == 376129806313455616 or member == ctx.author:
            await ctx.send('Hmmm, nope, not gonna do that.')
            return
        with open(currency_db_path, 'r') as f:
            currency = json.load(f)
        
        success = random.choice(['no', 'yes'])
        if success == 'no' or self.isInDatabase(member) is False:
            await ctx.send('you were found or they have no money lmao')
            return
        if success == 'yes':
            if self.isInDatabase(member) is True and self.isInDatabase(ctx.author) is True:
                stolen = random.randint(0, currency[str(member.id)])
                currency[str(member.id)] -= stolen
                currency[str(ctx.author.id)] += stolen
                self.bot.currency_cache = currency
                
                with open(currency_db_path, 'w') as f:
                    json.dump(currency, f, indent=4)
                await ctx.send('Stolen {} from {}'.format(stolen, member.name))
            elif self.isInDatabase(member) is True and self.isInDatabase(ctx.author) is False:
                stolen = random.randint(0, currency[str(member.id)])
                currency[str(member.id)] -= stolen
                currency[str(ctx.author.id)] = stolen
                self.bot.currency_cache = currency
                
                with open(currency_db_path, 'w') as f:
                    json.dump(currency, f, indent=4)
                await ctx.send('Stolen {} from {}'.format(stolen, member.name))
    
def setup(bot):
    bot.add_cog(Currency(bot))
