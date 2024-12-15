from telegram import User, Update, Message
from telegram.ext import ContextTypes
from django.utils import translation

import abroo_project.settings as settings

async def activate_user_language(user: User):
    user_language = user.language_code
    if user_language is None:
        raise ValueError('the user language was actually None!')
    if user_language in dict(settings.LANGUAGES).keys():
        translation.activate(user_language)
    else:
        translation.activate(settings.LANGUAGE_CODE)

async def deactivate_user_language():
    translation.deactivate()

async def get_user(update:Update) ->User:
    user = update.effective_user
    if user is None:
        raise ValueError('the user was actually None!')
    return user

async def get_message(update: Update) -> Message:
    message = update.message
    if message is None:
        raise ValueError('the message was actually None!')
    return message

async def get_user_data(context: ContextTypes.DEFAULT_TYPE):
    if context.user_data is None:
        raise ValueError('the user_data was actually None!')
    return context.user_data