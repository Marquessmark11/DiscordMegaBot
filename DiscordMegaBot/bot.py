import discord as api
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingRequiredArgument, BadArgument, MissingPermissions
from discord.utils import get
from properties import prefix, token, intents, insensitiveCase, ownerID, dagpi_token
from discord.ext import ui
from jishaku.cog import jsk
import time, datetime, humanize
import json
import subprocess as sp
from Utils.utils import DMBText, DMBot, utils
from asyncdagpi import Client
import mystbin

start = time.time()
intents = api.Intents.default()
intents.members = True
prefixes_db_path = './prefixes.json'

def get_prefix(bot, message):
    if message.guild is None:
        return ''
    else:
        if message.author.id in (376129806313455616, 528290553415335947):
            return [f'<@!{bot.user.id}> ', f'<@!{bot.user.id}>', bot.prefixes.get(str(message.guild.id)) or ':', '']
        else:
            return [f'<@!{bot.user.id}> ', f'<@!{bot.user.id}>', bot.prefixes.get(str(message.guild.id)) or ':']

bot = DMBot(command_prefix=get_prefix, intents=intents, case_insensitive=insensitiveCase, owner_ids={376129806313455616, 528290553415335947})

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
    for category in os.listdir('./Commands'):
        for cog in os.listdir(f'./Commands/{category}'):
            if cog.endswith('.py') and cog != '__init__.py':
                bot.load_extension(f'Commands.{category}.{cog[:-3]}')
                if cog == 'statuses.py':
                    from Commands.Statuses.statuses import Status
                    cog_status = Status(bot)
                    cog_status.change_status.start()
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
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    else:
        await ctx.send('```py\n' + str(error) + '\n```')
        raise error

@bot.ipc.route()
async def get_member_count(data):
    guild = bot.get_guild(
        data.guild_id
    )  # get the guild object using parsed guild_id

    return guild.member_count  # return the member count to the client

@bot.event
async def on_message_edit(before, after):
    if after.content.startswith(tuple(get_prefix(bot, after))):
        await bot.process_commands(after)

@bot.event
async def on_command_completion(ctx):
    bot._commands += 1

@bot.event
async def on_message(message):
    if message.content == f'<@!{bot.user.id}>':
        embed = api.Embed(title='Hello!', color=api.Color.green(), description=f'My prefix is {get_prefix(bot, message)[2]}, and you can mention me, of course.')
        await message.channel.send(embed=embed)
    await bot.process_commands(message)

bot.ipc.start()
bot.run(token)
