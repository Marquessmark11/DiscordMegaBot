import discord
from discord.ext import commands
import random
from datetime import datetime as dt
from selenium import webdriver
from asyncio import sleep
import inspect
import os
from discord.ext import flags
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

def oauth2link():
    link = discord.utils.oauth_url(client_id=741624868591763487, permissions=discord.Permissions(permissions=8))
    e = discord.Embed(title='Invite DMB To your server', description=f'[:robot: Invite Link]({link})', color=random.randint(100000, 999999))
    return e

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def distracted(self, ctx):
        await ctx.send('https://tenor.com/bop5H.gif')
    
    @commands.command()
    async def getstickbuggedlol(self, ctx):
        await ctx.send('https://tenor.com/bnQ1p.gif')

    @commands.command()
    async def echo(self, ctx, *, content:commands.clean_content):
        await ctx.send(content)
    
    @commands.command()
    async def life(self, ctx):
        await ctx.send('Life,\nIt has no meaning')
    
    @commands.command()
    async def rcolor(self, ctx):
        r = random.randint(100000, 999999)
        e = discord.Embed(title='Random Color', description=f'0x{r}', color=r)
        await ctx.send(embed=e)
    
    @commands.command()
    async def randomCharacter(self, ctx):
        r = random.randint(0, 2000)
        c = chr(r)
        await ctx.send(c)
    
    @commands.command()
    async def abcFull(self, ctx):
        var = 'a'
        alphabets = []
        # starting from the ASCII value of 'a' and keep increasing the
        # value by i.
        alphabets=[(chr(ord(var)+i)) for i in range(26)]
        await ctx.send(''.join(alphabets))
    
    @commands.command()
    async def shrug(self, ctx):
        await ctx.send('¯\_(ツ)_/¯')
    
    @commands.command()
    async def lenny(self, ctx):
        await ctx.send('( ͡° ͜ʖ ͡°)')
    
    @commands.command()
    async def pengoeatfish(self, ctx):
        await ctx.send("https://cdn1.vectorstock.com/i/1000x1000/16/85/penguin-eating-fish-on-ice-vector-6581685.jpg")
    
    @commands.command()
    async def help(self, ctx, category:str=None):
      co = random.randint(100000, 999999)
      if category is None:
          helpc = discord.Embed(color=co, title='Help Categories')
          helpc.add_field(name='Categories', value="""
```
General
Server
Games
Member
Moderation
```
Please choose one.
          """)
          await ctx.send(embed=helpc)
      if category.upper() == 'GENERAL':
          general = discord.Embed(color=co, title='General Commands', description='distracted\ngetstickbuggedlol\necho\nlife\nrcolor\nrandomCharacter\nabcFull\nshrug\nlenny\npengoeatfish\nhelp\nwhattodotoday\nspam\ncount\ninvite\ncouch\nfoo\nping\nabc\ncat\ndog\nbird\nhello\nrandom\nlick\nkiss\nsource\nuptime')
          await ctx.send(embed=general)
      elif category.upper() == 'SERVER':
          server = discord.Embed(color=co, title='Server Commands', description='whoOwns\nwhoHas\nallRoles\nserverIcon\nallMembers\nallBots\nallChannels')
          await ctx.send(embed=server)
      elif category.upper() == 'GAMES':
          games = discord.Embed(color=co, title='Games', description='rps\n8ball\nchoice\npseudotext\nroll\nspinner\nscramble\nreverse\ncoinflip\nupsidedown\neat')
          await ctx.send(embed=games)
      elif category.upper() == 'MEMBER':
          member = discord.Embed(color=co, title='Member Commands', description='yourAvatar\nyourDiscordPFP\ndm\nwhoIs')
          await ctx.send(embed=member)
      elif category.upper() == 'MODERATION':
          moderation = discord.Embed(color=co, title='Moderation Commands', description='announce\nwarn\nclear\nkick\nban\nunban')
          await ctx.send(embed=moderation)
      else:
          await ctx.send('That isn\'t a category!')
    
    @commands.command()
    async def whattodotoday(self, ctx):
        await ctx.send('To-do list: First item on this list is ahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    
    @commands.command()
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
    
    @commands.command()
    async def count(self, ctx, ending=100):
        for x in range(ending + 1):
            await ctx.send(x)
    
    @commands.command()
    async def invite(self, ctx):
        await ctx.send(embed = oauth2link())
    
    @commands.command()
    async def couch(self, ctx):
        for x in 'COUCH':
            await ctx.send('COUCH')
    
    @commands.command()
    async def foo(self, ctx):
        await ctx.send('bar')

    @commands.command()
    async def ping(self, ctx):
        latency = round((self.bot.latency * 1000), 6)
        color = random.randint(100000, 999999)
        e = discord.Embed(title=':ping_pong: Pong!', color=color, description=f'Latency: {latency}ms')
        e.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=e)
    
    @commands.command()
    async def abc(self, ctx):
        await ctx.send('You know your abc\'s, right?')
    
    @commands.command()
    async def cat(self, ctx):
        await ctx.send('Meow')
    
    @commands.command()
    async def dog(self, ctx):
        await ctx.send('Woof')
    
    @commands.command()
    async def bird(self, ctx):
        await ctx.send('Chirp')
    
    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hi!')
    
    @commands.command(name='random')
    async def _random(self, ctx, minimum : int=0, maximum : int=2147483647):
        randomnumber = random.randint(minimum, maximum)
        await ctx.send(str(randomnumber) + " was chosen")
    
    @commands.command()
    async def lick(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        
        await ctx.send(f'Bot: *licks {member.mention}*\n{member.mention}: Ew stop that')
    
    @commands.command()
    async def technicalInfo(self, ctx):
        integer = random.randint(100000, 999999)
        e = discord.Embed(color=integer)
        e.set_footer(text='@Copyright 2020 Connor Tippets')
        e.set_thumbnail(url=self.bot.user.avatar_url)
        e.set_author(name='Technical Info', icon_url=self.bot.user.avatar_url)
        e.add_field(name='Discord.py Release Level: ', value=f'{discord.version_info.releaselevel}', inline=False)
        e.add_field(name='Discord.py Release: ', value=f'{str(discord.__version__)}', inline=False)
        await ctx.send(embed=e)
    
    @commands.command()
    async def verify(self, ctx):
        if ctx.guild.name == 'The Good Guy Server':
            await ctx.message.delete()
            role_id = 758538458951843843
            role = get(ctx.guild.roles, id=role_id)
            await ctx.author.add_roles(role)
        elif ctx.guild.name != 'The Good Guy Server':
            await ctx.send('wrong guild')
    
    @commands.command()
    async def kiss(self, ctx, member:discord.Member=None):
        if member is None or member == ctx.author:
            await ctx.send(f'{ctx.author} kissed themselves...')
            return
        await ctx.send(f'{member.name} was kissed by {ctx.author}!')
    
    @commands.command()
    async def botInfo(self, ctx):
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
        await ctx.send(embed=e)
     
    @commands.command()
    async def allCommands(self, ctx):
        await ctx.send(len(self.bot.commands))
    
    @commands.command()
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

        final_url = f'<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>'
        await ctx.send(final_url)
    
    @commands.command()
    async def source_direct(self, ctx, *, command:str = None):
        await ctx.send('```py\n' + inspect.getsource(self.bot.get_command(command).callback) + '```')
    
    @commands.command(aliases=['connect'])
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice = await channel.connect()
        await ctx.send('Connected!')
    
    @commands.command(aliases=['disconnect'])
    async def leave(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        await voice.disconnect()
        await ctx.send('Disconnected!')
    
    @commands.command()
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
    
    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await voice.stop()
            await ctx.send('Stopped playing music!')
        else:
            await ctx.send('Not playing music. Can\'t stop!')
    
    @commands.command()
    async def math(self, ctx, expression):
        for byte in expression:
          if not byte in '0123456789+-/*':
            await ctx.send('Hey! I can see what you\'re doing.')
            return
          else:
            await ctx.send(eval(expression))
            return

def setup(bot):
    bot.add_cog(General(bot))
