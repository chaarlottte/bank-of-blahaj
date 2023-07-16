from src.database import Database, BalanceLocation, NotEnoughBalance
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
currency_symbol: str = config.get("currency_symbol")
admins: list = config.get("admins")
income_delay_in_seconds: int = config.get("income_delay_in_seconds")
work_delay_in_seconds: int = config.get("work_delay_in_seconds")

load_dotenv()
bot_token: str = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

database = Database()

jobs = json.loads(open("jobs.json").read()).get("jobs")

# Variables
embed_color = 0x5bcefa
embed_green = 0x57f287
embed_red = 0xed4245

x_emoji = "<:x_:1129945309305393232>"
check_emoji = "<:check:1129945323888984215>"

database.create_item(
    name="BLAHAJ",
    description="OMG SHONK BLAHAJ I LOVE HIM SO MUCH I WOULD DIE FOR THIS FUCKING SHARK AAAAAAAAAAAAA",
    price=500
)

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
    embed = discord.Embed(color=embed_color)

    for f in bot.commands:
        embed.add_field(name=f.name, value=prefix + f.name, inline=False)

    await ctx.send(embed=embed)

@bot.command(name="bot")
async def bot_(ctx: Context):
    embed = discord.Embed(color=embed_color)
    embed.set_author(name=ctx.message.author)
    embed.add_field(name="Authors", value="chaarlottte/quickdaffy, refactoring/ren", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="balance", aliases=["bal"])
async def user_balance(ctx: Context, mentioned_user: discord.User = None):
    if mentioned_user != None:
        user = database.get_user(mentioned_user)
        disc_usr = mentioned_user
    else:
        user = database.get_user(ctx.author._user)
        disc_usr = ctx.author._user

    embed = discord.Embed(color=embed_color)
    embed.set_author(name=disc_usr.name, icon_url=disc_usr.avatar.url)
    embed.add_field(name="Cash:", value=f"{currency_symbol} {user.cash}")
    embed.add_field(name="Bank:", value=f"{currency_symbol} {user.bank}")
    embed.add_field(name="Total:", value=f"{currency_symbol} {user.cash + user.bank}")
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

        embed = discord.Embed(color=embed_green)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"{check_emoji} You collected {currency_symbol} {amount}. Your balance is now {currency_symbol} {user.bank + user.cash}"
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=embed_red)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"{x_emoji} You can collect income again <t:{round((user.last_collected_income + income_delay) / 1000)}:R>."
        await ctx.send(embed=embed)

@bot.command(name="work")
async def work(ctx: Context):
    user = database.get_user(ctx.author._user)
    job = jobs[user.job_id]
    next_job = jobs[(user.job_id + 1) if user.job_id < 6 else user.job_id]

    job_name = job.get("name")
    xp_to_progress = job.get("xp_to_progress")

    now = round(time.time() * 1000)
    work_delay = work_delay_in_seconds * 1000

    if now - user.last_worked >= work_delay:
        hours_worked = random.randrange(1, 16)
        amount = hours_worked * job.get("income")
        xp_amount = int(hours_worked)

        user = database.add_to_user_balance(
            user,
            amount,
            direct_to_bank=False,
            last_worked=now
        )

        user = database.add_user_xp(
            user,
            job_xp=xp_amount
        )

        embed = discord.Embed(color=embed_green)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        if next_job != job:
            max_emojis = 10
            progress_percent = user.job_xp / xp_to_progress
            num_emojis = int(progress_percent * max_emojis)
            num_spaces = max_emojis - num_emojis

            progress_bar = "[" + "<:flushed_square:1129954680278093935>" * num_emojis + "⬜" * num_spaces + "]"
            embed.add_field(
                name=f"XP until next promotion:",
                value=f"{user.job_xp} {progress_bar} {xp_to_progress}"
            )
        embed.description = f"{check_emoji} You worked as a {job_name} for {hours_worked} hours and earned {currency_symbol} {amount}."
        await ctx.send(embed=embed)

        if user.job_xp >= xp_to_progress:
            user.job_id += 1
            database.session.commit()

            job = jobs[user.job_id]
            job_name = job.get("name")
            wage = job.get("income")

            embed = discord.Embed(title="Congratulations! You've been promoted!", color=embed_green)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.description = f"{check_emoji} You're now a {job_name}, and you'll make {currency_symbol} {wage} an hour!"
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=embed_red)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"{x_emoji} You can work again <t:{round((user.last_worked + work_delay) / 1000)}:R>."
        await ctx.send(embed=embed)

