import telegram.ext
from dotenv import load_dotenv
import os
from db import get_scenario_status

load_dotenv()

token = os.environ.get('TOKEN')


def start(update, context):
    update.message.reply_text('Hello! Print /help to see commands')


def handle_scenario_query(update, context):
    update.message.reply_text(get_scenario_status(update.message.text))


updater = telegram.ext.Updater(token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_scenario_query))

updater.start_polling()
updater.idle()
