import discord
from discord.ext import commands
from discord.ext import ui
from discord.utils import get
import random

def oauth2link():
    link = discord.utils.oauth_url(client_id=741624868591763487, permissions=discord.Permissions(permissions=8))
    e = discord.Embed(title='Invite DMB To your server', description=f'[:robot: Invite Link]({link})', color=random.randint(100000, 999999))
    return e

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def whoOwns(self, ctx):
        owner = ctx.guild.owner
        print(owner)
        await ctx.send(f'{owner.display_name} owns this server')
    
    @commands.command()
    async def whoHas(self, ctx, *, role:discord.Role=None):
        if role == None:
            role = await ui.prompt(ctx, 'What role?')
            role = get(ctx.guild.roles, name=role)
        role_members = []
        for role_member in role.members:
            role_members.append(role_member.display_name)
            if len(role_members) == 0:
                await ctx.send(f'No one has {role}!')
                return
        await ctx.send(', \n'.join(role_members))
    
    @commands.command()
    async def allRoles(self, ctx):
        roles = []
        for role in ctx.guild.roles:
            roles.append(role.name)
        output = ', \n'.join(roles)
        await ctx.send(output.strip('@everyone, '))

    @commands.command()
    async def serverIcon(self, ctx, server):
        guild = get(self.bot.guilds, name=server)
        server = self.bot.get_guild(guild.id)
        await ctx.send(server.icon_url)
    
    @commands.command()
    async def allMembers(self, ctx):
        members = []
        for member in ctx.guild.members:
            members.append(member.display_name)
        await ctx.send(', \n'.join(members))
    
    @commands.command()
    async def allBots(self, ctx):
        bots = []
        for member in ctx.guild.members:
            if member.bot:
                bots.append(member.display_name)
        await ctx.send(', \n'.join(bots))
    
    @commands.command()
    async def allChannels(self, ctx):
        channels = []
        for channel in ctx.guild.text_channels:
            channels.append(channel.name)
        await ctx.send(', \n'.join(channels))
    
    @commands.command()
    async def announce(self, ctx, channel_name, *, announcement=None):
        if announcement == None:
            announcement = await ui.prompt(ctx, 'What would you like to announce?')
        elif announcement != None:
            announcement_channel = get(ctx.guild.text_channels, name=channel_name)
            await announcement_channel.send(announcement)
    
    @commands.command()
    async def serverInfo(self, ctx, *, guild=None):
        guild = get(self.bot.guilds, name=guild)
        if guild == None:
            guild = ctx.guild
        c = random.randint(100000, 999999)
        info = discord.Embed(color=c)
        info.set_author(name=guild)
        info.set_thumbnail(url=guild.icon_url)
        info.add_field(name='Created At', value=guild.created_at)
        info.add_field(name='Member Count', value=len(guild.members), inline=False)
        info.add_field(name='Server ID', value=guild.id, inline=False)
        info.add_field(name='Server Owner', value=guild.owner.mention, inline=False)
        info.add_field(name='Server Region', value=guild.region, inline=False)
        await ctx.send(embed=info)

def setup(bot):
    bot.add_cog(Server(bot))
