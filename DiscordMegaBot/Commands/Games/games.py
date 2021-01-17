import discord
from discord.ext import commands
import random
import asyncio
from random_words import RandomWords
import copy
import upsidedown

eightBall_msgs = ["It is certain","Without a doubt", "\
You may rely on it","\
Yes definitely","\
It is decidedly so","\
As I see it, yes","\
Most likely","\
Yes","\
Outlook good","\
Signs point to yes","\
Reply hazy try again","\
Better not tell you now","\
Ask again later","\
Cannot predict now","\
Concentrate and ask again","\
Don’t count on it","\
Outlook not so good","\
My sources say no","\
Very doubtful","\
My reply is no"]
    
rocpapsci = ['rock', 'paper', 'scissors']

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def rps(self, ctx, ropasc=None):
        if ropasc is None:
            await ctx.send('Missing Required Arguments!')
            return
        if not ropasc in rocpapsci:
            await ctx.send('Invalid Argument! Valid Arguments: paper, scissors, rock')
            return
        a = random.choice(rocpapsci)
        await ctx.send('rock..')
        await asyncio.sleep(0.3)
        await ctx.send('paper..')
        await asyncio.sleep(0.3)
        await ctx.send('scissors..')
        await asyncio.sleep(0.3)
        await ctx.send('shoot!')
        await asyncio.sleep(0.3)
        await ctx.send('I chose {}.. you chose {}.'.format(a, ropasc))
    
    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        answer = random.choice(eightBall_msgs)
        await ctx.send(f'Question: {question}\nAnswer: {str(answer)}')
    
    @commands.command()
    async def roll(self, ctx, dice:int=3):
        if dice > 20:
            await ctx.send(f'Sorry, but i don\'t have {dice} dice')
            return
        if dice < 1:
            await ctx.send(f'Sorry, but i don\'t have {dice} die')
            return
        a = []
        for x in range(dice):
            a.append(str(random.randint(0, 10)))
        await ctx.send('You Rolled: \n`' + (', '.join(a)) + '`')
    
    @commands.command()
    async def choice(self, ctx, *args):
        choice = random.choice(args)
        await ctx.send('I chose '+choice)
    
    @commands.command()
    async def pseudotext(self, ctx):
        predicate = random.choice(['pseudo text', 'dog', 'cat', 'your mom', 'mr. beaver', 'people'])
        adjective = random.choice(['cool', 'bad', 'awesome', 'big', 'stupid', 'also stupid'])
        await ctx.send(predicate + ' is ' + adjective)
    
    @commands.command()
    async def spinner(self, ctx):
        a = random.randint(1, 100)
        await ctx.send('You started spinning a fidget spinner, lets see how long it spins!')
        await asyncio.sleep(a)
        await ctx.send(f'It spun for {a} seconds!')
    
    @commands.command()
    async def scramble(self, ctx, *, text:str):
        a = list(text)
        random.shuffle(a)
        await ctx.send(''.join(a))
    
    @commands.command()
    async def reverse(self, ctx, *, text:str):
        a = list(text)
        a.reverse()
        await ctx.send(''.join(a))
    
    @commands.command(name='upsidedown')
    async def _upsidedown(self, ctx, *, text:str):
        text = upsidedown.transform(text)
        await ctx.send(text)
    
    @commands.command()
    async def eat(self, ctx, member:discord.Member=None, *, reason:str=None):
        if member == None or member == ctx.author:
            await ctx.send(f'{ctx.author.mention} ate themselves...')
            return
        if reason == None:
            await ctx.send(f'{ctx.author.mention} ate {member.mention}')
        elif reason != None:
            await ctx.send(f'{ctx.author.mention} ate {member.mention} for {reason}')
    
    @commands.command()
    async def kill(self, ctx, member:discord.Member=None, *, reason:str=None):
        if member == None or member == ctx.author:
            await ctx.send(f'{ctx.author.mention} commited suicide')
            return
        if reason == None:
            await ctx.send(f'{ctx.author.mention} killed {member.mention}')
        elif reason != None:
            await ctx.send(f'{ctx.author.mention} killed {member.mention} for {reason}')

def setup(bot):
    bot.add_cog(Games(bot))
