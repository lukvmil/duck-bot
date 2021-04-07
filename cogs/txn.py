from discord.ext import commands, tasks
import requests
import json
from bs4 import BeautifulSoup
import consts
import storage
import re

class TxnCog(commands.Cog):

    def __init__(self, bot):
        print('Loaded TxnCog')
        self.bot = bot
        self.last_time_stamp = 0
        self.update_tx.start()
        print('Started update_tx()')

    def cog_unload(self):
        print('Unloaded TxnCog')
        self.update_tx.cancel()
        print('Stopped update_tx()')

    def demoji(self, text):
        regrex_pattern = re.compile(pattern = "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags = re.UNICODE)
        return regrex_pattern.sub(r'',text)

    # for internal use to set where to show tx updates
    @commands.command(hidden=True)
    @commands.is_owner()
    async def set_tx_channel(self, ctx):
        storage.set_val('tx_channel', ctx.channel.id)
        print(f'Set tx_channel to {ctx.channel.id}')
    
    @commands.command(aliases=['setwallet'])
    async def set_wallet(self, ctx, addr: str):
        if addr[0:3] == 'zil':
            storage.add_wallet(addr, ctx.author.id)
            await ctx.send(f'Wallet linked {ctx.author.mention} → {addr}')
        else:
            await ctx.send(f'Please enter a valid wallet address')
    
    @commands.command(aliases=['whois'])
    async def who_is(self, ctx, in_str: str):
        print(in_str)
        if in_str.startswith('<@'):
            user_id = int(in_str.replace('<@', '').replace('>', '').replace('!', ''))

            addr = storage.get_addr(user_id)

            if addr:
                await ctx.send(addr)
            else:
                await ctx.send('idk :cry: (set your addr with $setwallet)')

            print(user_id)
        
        if in_str.startswith('zil'):
            user = storage.get_user(in_str)
            print(in_str, user)

            if user:
                user_obj = await self.bot.fetch_user(user['user_id'])
                await ctx.send(user_obj.name)
            else:
                await ctx.send('idk who that is :sob:')
    
    @commands.command()
    async def contract(self, ctx):
        await ctx.send(consts.DUCK_ID)

    @tasks.loop(seconds=60.0)
    async def update_tx(self):
        tx_channel = self.bot.get_channel(storage.get_val('tx_channel'))

        if tx_channel:
            # gets html from viewblock to get latest tx
            r = requests.get(
                'https://viewblock.io/zilliqa/address/' + consts.DUCK_ID)
            soup = BeautifulSoup(r.text, "html.parser")
            script_tag = soup.find("script")

            if script_tag:
                # extracts json from html, contains list of transactions
                d = json.loads(script_tag.string.replace(
                    'window.__INITIAL_STATE__ = ', ''))
                txs = d['main']['address']['zilliqa']['map'][consts.DUCK_ID]['txs']['docs']

                # starts fresh on run, doesn't show old tx
                if not self.last_time_stamp:
                    self.last_time_stamp = txs[0]['timestamp']

                # reverses so oldest to newest
                for tx in txs[::-1]:
                    # checks if tx is newer than the last one received
                    if tx['timestamp'] > self.last_time_stamp:
                        from_id = tx['from']
                        to_id = tx['to']
                        raw_value = int(tx['value'])

                        # looking for to, from wallets in lookup table
                        name = await storage.get_name(self.bot, from_id)
                        if name:
                            from_ = '[' + self.demoji(name) + ']'
                        else:
                            from_ = from_id

                        name = await storage.get_name(self.bot, to_id)
                        if name:
                            to_ = '[' + self.demoji(name) + ']'
                        else:
                            to_ = to_id

                        # 2 decimal DUCK
                        value = raw_value / 100

                        r = requests.get(
                            'https://viewblock.io/zilliqa/tx/' + tx['hash'])
                        soup = BeautifulSoup(r.text, "html.parser")
                        script_tag = soup.find("script")

                        if script_tag:
                            # extracts json from html, contains list of transactions
                            d = json.loads(script_tag.string.replace(
                                'window.__INITIAL_STATE__ = ', ''))
                            tx_function = d['main']['tx']['zilliqa']['map'][tx['hash']]['extra']['method']

                            if tx_function == 'SwapExactZILForTokens' or tx_function == 'SwapZILForExactTokens':
                                tx_type = 'BUY'
                            elif tx_function == 'SwapExactTokensForZIL' or tx_function == 'SwapTokensForExactZIL':
                                tx_type = 'SELL'
                            elif tx_function == 'AddLiquidity':
                                tx_type = 'ADD LIQ'
                            elif tx_function == 'RemoveLiquidity':
                                tx_type = 'RM LIQ'
                            elif tx_function == 'Transfer':
                                tx_type = 'SEND'
                            elif tx_function == 'SwapExactTokensForTokens' or tx_function == 'SwapTokensForExactTokens':
                                tx_type = 'SWAP'
                            else:
                                tx_type = tx_function
                                print('New tx_type:', tx_function)

                        await tx_channel.send(
                            '`{:>5} DUCK {:<9} {:<42} → {:<42} `\n|| https://viewblock.io/zilliqa/tx/{} ||'.format(
                                value, '<' + tx_type + '>', from_, to_, tx['hash'])
                        )

                # starting place for next tx check
                self.last_time_stamp = txs[0]['timestamp']


def setup(bot):
    bot.add_cog(TxnCog(bot))
