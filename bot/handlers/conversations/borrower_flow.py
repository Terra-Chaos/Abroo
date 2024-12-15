
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (CommandHandler,
                          ConversationHandler,
                          MessageHandler,
                          filters,
                          ContextTypes)
from django.utils.translation import gettext as _

from bot.handlers.utils import *
from bot.services import get_or_create_user_profile

# The states in the conversation
BANK_INFO, CONFIRM_BANK_INFO = range(2)


async def start_borrower_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)
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
    
    message = await get_message(update)
    await message.reply_text(greeting)
    await deactivate_user_language()
    return BANK_INFO

async def received_bank_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)
    await activate_user_language(user)

    message = await get_message(update)
    bank_info = message.text
    user_data = await get_user_data(context)
    user_data['bank_info'] = bank_info

    reply_keyboard = [[_('Confirm'), _('Change')]]
    await message.reply_text(_('''You entered:
                                {bank_info}
                                Please confirm or change your input.
                                ''').format(bank_info=user_data['bank_info']),
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    await deactivate_user_language()
    return CONFIRM_BANK_INFO

async def confirm_bank_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)
    await activate_user_language(user)

    message = await get_message(update)
    user_response = message.text

    if user_response == _('Confirm'):
        await message.reply_text(
            _('Thank you! How much money do you want to borrow?')
        )

    
    await deactivate_user_language()    
    # return ConversationHandler.END




borrower_flow_handler = ConversationHandler(

    entry_points=[CommandHandler(_('start'), start_borrower_flow)],
    
    states={
        BANK_INFO: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_bank_info)
        ],
        CONFIRM_BANK_INFO: [
            MessageHandler(filters.TEXT, confirm_bank_info)
        ]
    },

    fallbacks=[],
    per_user=True,
    per_chat=True,
    allow_reentry=True
)