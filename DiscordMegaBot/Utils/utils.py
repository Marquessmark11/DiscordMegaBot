import discord
from discord.ext import commands, ipc
from properties import dagpi_token, google_key, ipc_key
from asyncdagpi import Client
import mystbin
import time
import json
import asyncio
import os
import humanize
import datetime as dt
import async_cse as cse
from aiohttp import ClientSession
from eight_ball import ball
from selenium import webdriver

class Utils:
    def __init__(self):
        pass
    def strl(self, a:list):
        return "".join(a)
    def addChar(self, char:str, adder:list, referencer:list):
        for x in range(len(referencer)):
            if referencer[x] == char:
                adder[x] = (char + adder[x])
        return adder
    def strd(self, a:list):
        return "".join((str(g)+'\n') for g in a)
    def bot_mentioned_in(self, message:discord.Message):
        return message.content == f'<@{message.guild.me.id}>'
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
    
    async def moving_bar(self, *, length:int=20):
        states = ['`[' + ' '*(length+1) + ']`']
        for i in range(1, length+1):
            states.append(f'`{"[" + "#"*i + " "*(length-i) + "]"}`')
        return states
    
    async def sembed(self, ctx, *, title=None, description=None, color=discord.Embed.Empty, author_url=None, author_name=None, footer_text=None, fields=None, image_url=None, thumbnail_url=None):
        embed=discord.Embed(title=title, description=description, color=color)
        if author_url and author_name:
            embed.set_author(icon_url=author_url, name=author_name)
        if footer_text:
            embed.set_footer(text=footer_text)
        if fields:
            for field_name, field_value in fields.items():
                embed.add_field(name=field_name, value=field_value)
        if image_url:
            embed.set_image(url=image_url)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        await ctx.send(embed=embed)
    
    async def screenshot_web(self, url:str):
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(r"C:\Users\Meisc\Downloads\chromedriver_win32\chromedriver.exe", options=options)
        driver.get(url)
        await asyncio.sleep(1)
        
        driver.get_screenshot_as_file("screenshot.png")
        driver.quit()
        return discord.File("screenshot.png")
    
    async def compute_code(self, code:str):
        output = []
        if code.__class__.__name__ != 'list':
            code = code.split('\n')
        var_dict = {}
        for x in range(len(code)):
            if code[x].startswith('var'):
                format = code[x][4:]
                name, content = format.split(':')
                var_dict[name] = content
            if code[x].startswith('echo'):
                if code[x][5:].startswith('%'):
                  try:
                      output.append(var_dict[code[x][5:].split('%')[1]])
                  except KeyError:
                      output.append(f'Var "{code[x][5:].split("%")[1]}" does not exist')
                else:
                  output.append(code[x].removeprefix('echo '))
            if code[x].startswith('newline'):
                output.append('\n')
        return '\n'.join(output)

class DMBText(commands.Context):
    @property
    def is_subclassed(self):
        return type(self) != commands.Context
    
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
        if self.message.id in self.bot._edit_cache:
            msg = self.bot._edit_cache[self.message.id]
            await msg.edit(content=content, **kwargs)
            return
        else:
            msg = await super().send(content, **kwargs)
            self.bot._edit_cache[self.message.id] = msg
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
        self.remove_command('help')
        self._commands = 0
        self.currency_cache = {}
        self.session = ClientSession(loop=self.loop)
        self.dag = Client(dagpi_token, loop=self.loop)
        self.mystbin = mystbin.Client()
        self._start = time.time()
        self._prefixes = json.load(open('./prefixes.json', 'r'))
        self._banned = json.load(open('./bans.json', 'r'))
        self._edit_cache = {}
        self.cse = cse.Search(google_key)
        self.ipc = ipc.Server(self, 'localhost', 8080, secret_key=ipc_key)
        self.ball = ball()
        self.load_extension('jishaku')
        os.environ["JISHAKU_NO_UNDERSCORE"] = "true"
        os.environ["JISHAKU_NO_DM_TRACEBACK"] = "true" 
        os.environ["JISHAKU_HIDE"] = "true"
    
    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        print("Ipc is ready.")
    
    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""
        print(endpoint, "raised", error)
    
    @property
    def commands_re(self):
        return self._commands
    
    @property
    def uptime(self):
        return humanize.naturaldelta(dt.timedelta(seconds=time.time() - self._start))
    
    @property
    def prefixes(self):
        return json.load(open('./prefixes.json', 'r'))
    
    @property
    def bans(self):
        return json.load(open('./bans.json', 'r'))
    
    async def get_context(self, message, cls=DMBText):
        return await super(self.__class__, self).get_context(message, cls=cls)

utils = Utils()
