from src.database import Database
from discord.ext import commands
from dotenv import load_dotenv
from charlogger import Logger
from discord.ext.commands.context import Context
import os, discord, time, json

logger = Logger(
    debug=True,
    default_prefix="[Bank]",
    color_text=True,
)

logger.info("Loading configuration")
config: dict = json.loads(open("config.json").read())

logger.info("Parsing configuration")
logger.info(config)

prefix: str = config.get("prefix")
admins: list = config.get("admins")

load_dotenv()
bot_token: str = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

database = Database()

# Variables
embed_color = 0x26a9d1

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

    embed = discord.Embed(title="Pong!", description=f"Latency: **`{str(int(ping))}ms`**", color=embed_color)
    await message.edit(content=None, embed=embed)

@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Bank of Blahaj", description="Help", color=embed_color)

    for f in bot.commands:
        embed.add_field(name=f.name, value=prefix + f.name, inline=False)

    await ctx.send(embed=embed)

@bot.command(name="bot")
async def bot_(ctx):
    embed = discord.Embed(title="Bank of Blahaj", description="Version 1.0.0", color=embed_color)
    embed.set_author(name=ctx.message.author)
    embed.add_field(name="Authors", value="chaarlottte/quickdaffy, refactoring/ren", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="profile")
async def profile(ctx: Context):
    user = database.get_user(ctx.author._user)
    embed = discord.Embed(title="Bank of Blahaj", description="Version 1.0.0", color=embed_color)
    embed.add_field(name="Username", value=f"{user.discord_username}", inline=True)
    embed.add_field(name="Balance", value=f"{user.balance}", inline=True)
    await ctx.send(embed=embed)

bot.run(bot_token)