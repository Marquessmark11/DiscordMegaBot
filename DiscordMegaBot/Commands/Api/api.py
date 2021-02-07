import discord
from discord.ext import commands
import json
from Utils.utils import utils
import unicodedata
from bottom import to_bottom, from_bottom
import base64
import random
import humanize
import datetime
import time
import asyncio

def to_string(c):
    digit = f'{ord(c):x}'
    name = unicodedata.name(c, 'Can not find')
    return f'`\\U{digit:>08}`= {name}'

squares = ['⬛', '⬜', '🟫', '🟥', '🟦', '🟩', '🟨', '🟧']
rule = {str(i): squares[i] for i in range(8)}
def toEmoji(e):
  for k in rule.keys():
    e = e.replace(k, rule[k])
  return e

def fromEmoji(e):
  for k in rule.keys():
    e = e.replace(rule[k], k)
  return e

class API(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief='Shows the raw data of a message')
    async def msgraw(self, ctx, id):
        await ctx.send(utils.codeblock(json.dumps(await self.bot.http.get_message(ctx.channel.id, id), indent=4), language='json'))
    
    @commands.command(brief='Shows the raw data of a user')
    async def userraw(self, ctx, id):
        await ctx.send(utils.codeblock(json.dumps(await self.bot.http.get_user(id), indent=4), language='json'))
    
    @commands.command(brief='Shows the raw data of a server')
    async def guildraw(self, ctx, id):
        try:
            await ctx.send(utils.codeblock(json.dumps(await self.bot.http.get_guild(id), indent=4), language='json'))
        except discord.HTTPException:
            cmd = self.bot.get_command('mystbin')
            raw = await self.bot.http.get_guild(id)
            context = await self.bot.get_context(await self.bot.get_guild(801287324109373481).get_channel(801920760565727263).fetch_message(801920951600152587))
            msg = await cmd(context, syntax='json', data=str(json.dumps(raw, indent=4)))
            await ctx.send('Output too long, so i uploaded it to mystbin: {}'.format(msg.content))
    
    @commands.command(brief='Shows unicode info on a character')
    async def charinfo(self, ctx, char:str):
        values = []
        for value in char:
            values.append(to_string(value))
        await ctx.send('\n'.join(values))
    
    @commands.command(brief='Maps numbers to emojis')
    async def grid(self, ctx, *, content:commands.clean_content):
        if content[0] == ':':
            await ctx.send(fromEmoji(content))
            return
        await ctx.send(toEmoji(content))
    
    @commands.group(brief='Encodes and decodes bottom')
    async def bottom(self, ctx):
        pass
    
    @bottom.command(brief='Encodes into bottom')
    async def encode(self, ctx, *, content:str):
        await ctx.send('```\n' + to_bottom(content) + '\n```')
    
    @bottom.command(brief='Decodes out of bottom')
    async def decode(self, ctx, *, content:str):
        await ctx.send('```\n' + from_bottom(content) + '\n```')
    
    @commands.command(aliases=['pt'], brief='Shows the id belonging to the token')
    async def parsetoken(self, ctx, token:str):
        id = base64.b64decode(token.split('.')[0])
        await ctx.send(f'The id belonging to this token is {id.decode()}')
    
    @commands.command(aliases=['rm'], brief='Shows a random message from the current channel')
    async def randommessage(self, ctx, limit:int=100):
        start = time.perf_counter()
        messages = await ctx.channel.history(limit=limit).flatten()
        message = random.choice(messages)
        end = time.perf_counter()
        e = discord.Embed(description=message.content, color=random.randint(100000, 999999))
        e.set_footer(text='ID: '+str(message.id) + ', Took ' + str(round((end - start)*1000, 6)) + 'ms to find message')
        e.add_field(name='jump url', value=f'[jump!]({message.jump_url})')
        e.set_author(icon_url=message.author.avatar_url, name=message.author.name)
        await ctx.send(embed=e)
    
    @commands.command(aliases=['rma'], brief='Shows a random message sent by you in the current channel')
    async def randmessageauth(self, ctx, limit:int=100):
        start = time.perf_counter()
        messages = [message for message in (await ctx.channel.history(limit=limit).flatten()) if message.author.name == ctx.author.name]
        message = random.choice(messages)
        end = time.perf_counter()
        e = discord.Embed(description=message.content, color=random.randint(100000, 999999))
        e.set_footer(text='ID: '+str(message.id) + ', Took ' + str(round((end - start)*1000, 6)) + 'ms to find message')
        e.add_field(name='jump url', value=f'[jump!]({message.jump_url})')
        e.set_author(icon_url=message.author.avatar_url, name=message.author.name)
        await ctx.send(embed=e)

def setup(bot):
  bot.add_cog(API(bot))
