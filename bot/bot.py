import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from bot.services import get_or_create_user_profile

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # Update or create the user profile
    user_profile, created = await get_or_create_user_profile(user)
    
    if created:
        greeting = f"Hello, {user.first_name}! Nice to meet you."
    else:
        greeting = f"Welcome back, {user.first_name}!"

    await update.message.reply_text(greeting)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am here to help you.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))

    app.run_polling()