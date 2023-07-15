from src.database import Database
from discord.ext import commands
from dotenv import load_dotenv
from charlogger import Logger
from discord.ext.commands.context import Context
import os, discord, time, json, time, random

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
income_delay_in_seconds: int = config.get("income_delay_in_seconds")

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

    embed = discord.Embed(title="pong!", description=f"Latency: **`{str(int(ping))}ms`**", color=embed_color)
    await message.edit(content=None, embed=embed)

@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="blahaj", color=embed_color)

    for f in bot.commands:
        embed.add_field(name=f.name, value=prefix + f.name, inline=False)

    await ctx.send(embed=embed)

@bot.command(name="bot")
async def bot_(ctx):
    embed = discord.Embed(title="blahaj", color=embed_color)
    embed.set_author(name=ctx.message.author)
    embed.add_field(name="Authors", value="chaarlottte/quickdaffy, refactoring/ren", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="balance")
async def user_balance(ctx: Context):
    user = database.get_user(ctx.author._user)
    embed = discord.Embed(title="blahaj", color=embed_color)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.add_field(name="Cash", value=f"{user.cash}")
    embed.add_field(name="Bank", value=f"{user.bank}")
    embed.add_field(name="Total", value=f"{user.cash + user.bank}")
    await ctx.send(embed=embed)

@bot.command(name="collect")
async def collect_income(ctx: Context):
    user = database.get_user(ctx.author._user)
    now = round(time.time() * 1000)
    income_delay = income_delay_in_seconds * 1000

    if now - user.last_collected_income >= income_delay:
        amount = int(random.randrange(10, 50))
        user = database.add_to_user_balance(
            user,
            amount,
            direct_to_bank=False,
            last_collected_income=now
        )

        embed = discord.Embed(title="blahaj",  color=embed_color)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"You collected {amount}. Your balance is now {user.bank + user.cash}"
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="blahaj",  color=embed_color)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"You can collect income again <t:{round((user.last_collected_income + income_delay) / 1000)}:R>."
        await ctx.send(embed=embed)

bot.run(bot_token)