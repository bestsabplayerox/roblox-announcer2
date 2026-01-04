import discord
from discord.ext import commands
from flask import Flask, jsonify
from threading import Thread
import os
import time

# // SECURITY CONFIGURATION //
# Render will provide the sensitive token hidden in the background.
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

# Setup the simple web server (Flask)
app = Flask(__name__)

# This variable stores the latest announcement in memory.
# When the bot restarts, this resets to "No active announcements".
current_announcement = {
    "id": "0",
    "title": "System",
    "msg": "No active announcements."
}

# // 1. DISCORD BOT SECTION //
intents = discord.Intents.default()
intents.message_content = True # Needed to read what you type
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot is online: {bot.user}')

@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, title: str, *, message: str):
    global current_announcement
    
    # We use the current time as an ID. 
    # Roblox compares this ID to the last one it saw. 
    # If they are different, it shows the announcement.
    current_announcement = {
        "id": str(time.time()),
        "title": title,
        "msg": message
    }
    
    # Confirm to the Discord user that it worked
    await ctx.send(f"🚀 **Announcement Updated!**\n**Title:** {title}\n**Message:** {message}")

# // 2. WEB SERVER SECTION //
@app.route('/')
def home():
    return "I am alive! Use /get-announcement to see data."

@app.route('/get-announcement')
def get_data():
    # This is the link Roblox will visit to get the message
    return jsonify(current_announcement)

# // 3. STARTUP LOGIC //
def run_web():
    # Render assigns a specific PORT (address) we must use.
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    # Run the web server in the background (Thread)
    t = Thread(target=run_web)
    t.start()
    
    # Run the Discord bot
    run_bot()
