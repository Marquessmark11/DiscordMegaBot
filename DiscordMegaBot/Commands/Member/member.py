import discord
from discord.ext import commands
import random

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief='Shows you the avatar of the person you choose, it will be you if you don\'t choose one')
    async def yourAvatar(self, ctx, *, member:discord.Member=None):
        if member == None:
            member = ctx.author
        e = discord.Embed(color=discord.Color.random())
        e.set_image(url=member.avatar_url)
        await ctx.send(embed=e)
    
    @commands.command(brief='Shows you the discord version of the avatar of the person you choose, you if none chosen')
    async def yourDiscordPFP(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        avatar = member.default_avatar_url
        await ctx.send(avatar)
    
    @commands.command(brief='Dm\'s the person you choose')
    async def dm(self, ctx, member : discord.Member, *, text="placeholder"):
        if member.dm_channel == None:
            channel = await member.create_dm()
            await channel.send(text)
            await ctx.send(f'`{text}` was sent to {member.display_name}')
        elif member.dm_channel != None:
            await member.dm_channel.send(text)
            await ctx.send(f'`{text}` was sent to {member.display_name}')
    
    @commands.command(brief='Shows you info on the person you choose, you if none chosen')
    async def whoIs(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        membersRolesNames = []
        for role in member.roles:
            membersRolesNames.append(role.name)
        integer = random.randint(100000, 999999)
        e = discord.Embed(color=integer)
        e.set_footer(text='@Copyright 2020 Connor Tippets')
        e.set_thumbnail(url=member.avatar_url)
        e.set_author(name=member.name, icon_url=member.avatar_url)
        e.add_field(name='Nickname/Name: ', value=f'{member.display_name}', inline=False)
        e.add_field(name='Id: ', value=f'{member.id}', inline=False)
        e.add_field(name='Bot?: ', value=f'{member.bot}', inline=False)
        e.add_field(name='Tag: ', value=f'{member.discriminator}', inline=False)
        membersRolesNames.remove('@everyone')
        e.add_field(name='Roles: ', value=f'\n'.join(membersRolesNames), inline=False)
        await ctx.send(embed=e)
    
    @commands.command(brief='Says if you have the role chosen')
    async def doIHave(self, ctx, *, role:discord.Role):
        for member in role.members:
            if member.id == ctx.author.id:
                await ctx.send(f'You have {role.name}')
                return
        await ctx.send(f'You don\'t have {role.name}')

def setup(bot):
    bot.add_cog(General(bot))
