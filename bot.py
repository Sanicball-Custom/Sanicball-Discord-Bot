import os
import urllib.request
import discord
from discord.ext import commands
from dotenv import load_dotenv
import soupsieve
import bs4

sanic_colour = 0x4D76B2

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!s ")
server_list_url = "https://sanicball.bdgr.zone/servers/"


@bot.command(name="status")
async def status(ctx):

    with urllib.request.urlopen(server_list_url) as response:
        html = response.read()
    html = str(html)[2:-1].split("<br>")
    html.pop()
    print(html)

    embed = discord.Embed(title="Sanicball servers status", description=f"There are currently {len(html)} public servers online", url=server_list_url, color=sanic_colour)

    for entry in html:
        _split = entry.split(":")
        embed.add_field(name=entry, value=f'ip: {_split[0]}\n'
                                          f'port: {_split[-1]}', inline=False)
    await ctx.send(embed=embed)


bot.run(TOKEN)
