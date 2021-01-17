import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @has_permissions(kick_members=True)
    async def warn(self, ctx, member : discord.Member, *, reason='placeholder'):
        await ctx.send(member.mention + ' has been warned for the reason of ' + reason)
        await member.send('You were warned in {} with the reason of {}'.format(ctx.guild.name, reason))
    
    @commands.command()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, clear_amount=5):
        clear_amount = clear_amount + 1
        new_clear_amount = clear_amount - 1
        if new_clear_amount != 1:
            if new_clear_amount > 250:
                await ctx.send('Error Code 007: Max clear amount is 250')
            elif new_clear_amount < 250:
                await ctx.channel.purge(limit=clear_amount)
                await ctx.send(f':thumbsup: {new_clear_amount} messages have been cleared')
            elif new_clear_amount == 250:
                await ctx.channel.purge(limit=clear_amount)
                await ctx.send(f':thumbsup: {new_clear_amount} messages have been cleared')
        elif new_clear_amount == 1:
            await ctx.message.delete()
            await ctx.send(f':thumbsup: {new_clear_amount} message have been cleared')
    
    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked by {ctx.author} for the reason of {reason}")
        await member.send('You were kicked in {} for the reason of {}'.format(ctx.guild.name, reason))
    
    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member} has been banned by {ctx.author} for the reason of {reason}")
        await member.send("You were banned in {} for the reason of {}".format(ctx.guild.name, reason))
    
    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_user = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_user:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member.discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.name}#{user.discriminator} has been unbanned by {ctx.author}")
                return

def setup(bot):
    bot.add_cog(Moderation(bot))
