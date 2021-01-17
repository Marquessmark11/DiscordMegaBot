import discord
from discord.ext import commands
from discord.ext import ui
import sqlite3
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def change_status_bot(self, ctx, *, activity='placeholder'):
        activity = discord.Game(f'{activity}')
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        await ctx.send(f'Changed activity to {activity}.')
    
    @commands.command()
    @commands.is_owner()
    async def stop_bot(self, ctx):
        emoji = '\N{THUMBS UP SIGN}'
        message = ctx.message
        await message.add_reaction(emoji)
        await ctx.bot.logout()
    
    @commands.command()
    @commands.is_owner()
    async def db(self, ctx):
        database = await ui.prompt(ctx, 'What database do you wish to execute commands on?')
        conn = sqlite3.connect(f'./Databases/{database}.db')
        c = conn.cursor()
        isdefargs = True
        commandoutput = []
        
        while isdefargs is True:
            command = await ui.prompt(ctx, 'What command do you wish to execute on this database? (type "last" at the end of your message if this is the last command you wish to execute)')
            if command.upper().startswith('SELECT '):
                action = await ui.prompt(ctx, 'SELECT command detected, would you like to recieve one row or all rows?')
                if action.upper() == 'ONE ROW':
                    c.execute(command)
                    commandoutput.append(c.fetchone())
                elif action.upper() == 'ALL ROWS':
                    for row in c.execute(command):
                        commandoutput.append(row)
            if command.upper().endswith('LAST'):
                c.execute(command[:-4])
                conn.commit()
                conn.close()
                await ctx.send(commandoutput)
                isdefargs = False
            c.execute(command)

def setup(bot):
    bot.add_cog(Admin(bot))
