from telegram import BotCommand
from telegram.ext import ApplicationBuilder
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def set_bot_commands():
    app = ApplicationBuilder().token(TOKEN).build()
    commands = [
        BotCommand(command="start", description="Start interacting with the bot"),
        BotCommand(command="help", description="Get help information"),
        # Add more commands as needed
    ]
    await app.bot.set_my_commands(commands)
    print("Bot commands have been set.")