from typing import Optional
from ..database import Database
import nextcord
from ..constants import *

"""

@bot.command(name="createitem")
async def create_user_item(ctx: Context, item_name: str, item_price: int, *, item_description = "no description set"):
    user = database.get_user(ctx.author._user)
    item = database.create_user_item(
        name=item_name,
        description=item_description,
        price=item_price,
        user=user
    )

    embed = nextcord.Embed(color=embed_green)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embed.description = f"{check_emoji} Created item!"
    embed.add_field(name="Name:", value=item.name)
    embed.add_field(name="Description:", value=item.description)
    embed.add_field(name="Price:", value=f"{currency_symbol} {item.price}")
    embed.add_field(name="Creator:", value=f"<@{item.creator_user.id}>")
    await ctx.send(embed=embed)
"""


class CreateItemModal(nextcord.ui.Modal):
    item_name = nextcord.ui.TextInput(
        label="Item Name",
        placeholder="The name of your item.",
        required=True
    )

    item_price = nextcord.ui.TextInput(
        label="Item Price",
        style=nextcord.TextInputStyle.short,
        placeholder="300",
        required=True
    )

    item_desc = nextcord.ui.TextInput(
        label="Item Description",
        style=nextcord.TextInputStyle.paragraph,
        placeholder="Your item's description here.",
        required=True,
        max_length=300,
    )

    def __init__(self, database: Database) -> None:
        super().__init__(title="Create Item")
        self.database = database

    async def on_submit(self, interaction: nextcord.Interaction):
        user = self.database.get_user(interaction.user)
        store = user.store
        item = self.database.create_item_for_store(
            store=store,
            name=self.item_name,
            description=self.item_desc,
            price=int(self.item_price)
        )

        embed = nextcord.Embed(color=embed_green)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.description = f"{check_emoji} Created item!"
        embed.add_field(name="Name:", value=item.name)
        embed.add_field(name="Description:", value=item.description)
        embed.add_field(name="Price:", value=f"{currency_symbol} {item.price}")
        embed.add_field(name="Creator:", value=f"<@{item.creator_user.id}>")
        await interaction.response.send_message(embed=embed)

    async def on_error(self, interaction: nextcord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)