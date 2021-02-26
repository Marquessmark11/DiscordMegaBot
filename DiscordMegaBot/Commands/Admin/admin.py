import discord
from discord.ext import commands
from discord.ext import ui
import sqlite3
import os
import subprocess as sp
from jishaku.codeblocks import codeblock_converter
import json
import random
from Commands.Games import games
import inspect
import asyncio
from Utils.utils import utils
import time
from discord.ext import menus

class PaginatorTest(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        self.places = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.place = 0
        return await channel.send(self.places[self.place])
    
    @menus.button('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}')
    async def on_empty_list(self, payload):
        self.place = 0
        await self.message.edit(content=self.places[self.place])
    
    @menus.button('\N{LEFTWARDS BLACK ARROW}')
    async def on_left_arrow(self, payload):
        if self.place == 0:
            return
        self.place -= 1
        await self.message.edit(content=self.places[self.place])
    
    @menus.button('\N{BLACK RIGHTWARDS ARROW}')
    async def on_right_arrow(self, payload):
        if self.place == len(self.places)-1:
            return
        self.place += 1
        await self.message.edit(content=self.places[self.place])
    
    @menus.button('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}')
    async def on_full_list(self, payload):
        self.place = (len(self.places) - 1)
        await self.message.edit(content=self.places[self.place])
    
    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        self.stop()

currency_db_path = './Commands/Currency/currency.json'
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    @commands.is_owner()
    async def dev(self, ctx):
        pass
    
    @dev.command()
    async def eval(self, ctx, *, code:str):
        cog = self.bot.get_cog("Jishaku")
        res = codeblock_converter(code)
        await cog.jsk_python(ctx, argument=res)
    
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
        await ctx.author.send(
            embed=discord.Embed(
                title="Developer Commands",
                color=random.randint(100000, 999999),
                description='\n'.join(
                    c.name for c in self.bot.get_cog('Admin').__cog_commands__
                ),
            )
        )
    
    @dev.command(name='await')
    async def eval_async(self, ctx, *, arg:str):
        try:
            res = eval(arg)
            for line in res:
                if inspect.isawaitable(line):
                    await res
        except:
            pass
    
    @dev.command()
    async def eval_python(self, ctx, *, code:str):
        with open('Evaluation/code.py', 'w') as f:
            code = code.replace('```py\n', '')
            code = code.replace('```python\n', '')
            code = code.replace('\n```', '')
            code = code.replace('```', '')
            f.write(code)
        code = code.split('\n')
        for line_index in range(len(code)):
            code[line_index] = '>>> ' + code[line_index]
        await ctx.tick(not sp.getoutput('py Evaluation/code.py').startswith('Traceback (most recent call last):'))
        if sp.getoutput('py Evaluation/code.py') == '':
            embed = discord.Embed(title="An Exception Occurred", description = '```py\n' + 'Traceback (most recent call last):\n    File "Evaluation/code.py", line {} in <module>\n        {}\nNoResponse: No response returned, you most likely forget to print your result'.format(len(code), code[len(code)-1].strip('>>> ')) + '\n```', color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        elif sp.getoutput('py Evaluation/code.py').startswith('Traceback (most recent call last):'):
            embed = discord.Embed(title="An Exception Occurred", description = '```py\n' + sp.getoutput('py Evaluation/code.py') + '\n```', color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title="Evaluation", color=discord.Color.green(), description='```py\n' + ('\n'.join(code)) + '\n' + sp.getoutput('py Evaluation/code.py').replace(self.bot.http.token, '{token redacted}') + '\n```')
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
        await ctx.send('https://discord.gg/H9Zd9ZYE6T')
    
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
    
    @dev.command(hidden=True)
    async def movingTest(self, ctx):
        menu = games.TestMover(timeout=60.0, clear_reactions_after=True)
        await menu.start(ctx)
    
    @commands.command(hidden=True)
    async def verify(self, ctx):
        if ctx.guild.name == 'The Good Guy Server':
            await ctx.message.delete()
            role_id = 758538458951843843
            role = get(ctx.guild.roles, id=role_id)
            await ctx.author.add_roles(role)
        else:
            await ctx.send('wrong guild')
    
    @dev.command(brief='Screenshots a webpage')
    async def scrn(self, ctx, *, url:str):
        warn = await ctx.channel.send('This may take some time...')
        await ctx.send(file=await utils.screenshot_web(url))
        await warn.delete()
    
    @dev.command(brief='Invoke a command')
    async def invoke(self, ctx, *args, **kwargs):
        args = [arg for arg in args]
        s = time.perf_counter()
        command = self.bot.get_command(args[0])
        args.pop(0)
        await command(ctx, *args, **kwargs)
        t = time.perf_counter()
        e = (t - s) * 1000
        await ctx.channel.send(f'Command {command.name} finished in {round(e, 6)}ms')
    
    @dev.command(hidden=True)
    async def paginatorTest(self, ctx):
        menu = PaginatorTest()
        await menu.start(ctx)

def setup(bot):
    bot.add_cog(Admin(bot))
