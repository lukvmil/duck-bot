from discord.ext import commands, tasks
import discord
import requests, json, asyncio

class TickerCog(commands.Cog):

    def __init__(self, bot):
        print('Loaded TickerCog')
        self.bot = bot
        self.update_ticker.start()
        print('Started update_ticker()')
    
    def cog_unload(self):
        print('Unloaded TickerCog')
        self.update_ticker.cancel()
        print('Stopped update_ticker()')

    @tasks.loop(seconds=10.0)
    async def update_ticker(self):
        # getting DUCK -> ZIL exchange
        r = requests.get('https://api.zilstream.com/rates/latest')
        rates = json.loads(r.text)

        duck_price = 0

        for rate in rates:
            if rate['symbol'] == 'DUCK':
                duck_price = rate['rate']

        # getting ZIL -> USD exchange
        r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=zilliqa&vs_currencies=usd')
        rates = json.loads(r.text)

        zil_price = rates['zilliqa']['usd']

        duck_price_usd = zil_price * duck_price

        if duck_price:
            await self.bot.change_presence(
                activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f'{round(duck_price)} ZIL | ${round(duck_price_usd)} USD'
            ))


def setup(bot):
    bot.add_cog(TickerCog(bot))
