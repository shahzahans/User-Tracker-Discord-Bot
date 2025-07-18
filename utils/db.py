# Import MongoDB driver
from pymongo import MongoClient

# Import libraries to handle environment variables
import os
from dotenv import load_dotenv

# 🌱 Load variables from .env file into the environment
load_dotenv()

# 🔐 Get MongoDB connection string securely from environment variable
MONGO_URI = os.getenv("MONGO_URI")

# 🔌 Connect to MongoDB using the connection string
client = MongoClient(MONGO_URI)

# 📂 Access (or create) the database named "discord-bot"
db = client["discord-bot"]

# 📁 Define collections (like tables)
users_collection = db["users"]       # Stores user data: messages, XP, level, etc.
commands_collection = db["commands"] # (Optional) Could track command usage
logs_collection = db["logs"]         # Stores join/leave logs

# 🛠️ Helper function to get a user or create one if they don't exist
def get_or_create_user(user_id):
    # 🔍 Try to find the user in the database
    user = users_collection.find_one({"user_id": str(user_id)})

    # ❌ If not found, create a new user entry with default stats
    if user is None:
        new_user = {
            "user_id": str(user_id),        # User's Discord ID (as string)
            "messages": 0,                  # How many messages they've sent
            "voice_time": 0,                # Placeholder for voice tracking (optional)
            "xp": 0,                        # Experience points
            "level": 1,                     # User starts at level 1
            "reactions_given": 0,           # Total emoji reactions given
            "reactions_received": 0         # Total emoji reactions received
        }

        # 💾 Save the new user into the database
        users_collection.insert_one(new_user)
        return new_user

    # ✅ If found, return the user document
    return user
