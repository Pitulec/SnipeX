import requests
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
BM_TOKEN = os.getenv("BM_TOKEN")

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

base_url = "https://api.battlemetrics.com"
headers = {"Authorization": f"Bearer {BM_TOKEN}"}

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def test(ctx):
    await ctx.send("This command works!")

@bot.command()
async def find(ctx, username: str):
    url = (
        f"{base_url}/players?"
        f"page[size]=10&"
        f"fields[server]=name&"
        f"filter[search]={username}&"
        f"filter[playerFlags]=&"
        f"filter[server][game]=rust&"
        f"include=flagPlayer,playerFlag,server"
    )

    players = requests.get(url, headers=headers).json()['data']

    embed = discord.Embed(title="Results", color=discord.Color.red())

    for player in players:
        if player['relationships']['servers']['data'][0]['meta']['online']:
            status = ":green_circle: - Online"
        else:
            status = ":red_circle: - Offline"
    
        embed.add_field(
            name="",
            value=f"[{player['attributes']['name']}](https://www.battlemetrics.com/players/{player['attributes']['id']})\n{status}",
            inline=False
        )

    embed.set_footer(text="Made by Pitulec")
    await ctx.send(embed=embed)

bot.run(TOKEN)
