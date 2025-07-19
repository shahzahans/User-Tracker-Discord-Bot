# User-Tracker Discord Bot

A smart Discord bot that tracks user activity — messages, XP, reactions, server join time, and more — using MongoDB. Built with 💜 using `discord.py`.

---

## Features

- Tracks messages, XP, levels
- Monitors voice time (coming soon)
- Logs member join/leave events
- Tracks reactions given/received
- Slash commands: `/stats`, `/joined`, `/leaderboard`, `/help`
- MongoDB backend for persistent data

---

## Installation

### 1. Clone the repo (by downloading the file or through terminal)
```bash
git clone https://github.com/your-username/user-tracker-bot.git
cd user-tracker-bot
```
### 2. Set up virtual environment (VS-Code Terminal)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your .env file
```bash
DISCORD_TOKEN=your_discord_bot_token
MONGO_URI=your_mongodb_connection_uri
```

### 5.Running the Bot
```bash
python bot.py
```

### 🛠 Future Development
This project is still a work in progress — I plan to continue adding more functionality over time! Features like voice activity tracking, custom rank cards, daily rewards, and admin dashboards may be introduced in future updates. Feel free to fork, contribute, or suggest features if you’d like to be part of the journey!

#### Built by Shadman Shahzahan

## License

This project is licensed under the MIT License - see the LICENSE file for details.




