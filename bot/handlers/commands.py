from telegram import Update
from telegram.ext import ContextTypes

from .utils import *



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)
    await activate_user_language(user)
    message = await get_message(update)
    await message.reply_text("I am here to help you.")
    await deactivate_user_language()