@bot.command(name="deposit", aliases=["dep"])
async def deposit_money(ctx: Context, amount: str):
    user = database.get_user(ctx.author._user)

    to_deposit = 0
    match amount:
        case "all":
            to_deposit = user.cash
        case "half":
            to_deposit = int(user.cash / 2)
        case _:
            if amount.isnumeric():
                to_deposit = int(amount)
            else:
                if amount.startswith("-"):
                    embed = discord.Embed(color=embed_red)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    embed.description = f"{x_emoji} You can't deposit a negative number, silly!"
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(color=embed_red)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    embed.description = f"{x_emoji} You gotta provide a number to deposit!"
                    await ctx.send(embed=embed)
    try:
        database.transfer_balance(
            user=user,
            to=BalanceLocation.BANK,
            amount=to_deposit
        )
        embed = discord.Embed(color=embed_green)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"{check_emoji} Deposited {currency_symbol} {to_deposit} to your bank."
        await ctx.send(embed=embed)
    except NotEnoughBalance:
        embed = discord.Embed(color=embed_red)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"{x_emoji} You don't have enough cash to deposit that amount!"
        await ctx.send(embed=embed)

@bot.command(name="withdraw", aliases=["with"])
async def withdraw_money(ctx: Context, amount: str):
    user = database.get_user(ctx.author._user)

    to_withdraw = 0
    match amount:
        case "all":
            to_withdraw = user.bank
        case "half":
            to_withdraw = int(user.bank / 2)
        case _:
            if amount.isnumeric():
                to_withdraw = int(amount)
            else:
                if amount.startswith("-"):
                    embed = discord.Embed(color=embed_red)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    embed.description = f"{x_emoji} You can't withdraw a negative number, silly!"
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(color=embed_red)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    embed.description = f"{x_emoji} You gotta provide a number to withdraw!"
                    await ctx.send(embed=embed)
    try:
        database.transfer_balance(
            user=user,
            to=BalanceLocation.CASH,
            amount=to_withdraw
        )
        embed = discord.Embed(color=embed_green)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"{check_emoji} Withdrew {currency_symbol} {to_withdraw} from your bank."
        await ctx.send(embed=embed)
    except NotEnoughBalance:
        embed = discord.Embed(color=embed_red)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"{x_emoji} You don't have enough cash to withdraw that amount!"
        await ctx.send(embed=embed)

@bot.command(name="pay", aliases=["send"])
async def pay_user(ctx: Context, user: discord.User, amount: int, *, args = None):
    paying_user = database.get_user(ctx.author._user)
    to_pay = database.get_user(user)

    if amount <= 0:
        embed = discord.Embed(color=embed_red)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"{x_emoji} You must pay at least {currency_symbol} 0!"
        await ctx.send(embed=embed)
        return

    if paying_user.cash >= amount:
        database.add_to_user_balance(paying_user, amount * -1)
        database.add_to_user_balance(to_pay, amount)

        embed = discord.Embed(color=embed_green)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"{check_emoji} Paid {user.name} {currency_symbol} {amount}."
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=embed_red)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.description = f"{x_emoji} You don't have enough {currency_symbol} for that!"
        await ctx.send(embed=embed)

@bot.command(name="shop", aliases=["store"])
async def display_store(ctx: Context):
    items = database.get_all_items()
    embed = discord.Embed(title="blahaj store", color=embed_color)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

    for item in items:
        embed.add_field(
            name=f"{currency_symbol} {item.price} - {item.name}",
            value=f"{item.description}",
            inline=False
        )

    await ctx.send(embed=embed)

bot.run(bot_token)