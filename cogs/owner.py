from discord.ext import commands
import discord

class OwnerCog(commands.Cog):
    
    def __init__(self, bot):
        print('Loaded OwnerCog')
        self.bot = bot
    
    def unload_cog(self):
        print('Unloaded OwnerCog')

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'{type(e).__name__} - {e}')
        else:
            await ctx.send('Success!')
    
    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'{type(e).__name__} - {e}')
        else:
            await ctx.send('Success!')
    
    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
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
        print(ctx.author.id)
        # await ctx.send('pong :wink:')
        await ctx.send(
            embed=discord.Embed(description="0.1 :duck: TRANSFER zil1y76r2hteww2v0kjfergalexa9u3m28xqywcd73 → zil1hdn75udaj43sh5fht0w7dtm7uvhqsqlzrrvxau [tx](https://viewblock.io)", color=0xFF5733)
        )
        await ctx.send(
            embed=discord.Embed(description="0.15 :duck: SELL zil1ynknmtrg58c2df54k806ev7h76ntmq9adnj4j2 [tx](https://viewblock.io)", color=0xFF5733)
        )
        await ctx.send(
            embed=discord.Embed(description="0.5 :duck: LIQUIDITY ADD zil10pgrrvrx7nmz8v8aufe7324sr6ceqta5udtlcm [tx](https://viewblock.io)", color=0xFF5733)
        )
    

def setup(bot):
    bot.add_cog(OwnerCog(bot))