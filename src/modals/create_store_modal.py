from typing import Optional
from ..database import Database
import nextcord
from nextcord.utils import MISSING

class CreateStoreModal(nextcord.ui.Modal):
    name = nextcord.ui.TextInput(
        label="Store Name",
        placeholder="The name of your store.",
    )

    store_desc = nextcord.ui.TextInput(
        label="Store description",
        style=nextcord.TextInputStyle.paragraph,
        placeholder="Your store's description.",
        required=True,
        max_length=300,
    )

    def __init__(self, database: Database) -> None:
        super().__init__(title="Create Store")
        self.database = database

    async def on_submit(self, interaction: nextcord.Interaction):
        user = self.database.get_user(interaction.user)
        store = self.database.create_store(
            user=user,
            store_name=self.name,
            store_description=self.store_desc
        )

        await interaction.response.send_message(f"Your store with name {self.name} has been created! :)")

    async def on_error(self, interaction: nextcord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)