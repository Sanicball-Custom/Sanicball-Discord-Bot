#!/usr/bin/python3

import os
from urllib import request
import discord
from discord.ext import commands
from dotenv import load_dotenv
import srcomapi as speedrun
from sanicball import ServerList

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
        embed = discord.Embed(title="Sanicball Categories",
                              description=f"there are {len(sanic.categories)} categories in Sanicball",
                              color=sanic_colour, url="https://www.speedrun.com/sanicball")
        for category in sanic.categories:
            embed.add_field(name=category.name, value="will add helpful description here soon xd", inline=False)
        await ctx.send(embed=embed)


@bot.command(name="status")
async def status(ctx):
    servers = ServerList(server_list_url)

    embed = discord.Embed(title="Sanicball servers status",
                          description=f"There are currently {len(servers.servers)} public servers online",
                          url=server_list_url,
                          color=sanic_colour)
    i = 0
    for server in servers.servers:
        i += 1
        embed.add_field(name=f"{i}: {server.name}", value=f'ip: {server.ip}\n'
                                                          f'port: {server.port}', inline=False)
    await ctx.send(embed=embed)


@bot.command(name="info")
async def info(ctx, server):
    if not server.isdigit():
        ctx.send(f"Server id must be a number!")
        return

    server = ServerList(server_list_url).servers[int(server) - 1]
    embed = discord.Embed(title=server.name, description=f"ip: {server.ip}\n"
                                                         f"port: {server.port}", url=server_list_url,
                          colour=sanic_colour)
    embed.add_field(name="status", value=f"Max players: {server.max_players}\n"
                                         f"Players racing: {server.players}\n"
                                         f"Is racing: {'yes' if server.is_racing else 'no'}")
    await ctx.send(embed=embed)


bot.run(TOKEN)
