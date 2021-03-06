from discord.ext import commands
import discord
import os

class OwnerCog(commands.Cog):
    
    def __init__(self, bot):
        print('Loaded OwnerCog')
        self.bot = bot
    
    def cog_unload(self):
        print('Unloaded OwnerCog')

    @commands.command(name='load', hidden=True)
    @commands.has_any_role('admin', 'Community Duck')
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'{type(e).__name__} - {e}')
        else:
            await ctx.send('Success!')
    
    @commands.command(name='unload', hidden=True)
    @commands.has_any_role('admin', 'Community Duck')
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'{type(e).__name__} - {e}')
        else:
            await ctx.send('Success!')
    
    @commands.command(name='reload', hidden=True)
    @commands.has_any_role('admin', 'Community Duck')
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'{type(e).__name__} - {e}')
        else:
            await ctx.send('Success!')
    
    @commands.command(name='quit', hidden=True)
    @commands.is_owner()
    async def quit(self, ctx):
        print('Shutting down...')
        await self.bot.close()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def transmit(self, ctx, *, msg: str):
        await ctx.send(msg)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong :wink:')
    
    @commands.command()
    @commands.is_owner()
    async def get_update(self, ctx):
        os.system('git pull')
        await ctx.send('Got update.')
        await ctx.send('Reloading all cogs...')
        self.bot.unload_extension('cogs.owner')
        self.bot.load_extension('cogs.owner')
        self.bot.unload_extension('cogs.ticker')
        self.bot.load_extension('cogs.ticker')
        self.bot.unload_extension('cogs.txn')
        self.bot.load_extension('cogs.txn')
        await ctx.send('Done!')

def setup(bot):
    bot.add_cog(OwnerCog(bot))