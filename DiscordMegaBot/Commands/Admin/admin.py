import discord
from discord.ext import commands
from discord.ext import ui
import sqlite3
import os
import subprocess as sp
import json
import random

currency_db_path = './Commands/Currency/currency.json'
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    @commands.is_owner()
    async def dev(self, ctx):
        pass
    
    @dev.command()
    async def status(self, ctx, *, activity):
        activity = discord.Game(activity)
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        await ctx.send(f'Changed activity to {activity}.')
    
    @dev.command()
    async def stop(self, ctx):
        emoji = '\N{THUMBS UP SIGN}'
        message = ctx.message
        await message.add_reaction(emoji)
        await ctx.bot.logout()
    
    @dev.command()
    async def give(self, ctx, member:discord.Member, money:int):
        with open(currency_db_path, 'r') as f:
            currency = json.load(f)
        
        currency[str(member.id)] += money
        self.bot.currency_cache = currency
        
        with open(currency_db_path, 'w') as f:
            json.dump(currency, f, indent=4)
        await ctx.send('Given {} {} dollars(s)'.format(member.name, money))
    
    @dev.command()
    async def take(self, ctx, member:discord.Member, money:int):
        with open(currency_db_path, 'r') as f:
            currency = json.load(f)
        
        currency[str(member.id)] -= money
        self.bot.currency_cache = currency
        
        with open(currency_db_path, 'w') as f:
            json.dump(currency, f, indent=4)
        await ctx.send('Taken {} dollar(s) from {}'.format(money, member.name))
    
    @dev.command()
    async def set(self, ctx, member:discord.Member, money:int):
        with open(currency_db_path, 'r') as f:
            currency = json.load(f)
        
        currency[str(member.id)] = money
        self.bot.currency_cache = currency
        
        with open(currency_db_path, 'w') as f:
            json.dump(currency, f, indent=4)
        await ctx.send('Set {}\'s amount of dollar(s) to be {}'.format(member.name, money))
    
    @dev.command()
    async def remove(self, ctx, member:discord.Member):
        with open(currency_db_path, 'r') as f:
            currency = json.load(f)
        
        del currency[str(member.id)]
        self.bot.currency_cache = currency
        
        with open(currency_db_path, 'w') as f:
            json.dump(currency, f, indent=4)
        await ctx.send('Removed {} from database'.format(member.name))
    
    @dev.command(name='help')
    async def devHelp(self, ctx):
        await ctx.author.send(embed = discord.Embed(title="Developer Commands", color=random.randint(100000, 999999), description='\n'.join([c.name for c in self.bot.get_cog('Admin').__cog_commands__])))
    
    @dev.command()
    async def eval_python(self, ctx, *, code:str):
        f = open('Evaluation/code.py', 'w')
        code = code.replace('```py\n', '')
        code = code.replace('```python\n', '')
        code = code.replace('\n```', '')
        code = code.replace('```', '')
        f.write(code)
        f.close()
        code = code.split('\n')
        for line_index in range(len(code)):
            code[line_index] = '>>> ' + code[line_index]
        await ctx.tick(not sp.getoutput('python Evaluation/code.py').startswith('Traceback (most recent call last):'))
        if sp.getoutput('python Evaluation/code.py') == '':
            embed = discord.Embed(title="An Exception Occurred", description = '```py\n' + 'Traceback (most recent call last):\n    File "Evaluation/code.py", line {} in <module>\n        {}\nNoResponse: No response returned, you most likely forget to print your result'.format(len(code), code[len(code)-1].strip('>>> ')) + '\n```', color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        elif sp.getoutput('python Evaluation/code.py').startswith('Traceback (most recent call last):'):
            embed = discord.Embed(title="An Exception Occurred", description = '```py\n' + sp.getoutput('python Evaluation/code.py') + '\n```', color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title="Evaluation", color=discord.Color.green(), description='```py\n' + ('\n'.join(code)) + '\n' + sp.getoutput('python Evaluation/code.py').replace(self.bot.http.token, '{token redacted}') + '\n```')
        await ctx.send(embed=embed)
    
    @dev.command()
    async def remmessages(self, ctx):
        async for message in ctx.channel.history():
            try:
                await message.delete()
            except discord.Forbidden:
                continue
        await ctx.send('Removed all my messages from 2 weeks ago onwards')
    
    @dev.command()
    async def testingServer(self, ctx):
        await ctx.send('https://discord.gg/Zbcxvw9g')
    
    @dev.command()
    async def support(self, ctx):
        await ctx.send('https://discord.gg/ysq4ayTc83')
    
    @dev.command()
    async def output(self, ctx, *, cmd:str):
        await ctx.send(f'Dev Note: Temporary output, will add embed soon!\n{sp.getoutput(cmd)}')
    
    @dev.command()
    async def remmessage(self, ctx, id:int):
        try:
            await (await ctx.fetch_message(id)).delete()
            await ctx.send('Successfully deleted ' + str(id))
        except discord.Forbidden:
            await ctx.send('I require manage messages permission to delete this message')
    
    @dev.command()
    async def clear(self, ctx, amount:int):
        def is_me(m):
            return m.author.id == self.bot.user.id
        
        purges = await ctx.channel.purge(limit=amount, check=is_me, bulk=False)
        await ctx.send(f"cleared {len(purges)} messages")
    
    @dev.command()
    async def blacklist(self, ctx, member:discord.Member):
        with open('./bans.json', 'r') as f:
            bans = json.load(f)
        
        bans[str(member.id)] = 'Yes'
        
        with open('./bans.json', 'w') as f:
            json.dump(bans, f, indent=4)
        
        await ctx.send('Successfully blacklisted {} from this bot'.format(member.display_name))
    
    @dev.command()
    async def whitelist(self, ctx, member:discord.Member):
        with open('./bans.json', 'r') as f:
            bans = json.load(f)
        
        del bans[str(member.id)]
        
        with open('./bans.json', 'w') as f:
            json.dump(bans, f, indent=4)
        
        await ctx.send('Successfully whitelisted {} from this bot'.format(member.display_name))

def setup(bot):
    bot.add_cog(Admin(bot))