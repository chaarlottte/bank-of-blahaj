from discord.ext import commands
from dotenv import load_dotenv
import os, discord
import json
from charlogger import Logger
import time

logger = Logger(True, "[Bank]", True, centered=True)

config = {  }
# prefix = '!'

logger.info("Loading configuration")

with open('config.json') as f:
    # logger.info(f.read())
    config = json.loads(f.read())

logger.info("Parsing configuration")

logger.info(config)

prefix = config["prefix"]
admins = config.get("admins")

load_dotenv()
bot_token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

# Variables

blahajEmbedColor = 0x26a9d1

# Events

@bot.event
async def on_ready():
    activity = discord.Game(name="with myself")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

# Commands

@bot.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Calculating...")
    ping = (time.monotonic() - before) * 1000

    embed=discord.Embed(title="Pong!", description="Latency: **`" + str(int(ping)) + "ms`**", color=blahajEmbedColor)
    await message.edit(content=None, embed=embed)

@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Bank of Blahaj", description="Help", color=blahajEmbedColor)

    for f in bot.commands:
        embed.add_field(name=f.name, value=prefix + f.name, inline=False)

    await ctx.send(embed=embed)

@bot.command(name="bot")
async def bot_(ctx):
    embed=discord.Embed(title="Bank of Blahaj", description="Version 1.0.0", color=0xff0000)
    embed.set_author(name=ctx.message.author)
    embed.add_field(name="Authors", value="chaarlottte/quickdaffy, refactoring/ren", inline=False)
    await ctx.send(embed=embed)

bot.run(bot_token)