import discord
from discord.ext import commands
import time
import json
import asyncio

class Utils:
    def __init__(self):
        pass
    def strl(self, a:list):
        h = ""
        for g in a:
            h+=g
        return h
    def addChar(self, char:str, adder:list, referencer:list):
        for x in range(len(referencer)):
            if referencer[x] == char:
                adder[x] = (char + adder[x])
        return adder
    def strd(self, a:list):
        h = ""
        for g in a:
            h+=(str(g)+'\n')
        return h
    def bot_mentioned_in(self, message:discord.Message):
        if message.content == f'<@{message.guild.me.id}>':
            return True
        else:
            return False
    def indent(self, code:str):
        code = code.split('\n')
        for line_index in range(len(code)):
          if code[line_index].endswith(':') and not code[line_index+1].startswith(" "):
            code[line_index+1] = '    ' + code[line_index+1]
        return '\n'.join(code)
    def codeblock(self, code:str, *, language:str='python'):
        code = f'```{language}\n{code}\n```'
        return code
    
    def prefix_for(self, bot, guild:discord.Guild):
        return bot.prefixes[str(guild.id)]
    
    async def moving_bar(self, ctx, *, length:int=20):
        states = []
        states.append('`[' + ' '*(length+1) + ']`')
        for i in range(1, length+1):
            await asyncio.sleep(2)
            states.append(f'`{"[" + "#"*i + " "*(length-i) + "]"}`')
        return states
    
    async def sembed(self, ctx, *, title=None, description=None, color=discord.Embed.Empty, author_url=None, author_name=None, footer_text=None, fields=None, image_url=None, thumbnail_url=None):
        embed=discord.Embed(title=title, description=description, color=color)
        if author_url and author_name:
            embed.set_author(icon_url=author_url, name=author_name)
        if footer_text:
            embed.set_footer(text=footer_text)
        if fields:
            for field_name, field_value in fields:
                embed.add_field(name=field_name, value=field_value)
        if image_url:
            embed.set_image(url=image_url)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        await ctx.send(embed=embed)

class DMBText(commands.Context):
    @property
    def is_subclassed(self):
        return not type(self) == commands.Context
    
    async def tick(self, value):
        emoji = '\N{WHITE HEAVY CHECK MARK}' if value else '\N{CROSS MARK}'
        await self.message.add_reaction(emoji)
    
    async def sembed(self, *, title=None, description=None, color=discord.Embed.Empty, author_url=None, author_name=None, footer_text=None, fields=None, image_url=None, thumbnail_url=None):
        embed=discord.Embed(title=title, description=description, color=color)
        if author_url and author_name:
            embed.set_author(icon_url=author_url, name=author_name)
        if footer_text:
            embed.set_footer(text=footer_text)
        if fields:
            for field_name, field_value in fields:
                embed.add_field(name=field_name, value=field_value)
        if image_url:
            embed.set_image(url=image_url)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        await self.send(embed=embed)
    
    async def send(self, content=None, **kwargs):
        if str(self.author.id) in json.load(open('./bans.json', 'r')):
            msg = await super().send('You are blacklisted from this bot.')
            return msg
        if self.message.id in self.bot.edit_cache:
            msg = self.bot.edit_cache[self.message.id]
            if "file" in kwargs:
                kwargs.pop("file")
            await msg.edit(content = content, **kwargs)
            return
        else:
            msg = await super().send(content, **kwargs)
            self.bot.edit_cache[self.message.id] = msg
            return msg
    
    async def owoify(self, text:str):
        return text.replace('l', 'w').replace('L', 'W').replace('r', 'w').replace('R', 'W').replace('o', 'owo').replace('O', 'OWO')

class BoolConverter(commands.Converter):
        async def convert(self, ctx, argument):
            if argument.lower() in ('yes', 'correct', 'agree', '1', 'right', 'true'):
                return True
            elif argument.lower() in ('no', 'incorrect', 'disagree', '0', 'wrong', 'false'):
                return False
            else:
                return False

class DMBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def get_context(self, message, cls=DMBText):
        return await super(self.__class__, self).get_context(message, cls=cls)

utils = Utils()
