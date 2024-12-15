import os
from telegram import Update, User, ReplyKeyboardMarkup
from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          ConversationHandler,
                          MessageHandler,
                          filters,
                          ContextTypes)

from dotenv import load_dotenv
from bot.services import get_or_create_user_profile
from django.utils.translation import gettext as _
from django.utils import translation
import abroo_project.settings as settings

BORROWER_FLOW_BANK_INFO, BORROWER_FLOW_CONFIRM_BANK_INFO = range(2)

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

    # ask the user for their bank info
    greeting += _('''
    Please give your bank info,
    so others can use it to send you money.
''')

    await update.message.reply_text(greeting)
    translation.deactivate()
    return BORROWER_FLOW_BANK_INFO

async def received_bank_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await activate_user_language(user)

    bank_info = update.message.text
    context.user_data['bank_info'] = bank_info

    reply_keyboard = [[_('Confirm'), _('Change')]]
    await update.message.reply_text(_('''You entered:
                                {bank_info}
                                Please confirm or change your input.
                                ''').format(bank_info=context.user_data['bank_info']),
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    translation.deactivate()
    return BORROWER_FLOW_CONFIRM_BANK_INFO

async def confirm_bank_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await activate_user_language(user)

    user_response = update.message.text

    if user_response == _('Confirm'):
        await update.message.reply_text(
            _('Thank you! How much money do you want to borrow?')
        )

    
    translation.deactivate()    
    # return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await activate_user_language(user)
    await update.message.reply_text("I am here to help you.")
    translation.deactivate()


borrower_flow_handler = ConversationHandler(
    entry_points=[CommandHandler(_('start'), start)],
    states={
        BORROWER_FLOW_BANK_INFO: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_bank_info)
        ],
        BORROWER_FLOW_CONFIRM_BANK_INFO: [
            MessageHandler(filters.TEXT, confirm_bank_info)
        ]
    },
    fallbacks=[],
    per_user=True,:
    per_chat=True,
    allow_reentry=True
)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # app.add_handler(CommandHandler('start', start))
    app.add_handler(borrower_flow_handler)

    app.add_handler(CommandHandler('help', help_command))

    app.run_polling()