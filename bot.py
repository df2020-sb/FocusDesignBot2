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

updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path=token,
                      webhook_url='https://focus-design-bot.herokuapp.com/' + token
                      )
# updater.idle()
