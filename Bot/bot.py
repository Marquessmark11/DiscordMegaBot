import discord as api
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingRequiredArgument, BadArgument, MissingPermissions
from discord.utils import get
from properties import prefix, token, intents, insensitiveCase, ownerID
from discord.ext import ui
from jishaku.cog import jsk
import time, datetime, humanize
import json
import subprocess as sp
from tools import helper

start = time.time()
intents = api.Intents.default()
intents.members = True
intents.presences = True
prefixes_db_path = './Databases/prefixes.json'

def get_prefix(bot, message):
    with open(prefixes_db_path, 'r') as f:
        prefixes = json.load(f)
    
    return prefixes[str(message.guild.id)]

bot = commands.AutoShardedBot(command_prefix=get_prefix, intents=intents, case_insensitive=insensitiveCase, owner_id=ownerID)
bot.remove_command('help')
bot.commands_since_restart = 0
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"
bot.load_extension('jishaku')

def who(person, command):
    trigger = f'{person} just ran {command}'
    return trigger

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(f'Commands.{extension.capitalize()}.{extension}')
        message = ctx.message
        await message.add_reaction('\U00002705')
    except commands.ExtensionFailed as e:
        await ctx.send(e)
        await ctx.message.add_reaction('\U0000274e')

@bot.command()
@commands.is_owner()
async def unload(ctx, folder, extension):
    try:
        bot.unload_extension(f'Commands.{extension.capitalize()}.{extension}')
        message = ctx.message
        await message.add_reaction('\U00002705')
    except commands.ExtensionFailed as e:
        await ctx.send(e)
        await ctx.message.add_reaction('\U0000274e')

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        bot.reload_extension(f'Commands.{extension.capitalize()}.{extension}')
        message = ctx.message
        await message.add_reaction('\U00002705')
    except commands.ExtensionFailed as e:
        await ctx.send(e)
        await ctx.message.add_reaction('\U0000274e')

@bot.event
async def on_ready():
    def uptime_seconds():
        end = time.time()
        difference = end - start
        return difference
    
    def uptime_delta():
        difference = uptime_seconds()
        delta = datetime.timedelta(seconds=difference)
        return delta
    
    def uptime_delta_humanized():
        delta = uptime_delta()
        humandelta = humanize.naturaldelta(delta)
        return humandelta
    
    def uptime_delta_humanized_precise():
        delta = uptime_delta()
        humandeltaprecise = humanize.precisedelta(delta)
        return humandeltaprecise
    
    bot.uptime_seconds = uptime_seconds
    bot.uptime_delta = uptime_delta
    bot.uptime_delta_humanized = uptime_delta_humanized
    bot.uptime_delta_humanized_precise = uptime_delta_humanized_precise

    for category in os.listdir('./Commands'):
        for cog in os.listdir(f'./Commands/{category}'):
            if cog.endswith('.py'):
                bot.load_extension(f'Commands.{category}.{cog[:-3]}')
    
    for guild in bot.guilds:
        with open(prefixes_db_path, 'r') as f:
            prefixes = json.load(f)
        
        if prefixes.get(str(guild.id)) is None:
            prefixes[str(guild.id)] = prefix
            
            with open(prefixes_db_path, 'w') as f:
                json.dump(prefixes, f, indent=4)
        
        elif not prefixes.get(str(guild.id)) is None:
            continue
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

@bot.event
async def on_guild_join(guild):
    with open(prefixes_db_path, 'r') as f:
        prefixes = json.load(f)
    
    prefixes[str(guild.id)] = prefix
    
    with open(prefixes_db_path, 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open(prefixes_db_path, 'r') as f:
        prefixes = json.load(f)
    
    prefixes.pop(str(guild.id))
    
    with open(prefixes_db_path, 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.command(aliases=['changeprefix'])
@has_permissions(administrator=True)
async def setprefix(ctx, prefix:str):
    with open(prefixes_db_path, 'r') as f:
        prefixes = json.load(f)
    
    prefixes[str(ctx.guild.id)] = prefix
    
    with open(prefixes_db_path, 'w') as f:
        json.dump(prefixes, f, indent=4)
    
    try:
        await ctx.guild.me.edit(nick=f'[{prefix}] Discord Mega Bot')
        await ctx.send(f'Successfully changed server prefix to `{prefix}`')
    except api.HTTPException:
        await ctx.send('Nickname must be 32 or fewer in length! Although, i did change the prefix')

@bot.event
async def on_message_edit(before, after):
    if after.content.startswith(get_prefix(bot, after)):
        await bot.process_commands(after)

@bot.event
async def on_message(message):
    if message.content.startswith(get_prefix(bot, message)):
        bot.commands_since_restart += 1
    elif helper.bot_mentioned_in(message):
        await message.channel.send('what do you want')
    await bot.process_commands(message)

@bot.command()
async def sync(ctx):
    """Get the most recent changes from the GitHub repository
    Uses: p,sync"""
    #credit to vaskel at penguin-bot repo
    embedvar = api.Embed(title="Syncing...", description="Syncing with the GitHub repository, this should take up to 15 seconds",
                             color=0xff0000, timestamp=ctx.message.created_at)
    msg = await ctx.send(embed=embedvar)
    async with ctx.channel.typing():
        c = bot.get_guild(768679097042862100).get_channel(768679097042862103)
        output = sp.getoutput('git pull git@github.com:ConnorTippets/DiscordMegaBot/.git main')
        await c.send(f""" ```sh
        {output} ```""")
        msg1 = await ctx.send("Success!")
        await msg1.delete()
        embedvar = api.Embed(title="Synced", description="Sync with the GitHub repository has completed, check the logs to make sure it worked",
                                 color=0x00ff00, timestamp=ctx.message.created_at)

bot.run(token)
