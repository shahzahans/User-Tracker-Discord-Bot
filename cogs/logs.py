# Import the commands extension from discord.py
from discord.ext import commands

# Import the logs collection from your MongoDB utility file
from utils.db import logs_collection

# 👇 This Cog (a modular class) tracks users joining or leaving the server
class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance for use in this cog

    # ✅ Event listener that runs whenever a member joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Insert a document into MongoDB to log the "join" event
        logs_collection.insert_one({
            "type": "join",  # Type of event
            "user_id": str(member.id),  # Store user ID
            "username": str(member),  # Store username#discriminator
            "guild": str(member.guild),  # Store the server (guild) they joined
        })

    # ✅ Event listener that runs whenever a member leaves or is removed from the server
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Insert a document into MongoDB to log the "leave" event
        logs_collection.insert_one({
            "type": "leave",  # Type of event
            "user_id": str(member.id),  # Store user ID
            "username": str(member),  # Store username#discriminator
            "guild": str(member.guild),  # Store the server (guild) they left
        })

# 🔧 Required setup function to register this cog with your main bot
async def setup(bot):
    await bot.add_cog(Logs(bot))  # Register the Logs cog with the bot
