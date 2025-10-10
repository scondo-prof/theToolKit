import os

import discord
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready() -> None:
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: str) -> int:
    if message.author == client.user:
        return 0

    if message.content.startswith("/test"):
        await message.channel.send("WE ARE IN HELL")
        return 1


client.run(token=os.getenv("DISCORD_BOT_TOKEN"))
