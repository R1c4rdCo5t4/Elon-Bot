import discord
from discord import app_commands

class async_client(discord.Client):
    guild_id = 1
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True

        print(f"{self.user} has been logged in.")

client = async_client()
tree = app_commands.CommandTree(client)

@tree.command(name="bye", description="say goodbye")
async def self(interaction: discord.Interaction, name:str):
    await interaction.response.send_message(f"Goodbye {name}!")

client.run("ODIwMzcyNzcxOTkyNjMzNDI0.Gim905.bJnyO8rzGvgiAHgkZRuofalyFdHiZFx_6tlnBA")