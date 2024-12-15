import os
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv

from .handlers.commands import help_command
from .handlers.conversations.borrower_flow import borrower_flow_handler

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def main():
    if TOKEN is None:
        raise ValueError('the token is actually None!')
    app = ApplicationBuilder().token(TOKEN).build()

    # app.add_handler(CommandHandler('start', start))
    app.add_handler(borrower_flow_handler)

    app.add_handler(CommandHandler('help', help_command))

    app.run_polling()