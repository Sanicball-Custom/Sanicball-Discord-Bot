#!/usr/bin/python3

import os
from urllib import request
import discord
from discord.ext import commands
from dotenv import load_dotenv
import srcomapi as speedrun

sanic_colour = 0x4D76B2

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!s ")
server_list_url = "https://sanicball.bdgr.zone/servers/"

api = speedrun.SpeedrunCom()
api.debug = 1

sanic = api.search(speedrun.datatypes.Game, {"name": "sanicball"})[0]


@bot.command(name="tracks")
async def tracks(ctx):
    with ctx.typing():
        embed = discord.Embed(title="Sanicball Tracks", description=f"There are {len(sanic.levels)} laps in Sanicball",
                              color=sanic_colour, url="https://www.speedrun.com/sanicball")
        for level in sanic.levels:
            embed.add_field(name=level.name, value="will add helpful description here soon xd", inline=False)
        await ctx.send(embed=embed)


@bot.command(name="categories")
async def categories(ctx):
    with ctx.typing():
        embed = discord.Embed(title="Sanicball Categories", description=f"there are {len(sanic.categories)} categories in Sanicball",
                              color=sanic_colour, url="https://www.speedrun.com/sanicball")
        for category in sanic.categories:
            embed.add_field(name=category.name, value="will add helpful description here soon xd", inline=False)
        await ctx.send(embed=embed)


@bot.command(name="status")
async def status(ctx):
    with ctx.typing():
        with request.urlopen(server_list_url) as _response:
            html = _response.read()
        html = str(html)[2:-1].split("<br>")
        html.pop()
        print(html)

        embed = discord.Embed(title="Sanicball servers status",
                              description=f"There are currently {len(html)} public servers online", url=server_list_url,
                              color=sanic_colour)

        for entry in html:
            _split = entry.split(":")
            embed.add_field(name=entry, value=f'ip: {_split[0]}\n'
                                              f'port: {_split[-1]}', inline=False)
        await ctx.send(embed=embed)


bot.run(TOKEN)
