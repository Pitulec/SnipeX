import requests
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

base_url = "https://api.battlemetrics.com/"

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def test(ctx):
    await ctx.send("Hello")

@bot.command()
async def find(ctx, username):
    url = f"{base_url}/players?page%5Bsize%5D=10&fields%5Bserver%5D=name&filter%5Bsearch%5D={username}&filter%5BplayerFlags%5D=&filter%5Bserver%5D%5Bgame%5D=rust&include=flagPlayer%2CplayerFlag%2Cserver"
    response = requests.get(url).json()
    for player in response['data']:
        print(f"Nick: {player['attributes']['name']} \n Online: {player['relationships']['servers']['data'][0]['meta']['online']}")
    # print(response['data'][0])

bot.run('TOKEN')