
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (CommandHandler,
                          ConversationHandler,
                          MessageHandler,
                          filters,
                          ContextTypes)
from django.utils.translation import gettext as _

from bot.handlers.utils import *
from bot.services import get_or_create_user_profile

# The states in the conversation
BANK_INFO, CONFIRM_BANK_INFO, LOAN_AMOUNT, CONFIRM_AMOUNT, REPAYMENT_MONTHS = range(2)


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
        to_return =  LOAN_AMOUNT
    elif user_response == _('Change'):
        await message.reply_text(
            _('Please provide the correct info:'),
            reply_markup=ReplyKeyboardRemove()
        )
        to_return = BANK_INFO

    else:
        await message.reply_text(
            _('Please choose an option.')
        )
        to_return = CONFIRM_BANK_INFO
    
    await deactivate_user_language()    
    return to_return


async def received_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await get_message(update)
    user_input = message.text

    amount = await parse_amount(user_input)
    if amount is not None:
        user_data = await get_user_data(context)
        user_data['amount'] = amount
        
        reply_keyboard = [[_('Confirm'), _('Change')]]
        await message.reply_text(_('''You entered:
                                {loan_amount}
                                Please confirm or change your input.
                                ''').format(loan_amount=user_data['amount']),
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return CONFIRM_AMOUNT
    else:
        await message.reply_text(
            _('Invalid amount. Please enter a numeric value for the amount you want to borrow.')
        )
        return LOAN_AMOUNT


async def confirm_loan_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update)
    await activate_user_language(user)

    message = await get_message(update)
    user_response = message.text

    if user_response == _('Confirm'):
        await message.reply_text(
            _('Thank you! How many months will it take you to repay the loan?')
        )
        to_return = REPAYMENT_MONTHS
    elif user_response == _('Change'):
        await message.reply_text(
            _('Please provide the correct amount:'),
            reply_markup=ReplyKeyboardRemove()
        )
        to_return = LOAN_AMOUNT
    else:
        await message.reply_text(
            _('Please choose an option.')
        )
        to_return = CONFIRM_AMOUNT
    
    await deactivate_user_language()    
    return to_return



borrower_flow_handler = ConversationHandler(

    entry_points=[CommandHandler(_('start'), start_borrower_flow)],
    
    states={
        BANK_INFO: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_bank_info)
        ],
        CONFIRM_BANK_INFO: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_bank_info)
        ],
        LOAN_AMOUNT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_amount)
        ],
        CONFIRM_AMOUNT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_loan_amount)
        ],
        REPAYMENT_MONTHS: [
            
        ],
    },

    fallbacks=[],
    per_user=True,
    per_chat=True,
    allow_reentry=True
)