from discord.ext.commands.context import Context
from discord.ext import commands
import time, discord

class Command:
    def __init__(
            self,
            bot: commands.Bot
        ) -> None:
        self.bot = bot

        @self.bot.command()
        async def cmd_name(ctx: Context):
            await ctx.send("haha penis")
        pass