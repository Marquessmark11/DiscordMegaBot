import discord
from discord.ext import commands
import random
from datetime import datetime as dt
from asyncio import sleep
import time
import inspect
import os
from discord.ext import flags
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import praw
import sys
import humanize
import mystbin
import aiohttp
import datetime
import urllib
import requests
from bs4 import BeautifulSoup

def scrape_google(query):
    query = query.replace(' ', '+')
    url = f"https://google.com/search?q={query}"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                item = {
                    "link": link
                }
                results.append(item)
        return results

def oauth2link():
    link = discord.utils.oauth_url(client_id=741624868591763487, permissions=discord.Permissions(permissions=8))
    e = discord.Embed(title='Invite DMB To your server', description=f'[:robot: Invite Link]({link})', color=random.randint(100000, 999999))
    return e

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief='A Distraction')
    async def distracted(self, ctx):
        await ctx.send('https://tenor.com/bop5H.gif')
    
    @commands.command(brief='A stickbug meme')
    async def getstickbuggedlol(self, ctx):
        await ctx.send('https://tenor.com/bnQ1p.gif')

    @commands.command(brief='A command that lets you be able to make the bot say anything')
    async def echo(self, ctx, *, content:commands.clean_content):
        await ctx.send(content)
    
    @commands.command(brief='Life.')
    async def life(self, ctx):
        await ctx.send('Life,\nIt has no meaning')
    
    @commands.command(brief='Generates a random number and shows it to you in the form of an embed.')
    async def rcolor(self, ctx):
        r = random.randint(100000, 999999)
        e = discord.Embed(title='Random Color', description=f'0x{r}', color=r)
        await ctx.send(embed=e)
    
    @commands.command(brief='Generates a random symbol/character and shows it to you')
    async def randomCharacter(self, ctx):
        r = random.randint(0, 2000)
        c = chr(r)
        await ctx.send(c)
    
    @commands.command(brief='Shows you the full abcs')
    async def abcFull(self, ctx):
        var = 'a'
        alphabets = []
        # starting from the ASCII value of 'a' and keep increasing the
        # value by i.
        alphabets=[(chr(ord(var)+i)) for i in range(26)]
        await ctx.send(''.join(alphabets))
    
    @commands.command(brief='Shrug.')
    async def shrug(self, ctx):
        await ctx.send('¯\_(ツ)_/¯')
    
    @commands.command(brief='Lenny')
    async def lenny(self, ctx):
        await ctx.send('( ͡° ͜ʖ ͡°)')
    
    @commands.command(brief='Penguin eating fish')
    async def pengoeatfish(self, ctx):
        await ctx.send("https://cdn1.vectorstock.com/i/1000x1000/16/85/penguin-eating-fish-on-ice-vector-6581685.jpg")
    
    @commands.command(brief='Shows help for this bot', invoke_without_command=True)
    async def help(self, ctx, query:str=None):
      if not query:
          co = random.randint(100000, 999999)
          helpc = discord.Embed(color=co, title='Help Categories')
          cogs = [name for name in self.bot.cogs]
          cogs.remove('Admin')
          cogs.remove('Jishaku')
          cogs.remove('Modmail')
          cogs.remove('Status')
          cogs.remove('Uptime')
          categories = '\n'.join(cogs)
          helpc.add_field(name='Categories', value=f"""
```
{categories}
```
Please choose one using {self.bot.command_prefix(self.bot, ctx.message)[2]}help <category name>.
          """)
          await ctx.send(embed=helpc)
      else:
          maybe_cog = self.bot.get_cog(query.lower().capitalize())
          if not maybe_cog and query.lower() == 'api':
              maybe_cog = self.bot.get_cog('API')
          if maybe_cog:
              if maybe_cog.qualified_name == 'Admin' and not ctx.bot.is_owner(ctx.author):
                  await ctx.send('Access Denied')
                  return
              else:
                  co = random.randint(100000, 999999)
                  commands = '\n'.join([command.name for command in maybe_cog.__cog_commands__])
                  e = discord.Embed(color=co, title=f'{maybe_cog.qualified_name}', description=f'{commands}\n\nYou can use {self.bot.command_prefix(self.bot, ctx.message)[2]}help <command name> to get help on a command')
                  await ctx.send(embed=e)
          else:
              command = self.bot.get_command(query)
              if command.cog.qualified_name == 'Admin' and not await ctx.bot.is_owner(ctx.author):
                  await ctx.send('Access Denied.')
                  return
              co = random.randint(100000, 999999)
              embed = discord.Embed(color=co, description=command.brief)
              embed.set_author(name=query)
              await ctx.send(embed=embed)
    
    @commands.command(brief='I was really tired when making this command.')
    async def whattodotoday(self, ctx):
        await ctx.send('To-do list: First item on this list is ahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    
    @commands.command(brief='Allows you to spam something any amount of times.')
    async def spam(self, ctx, a : int=5, *, text : str='placeholder'):
        if text != 'spamabc':
            if a > 1000:
                await ctx.send('Error Code 004: Max spam amount is 1000')
            elif a < 1000:
                for x in range(a):
                    await ctx.send(text)
            elif a == 1000:
                for x in range(a):
                    await ctx.send(text)
    
    @commands.command(brief='Shows an OAuth Invite for the bot')
    async def invite(self, ctx):
        await ctx.send(embed = oauth2link())
    
    @commands.command(brief='Couch.')
    async def couch(self, ctx):
        for x in 'COUCH':
            await ctx.send('COUCH')
    
    @commands.command(brief='Bar')
    async def foo(self, ctx):
        await ctx.send('bar')

    @commands.command(brief='Shows you the bot\'s ping')
    async def ping(self, ctx):
        t = time.perf_counter()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dagpi.xyz/image/wanted", headers={'Authorization': self.bot.dag.token}) as resp:
                pass
        e = time.perf_counter()
        t = time.perf_counter()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://beta.dagpi.xyz/image/wanted", headers={'Authorization': self.bot.dag.token}) as resp:
                pass
        e = time.perf_counter()
        dagpi_latency = (e -t) * 1000
        beta_dagpi_latency = (e -t) * 1000
        latency = round((self.bot.latency * 1000), 6)
        color = random.randint(100000, 999999)
        start = time.perf_counter()
        message = await ctx.send("l")
        end = time.perf_counter()
        duration = (end - start) * 1000
        e = discord.Embed(title=':ping_pong: Pong!', color=color)
        e.add_field(name='Websocket Latency', value="{}ms".format(latency))
        e.add_field(name='Typing Latency', value="{:.2f}ms".format(duration))
        e.add_field(name='Dagpi Latency', value=f'{round(dagpi_latency, 6)}ms')
        e.add_field(name='Beta Dagpi Latency', value=f'{round(beta_dagpi_latency, 6)}ms')
        e.set_thumbnail(url=self.bot.user.avatar_url)
        await message.edit(content="", embed=e)
    
    @commands.command(brief='abcdefghijklmnopqrstuvwxyz')
    async def abc(self, ctx):
        await ctx.send('You know your abc\'s, right?')
    
    @commands.command(brief='Meow')
    async def cat(self, ctx):
        await ctx.send('Meow')
    
    @commands.command(brief='Woof')
    async def dog(self, ctx):
        await ctx.send('Woof')
    
    @commands.command(brief='Chirp')
    async def bird(self, ctx):
        await ctx.send('Chirp')
    
    @commands.command(brief='Hi!')
    async def hello(self, ctx):
        await ctx.send('Hi!')
    
    @commands.command(name='random', brief='Generates a random number between whatever you want.')
    async def _random(self, ctx, minimum : int=0, maximum : int=2147483647):
        randomnumber = random.randint(minimum, maximum)
        await ctx.send(str(randomnumber) + " was chosen")
    
    @commands.command(brief='Licking People.')
    async def lick(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        
        await ctx.send(f'Bot: *licks {member.mention}*\n{member.mention}: Ew stop that')
    
    @commands.command(brief='Technical Info about the bot')
    async def technicalInfo(self, ctx):
        integer = random.randint(100000, 999999)
        e = discord.Embed(color=integer)
        e.set_footer(text='@Copyright 2020 Connor Tippets')
        e.set_thumbnail(url=self.bot.user.avatar_url)
        e.set_author(name='Technical Info', icon_url=self.bot.user.avatar_url)
        e.add_field(name='Discord.py Release Level: ', value=f'{discord.version_info.releaselevel}', inline=False)
        e.add_field(name='Discord.py Release: ', value=f'{str(discord.__version__)}', inline=False)
        e.add_field(name='Pyhon Release: ', value='{}.{}.{}'.format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
        await ctx.send(embed=e)
    
    @commands.command(brief='Kissing People')
    async def kiss(self, ctx, member:discord.Member=None):
        if member is None or member == ctx.author:
            await ctx.send(f'{ctx.author} kissed themselves...')
            return
        await ctx.send(f'{member.name} was kissed by {ctx.author}!')
    
    @commands.command(brief='Info about the bot')
    async def info(self, ctx):
        bot_user = self.bot.user
        bot_info = await self.bot.application_info()
        integer = random.randint(100000, 999999)
        e = discord.Embed(color=integer)
        e.set_footer(text='@Copyright 2020 Connor Tippets')
        e.set_thumbnail(url=bot_user.avatar_url)
        e.set_author(name='Bot Info', icon_url=bot_user.avatar_url)
        e.add_field(name='Name: ', value=f'{bot_info.name}', inline=False)
        e.add_field(name='Id: ', value=f'{bot_info.id}', inline=False)
        e.add_field(name='Bot Creator: ', value=f'{bot_info.owner.mention}', inline=False)
        e.add_field(name='Default Prefix: ', value=':', inline=False)
        e.add_field(name='Servers: ', value=len(self.bot.guilds), inline=False)
        e.add_field(name='Users: ', value=len(self.bot.users), inline=False)
        e.add_field(name='Existed For: ', value=humanize.precisedelta(self.bot.user.created_at), inline=False)
        e.add_field(name='Been Up For: ', value=humanize.precisedelta(datetime.timedelta(seconds=time.time() - self.bot._start)), inline=False)
        e.add_field(name='Credit: ', value='I made most of it myself, but i\'ll give credit where credit is due:', inline=False)
        e.add_field(name='Danny', value='https://github.com/Rapptz/RoboDanny\nhttps://github.com/Rapptz/discord.py', inline=False)
        e.add_field(name='Discord.py Server members', value='https://discord.gg/dpy', inline=True)
        e.add_field(name='And of course, all my friends.', value='None of this would\'ve existed without them.', inline=True)
        await ctx.send(embed=e)
    
    @commands.command(brief='All commands that the bot has')
    async def allCommands(self, ctx):
        await ctx.send(len(self.bot.commands))
    
    @commands.command(brief='Shows you the bots source for a command')
    async def source(self, ctx, *, command: str = None):
        source_url = 'https://github.com/ConnorTippets/DiscordMegaBot'
        branch = 'main'
        if command is None:
            return await ctx.send(source_url)

        if command == 'help':
            src = type(self.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            obj = self.bot.get_command(command.replace('.', ' '))
            if obj is None:
                return await ctx.send('Could not find command.')

            # since we found the command we're looking for, presumably anyway, let's
            # try to access the code itself
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith('discord'):
            # not a built-in command
            location = os.path.relpath(filename).replace('\\', '/')
        else:
            location = module.replace('.', '/') + '.py'
            source_url = 'https://github.com/Rapptz/discord.py'
            branch = 'master'

        final_url = f'<{source_url}/blob/{branch}/DiscordMegaBot/{location}#L{firstlineno + 1}-L{firstlineno + len(lines)}>'
        await ctx.send(final_url)
    
    @commands.command(aliases=['connect'], brief='Makes the bot join a VC')
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice = await channel.connect()
        await ctx.send('Connected!')
    
    @commands.command(aliases=['disconnect'], brief='Makes the bot leave a VC')
    async def leave(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        await voice.disconnect()
        await ctx.send('Disconnected!')
    
    @commands.command(brief='Makes the bot play music in a VC')
    async def play(self, ctx, url):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        
        if voice is None:
            await ctx.send('Not Connected to VC! Connecting....')
            channel = ctx.author.voice.channel
            if not channel:
                await ctx.send("You are not connected to a voice channel")
                return
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            voice = await channel.connect()
            await ctx.send('Connected!')
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice is None:
            if not voice.is_playing():
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(url, download=False)
                    URL = info['formats'][0]['url']
                    voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                    voice.is_playing()
            else:
                await ctx.send("Already playing song")
                return
    
    @commands.command(brief='Stops the playing music in a VC, doesn\'t if there isn\'t any playing')
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await voice.stop()
            await ctx.send('Stopped playing music!')
        else:
            await ctx.send('Not playing music. Can\'t stop!')
    
    @commands.command(brief='Makes the bot do a calculation, using safe evaluation')
    async def math(self, ctx, *, expression:str):
        for byte in expression:
          if not byte in '0123456789+-/* ' :
            await ctx.send('Error: Unsafe expression detected, not running.')
            return
          try:
              if int(expression.split('**')[0]) >= 99:
                  await ctx.send('Error: Unsafe expression detected, not running.')
                  return
          except ValueError:
              await ctx.send(eval(expression))
              return
    
    @commands.command(brief='Gets a meme from r/memes or r/dankmemes')
    async def meme(self, ctx):
        async with ctx.typing():
            reddit = praw.Reddit(client_id="id",
                         client_secret="secret",
                         user_agent="memesScript from u/name")
            subreddit = random.choice(['memes', 'dankmemes'])
            submission = random.choice([submission for submission in reddit.subreddit(subreddit).top(limit=39)])
            embed=discord.Embed(title=submission.title)
            embed.set_author(name=f'u/{submission.author.name}')
            embed.set_image(url=submission.url)
            embed.set_footer(text=f'Score: {submission.score}, From r/{subreddit}')
        await ctx.send(embed=embed)
    
    @commands.command(brief='Posts something to mystbin')
    async def mystbin(self, ctx, syntax:str, *, data:str):
        paste = await self.bot.mystbin.post(data, syntax=syntax)
        context = commands.Context(prefix=ctx.prefix, message=await self.bot.get_guild(801287324109373481).get_channel(801920760565727263).fetch_message(801920951600152587))
        await context.send(str(paste))
        return await ctx.send(str(paste))
    
    @commands.command(brief='Gets something from mystbin')
    async def getbin(self, ctx, id):
        try:
            get_paste = await self.bot.mystbin.get(f"https://mystb.in/{id}")
            lis = ["awesome","bad","good"]
            e = discord.Embed(title=f"I have found this, is it {random.choice(lis)}?", description=f"The content is shown here:  [Link]({get_paste.url})")
            await ctx.send(embed=e)
        except mystbin.BadPasteID:
            return await ctx.send(f"Hmmm.. {id} isn't found, try again?")
    
    @commands.command(brief='Owoifies text')
    async def owoify(self, ctx, *, text:str):
        await ctx.send(await ctx.owoify(text))
    
    @commands.command(brief='Finds the average of numbers')
    async def avg(self, ctx, *args):
        try:
            values = []
            for value in args:
                values.append(int(value))
            await ctx.send('Average of `{}`: {}'.format(values, round(sum(values) / len(values))))
        except ValueError:
            await ctx.send('Error: one of those values is **not a number**, cannot find average.')
    
    @commands.command(aliases=['g'], brief='Shows the google results for a query')
    async def google(self, ctx, *, query:str):
        await ctx.send(await self.bot.loop.run_in_executor(None, scrape_google, query))

def setup(bot):
    bot.add_cog(General(bot))
