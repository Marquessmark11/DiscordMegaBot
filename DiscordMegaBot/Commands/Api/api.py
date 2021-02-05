import discord
from discord.ext import commands
import json
from Utils.utils import utils
import unicodedata
from bottom import to_bottom, from_bottom
import base64

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

class API(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def msgraw(self, ctx, id):
        await ctx.send(utils.codeblock(json.dumps(await self.bot.http.get_message(ctx.channel.id, id), indent=4), language='json'))
    
    @commands.command()
    async def userraw(self, ctx, id):
        await ctx.send(utils.codeblock(json.dumps(await self.bot.http.get_user(id), indent=4), language='json'))
    
    @commands.command()
    async def guildraw(self, ctx, id):
        try:
            await ctx.send(utils.codeblock(json.dumps(await self.bot.http.get_guild(id), indent=4), language='json'))
        except discord.HTTPException:
            cmd = self.bot.get_command('mystbin')
            raw = await self.bot.http.get_guild(id)
            context = await self.bot.get_context(await self.bot.get_guild(801287324109373481).get_channel(801920760565727263).fetch_message(801920951600152587))
            msg = await cmd(context, syntax='json', data=str(json.dumps(raw, indent=4)))
            await ctx.send(f'Output too long, so i uploaded it to mystbin: {msg.content}')
    
    @commands.command()
    async def charinfo(self, ctx, char:str):
        values = []
        for value in char:
            values.append(to_string(value))
        await ctx.send('\n'.join(values))
    
    @commands.command()
    async def toEmoji(self, ctx, *, content:str):
        await ctx.send(content.replace('0', '🟦').replace('1', '🟩'))
    
    @commands.command()
    async def grid(self, ctx, *, content:str):
        await ctx.send(toEmoji(content))
    
    @commands.group()
    async def bottom(self, ctx):
        pass
    
    @bottom.command()
    async def encode(self, ctx, *, content:str):
        await ctx.send('```\n' + to_bottom(content) + '\n```')
    
    @bottom.command()
    async def decode(self, ctx, *, content:str):
        await ctx.send('```\n' + from_bottom(content) + '\n```')
    
    @commands.command(aliases=['pt'])
    async def parsetoken(self, ctx, token:str):
        id = base64.b64decode(token.split('.')[0])
        await ctx.send(f'The id belonging to this token is {id.decode()}')

def setup(bot):
  bot.add_cog(API(bot))
