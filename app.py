import discord
from discord.ext import commands

initial_extensions = [
    'cogs.owner',
    'cogs.ticker',
    'cogs.txn'
]

bot = commands.Bot(command_prefix='$')
    

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id}) on {" ".join([f"[{x.name}]" for x in bot.guilds])}')
    
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run(
    open('token.txt', 'r').read(),
    bot=True,
    reconnect=True
)