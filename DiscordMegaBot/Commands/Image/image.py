import discord
from discord.ext import commands
from asyncdagpi import ImageFeatures

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def colors(self, ctx, member:discord.Member=None):
        if member is None:
            member = ctx.author
        
        url = str(member.avatar_url_as(format="png", size=1024))
        img = await self.bot.dag.image_process(ImageFeatures.colors(), url)
        await ctx.send(file = discord.File(fp=img.image,filename=f"pixel.{img.format}"))
    
    @commands.command()
    async def wanted(self, ctx, member:discord.Member=None):
        if member is None:
            member = ctx.author
        warn_msg = 'the dagpi wanted endpoint has a flaw which makes it very slow to compute' if ctx.author.id in self.bot.owner_ids else 'This may take some time'
        warn = await ctx.send(warn_msg)
        url = str(member.avatar_url_as(format="png", size=1024))
        img = await self.bot.dag.image_process(ImageFeatures.wanted(), url)
        try:
            await warn.delete()
        except:
            pass
        finally:
            await (commands.Context(prefix=ctx.prefix, message=ctx.message)).send(file = discord.File(fp=img.image,filename=f"pixel.{img.format}"))

def setup(bot):
    bot.add_cog(Image(bot))
