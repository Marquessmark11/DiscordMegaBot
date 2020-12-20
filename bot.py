import discord as api
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingRequiredArgument, BadArgument, MissingPermissions
from discord.utils import get
from properties import prefix, token, intents, insensitiveCase, ownerID
from discord.ext import ui

intents = api.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=insensitiveCase, owner_id=ownerID)
bot.remove_command('help')
bot.commands_since_restart = 0
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

def who(person, command):
    trigger = f'{person} just ran {command}'
    return trigger

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'Commands.{extension.capitalize()}.{extension}')
    message = ctx.message
    await message.add_reaction('<:greenTick:596576670815879169>')

@bot.command()
@commands.is_owner()
async def unload(ctx, folder, extension):
    bot.unload_extension(f'Commands.{extension.capitalize()}.{extension}')
    message = ctx.message
    await message.add_reaction('<:greenTick:596576670815879169>')

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.reload_extension(f'Commands.{extension.capitalize()}.{extension}')
    message = ctx.message
    await message.add_reaction('<:greenTick:596576670815879169>')

for category in os.listdir('./Commands'):
    for cog in os.listdir(f'./Commands/{category}'):
        if cog.endswith('.py'):
            bot.load_extension(f'Commands.{category}.{cog[:-3]}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

@bot.event
async def on_message_edit(before, after):
    if after.content.startswith(prefix):
        await bot.process_commands(after)

@bot.event
async def on_message(message):
    if message.content.startswith(prefix):
        bot.commands_since_restart += 1
    await bot.process_commands(message)

bot.run(token)
