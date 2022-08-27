import telegram
import telegram.ext
from dotenv import load_dotenv
import os

from telegram import *

from constants import OUT_MESSAGES
from sheets import get_scenario_status, get_team_scenarios
from utils import is_team_name, getGreetingText

load_dotenv()

token = os.environ.get('TOKEN')


def start(update, context):
    user = update.message.chat.first_name
    update.message.reply_text(f"{OUT_MESSAGES['greeting']}, {user}")
    # context.bot.send_message(chat_id=update.effective_chat.id, text=OUT_MESSAGES['greeting'])


def greet(update, context):
    update.message.reply_text(getGreetingText(update.message.chat.first_name))


def handle_query(update, context):
    text = update.message.text

    if is_team_name(text):
        context.bot.send_message(chat_id=update.effective_chat.id, text=get_team_scenarios(text), parse_mode='Markdown')

    else:
        button1 = InlineKeyboardButton(text='Повысить приоритет', callback_data='button1 pressed')
        button2 = InlineKeyboardButton(text='Понизить приоритет', callback_data='button2 pressed')
        button3 = InlineKeyboardButton(text='Предложить срок', callback_data='button3 pressed')
        keyboard_inline = InlineKeyboardMarkup([[button1, button2], [button3]])
        update.message.reply_text(get_scenario_status(text), parse_mode='Html', reply_markup=keyboard_inline)
        # context.bot.send_message(chat_id=update.effective_chat.id, text=get_scenario_status(text), parse_mode='Markdown', reply_markup=keyboard_inline)
        # update.message.reply_text(get_scenario_status(text), parse_mode='Markdown')


def callback1(update, context):
    user = update.callback_query.from_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Pressed button1, {user}')


def handle_button_click(update, context):
    query = update.callback_query
    query.answer()
    choice = query.data
    if choice == 'button1 pressed':
        callback1(update, context)

    if choice == 'button2 pressed':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Pressed button2')

    if choice == 'button3 pressed':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Pressed button3')


updater = telegram.ext.Updater(token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_query))
dispatcher.add_handler(telegram.ext.CallbackQueryHandler(handle_button_click))

updater.start_polling()
updater.idle()
