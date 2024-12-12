import os
from telegram import Update, User
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from bot.services import get_or_create_user_profile
from django.utils.translation import gettext as _
from django.utils import translation
import abroo_project.settings as settings

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def activate_user_language(user: User):
    user_language = user.language_code
    if user_language in dict(settings.LANGUAGES).keys():
        translation.activate(user_language)
    else:
        translation.activate(settings.LANGUAGE_CODE)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await activate_user_language(user)
    # Update or create the user profile
    user_profile, created = await get_or_create_user_profile(user)
    
    if created:
        greeting = _("Hello, {first_name}! Nice to meet you.").format(first_name=user.first_name)
    else:
        greeting = _("Welcome back, {first_name}!").format(first_name=user.first_name)

    await update.message.reply_text(greeting)
    translation.deactivate()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await activate_user_language(user)
    await update.message.reply_text("I am here to help you.")
    translation.deactivate()

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))

    app.run_polling()