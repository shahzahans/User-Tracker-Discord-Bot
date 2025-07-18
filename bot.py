# 🧠 Core imports
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 🔐 Load your .env file containing secrets like the bot token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Fetch the bot token from .env

# ⚙️ Set up Discord gateway "intents" to specify which events your bot listens to
intents = discord.Intents.default()      # Start with default permissions
intents.message_content = True           # Allow reading message text (required for message tracking)
intents.members = True                   # Needed to track join/leave events
intents.guilds = True                    # Needed for slash commands and server info
intents.reactions = True                 # Required for tracking emoji usage
intents.voice_states = True              # Optional: for future voice tracking

# 🤖 Initialize your bot with "!" as the prefix for legacy commands (e.g., !stats)
bot = commands.Bot(command_prefix="!", intents=intents)

# 🔔 When the bot is ready and connected
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")  # Print confirmation when bot is live
    try:
        synced = await bot.tree.sync()  # Sync slash commands with Discord's API
        print(f"🔁 Synced {len(synced)} slash commands.")  # Show how many were synced
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")  # Catch and log any sync errors

# 🧩 Load all cog extensions (your bot's feature modules)
async def load_extensions():
    extensions = [
        "cogs.tracker",       # Tracker for messages and XP
        "cogs.logs",          # Tracks join and leave logs
        "cogs.reactions",     # Tracks emoji reactions given/received
        "cogs.commands"       # Slash command interface (/stats, /joined, etc.)
    ]

    for ext in extensions:
        try:
            await bot.load_extension(ext)  # Load each cog dynamically
            print(f"✅ Loaded: {ext}")      # Log success
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")  # Log failure

# 🚀 Run the bot (entry point)
async def main():
    async with bot:                  # Proper context management
        await load_extensions()      # Load all cogs
        await bot.start(TOKEN)       # Start the bot with your token

# 🧵 Run the async bot inside an event loop
import asyncio
asyncio.run(main())

