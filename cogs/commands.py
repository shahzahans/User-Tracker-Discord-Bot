# Import required Discord libraries and our MongoDB connection
import discord
from discord.ext import commands  # Used for command handling and creating cogs
from discord import app_commands  # Used specifically for slash commands
from utils.db import users_collection  # Importing the MongoDB users collection
from datetime import datetime  # For handling time/date, used in /joined command

# Define a cog (command group) called SlashCommands
class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store reference to the bot instance

    # /stats command — Shows tracking stats for a user or the command invoker
    @app_commands.command(name="stats", description="Show user tracking stats")
    @app_commands.describe(user="The user to check (leave blank for yourself)")
    async def stats(self, interaction: discord.Interaction, user: discord.Member = None):
        member = user or interaction.user  # Use provided user or default to the command invoker
        user_data = users_collection.find_one({"user_id": str(member.id)})  # Query user data from MongoDB

        if user_data:  # If the user is found in the database
            embed = discord.Embed(
                title=f"Here is your Stats, Senpai: {member.display_name}",
                color=discord.Color.blue()
            )
            # Add stats as fields in the embed
            embed.add_field(name="Messages", value=user_data['messages'], inline=True)
            embed.add_field(name="XP", value=user_data['xp'], inline=True)
            embed.add_field(name="Level", value=user_data['level'], inline=True)
            embed.add_field(name="Reactions Given", value=user_data['reactions_given'], inline=True)
            embed.add_field(name="Reactions Received", value=user_data['reactions_received'], inline=True)

            await interaction.response.send_message(embed=embed)  # Send the stats embed
        else:
            # If the user is not found in the database
            await interaction.response.send_message(
                f"So unfortunate... this user isn't tracked in the system, Senpai: {member.display_name}."
            )

    # /leaderboard command — Displays top 5 users based on XP
    @app_commands.command(name="leaderboard", description="Top Goats by XP")
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer response in case Mongo takes time

        try:
            top_users = users_collection.find().sort("xp", -1).limit(5)  # Fetch top 5 XP users from MongoDB

            embed = discord.Embed(
                title="🏆 XP Leaderboard",
                color=discord.Color.gold()
            )

            # Loop through users and add to embed
            for i, user in enumerate(top_users, start=1):
                member = interaction.guild.get_member(int(user["user_id"]))  # Get actual member object
                name = member.display_name if member else f"User ID {user['user_id']}"  # Fallback name
                embed.add_field(
                    name=f"{i}. {name}",
                    value=f"Level: {user['level']} | XP: {user['xp']}",
                    inline=False
                )

            await interaction.followup.send(embed=embed)  # Send leaderboard
        except Exception as e:
            print("❌ Error in /leaderboard:", e)  # Log error in terminal
            await interaction.followup.send("Something went wrong showing the leaderboard.")  # Notify user

    # /joined command — Shows how long a member has been in the server
    @app_commands.command(name="joined", description="Check how long a user has been in the server")
    @app_commands.describe(user="The member to check (leave blank for yourself)")
    async def joined(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer()  # Defer in case it takes long

        try:
            member = user or interaction.user  # Use provided user or fallback to author
            joined = member.joined_at  # Get the time the user joined

            if joined is None:  # If for some reason the date is missing
                await interaction.followup.send("❌ Couldn't determine when Senpai joined.")
                return

            now = datetime.now(tz=joined.tzinfo)  # Get current time in the same timezone as joined_at
            days = (now - joined).days  # Calculate number of days they've been in the server

            # Respond based on number of days
            if days >= 365:
                years = days // 365
                await interaction.followup.send(
                    f"📅 **{member.display_name}** joined the Gang **{years} year{'s' if years > 1 else ''} ago** on `{joined.strftime('%Y-%m-%d')}`"
                )
            else:
                await interaction.followup.send(
                    f"📅 **{member.display_name}** joined the Gang **{days} days ago** on `{joined.strftime('%Y-%m-%d')}`"
                )
        except Exception as e:
            print("❌ Error in /joined:", e)  # Log the error
            await interaction.followup.send("Something went wrong checking join time.")  # Tell the user

    # /help command — Shows list of available slash commands
    @app_commands.command(name="help", description="Show all available commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛠️ User-Tracker Commands",
            description="Here's a list of commands you can use:",
            color=discord.Color.green()
        )
        # Add descriptions for each command
        embed.add_field(name="/stats [user]", value="View your or someone else's tracking stats", inline=False)
        embed.add_field(name="/leaderboard", value="See the top 5 users by XP", inline=False)
        embed.add_field(name="/joined [user]", value="See how long a user has been in the server", inline=False)
        embed.add_field(name="!stats", value="(Legacy) Use this if slash commands aren't working", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)  # Only visible to the user


# Required setup function to register the cog
async def setup(bot):
    await bot.add_cog(SlashCommands(bot))





        
    