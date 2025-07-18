# Import discord.py's command extension
from discord.ext import commands 

# Import our helper to get or create user in DB and the users collection itself
from utils.db import get_or_create_user, users_collection

# 📦 Tracker Cog — This tracks message activity and awards XP & level-ups
class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store bot instance

    # 🔔 Event listener that triggers whenever a message is sent
    @commands.Cog.listener()
    async def on_message(self, message):
        # 🚫 Ignore messages from bots (we don't want them gaining XP!)
        if message.author.bot:
            return

        # Get the user's ID and ensure they exist in MongoDB
        user_id = str(message.author.id)
        user = get_or_create_user(user_id)

        # 🎮 XP system logic
        xp_gain = 10  # XP earned per message
        new_xp = user["xp"] + xp_gain  # Add earned XP to current total
        new_level = user["level"]  # Get current level
        required_xp = 100 * user["level"]  # XP needed to level up increases with level

        # 🚀 Level up logic
        if new_xp >= required_xp:
            new_level += 1  # Increase level
            new_xp -= required_xp  # Carry over extra XP
            await message.channel.send(
                f"🚀 **{message.author.display_name}** Tribal Chief Shad has promoted you to **Level {new_level}!**"
            )

        # 📝 Update the user's stats in the MongoDB database
        users_collection.update_one(
            {"user_id": user_id},  # Filter by user ID
            {
                "$set": {
                    "xp": new_xp,       # Set new XP
                    "level": new_level  # Set new level
                },
                "$inc": {
                    "messages": 1       # Increment total messages sent
                }
            }
        )

# 🔧 Setup function required to register this cog with your bot
async def setup(bot):
    await bot.add_cog(Tracker(bot))  # Attach Tracker cog to the bot



