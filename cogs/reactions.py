# Import discord.py's command extension
from discord.ext import commands

# Import MongoDB helpers: get_or_create_user ensures the user exists in DB
from utils.db import get_or_create_user, users_collection

# 📦 Reactions Cog — This cog tracks when users give or receive emoji reactions
class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance for this cog

    # 🔔 Event listener for when a reaction is added to a message
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # 🚫 Ignore reactions added by other bots
        if user.bot:
            return

        # ✅ Make sure the reacting user exists in the database
        get_or_create_user(user.id)

        # ➕ Increase the number of reactions the user has given by 1
        users_collection.update_one(
            {"user_id": str(user.id)},  # Find the reacting user in DB
            {"$inc": {"reactions_given": 1}}  # Increment "reactions_given"
        )

        # ✅ Check if the message author exists and is not a bot
        if reaction.message.author and not reaction.message.author.bot:
            # Ensure the message author also exists in the DB
            get_or_create_user(reaction.message.author.id)

            # ➕ Increase the number of reactions the message author received
            users_collection.update_one(
                {"user_id": str(reaction.message.author.id)},  # Find message author
                {"$inc": {"reactions_received": 1}}  # Increment "reactions_received"
            )

# 🔧 Required setup function to register this cog with the bot
async def setup(bot):
    await bot.add_cog(Reactions(bot))  # Register the Reactions cog

