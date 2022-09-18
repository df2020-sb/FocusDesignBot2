from dotenv import load_dotenv
from datetime import datetime
from telegram import *
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, CallbackQueryHandler, Filters, Updater
import os
import re

from constants import OUT_MESSAGES, ACTION_TYPES
from data import get_scenarios, send_update
from utils import get_greeting_text, make_scenario_info_string, is_team_name, get_user_ids

load_dotenv()
token = os.environ.get('TOKEN')
my_bot = Bot(token)
users = get_user_ids()


def start(update, context):
    reply_markup = ReplyKeyboardRemove()
    user_id = update.effective_chat.id
    if user_id in users:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_greeting_text(update.message.chat.first_name),
                                 parse_mode='Markdown',
                                 reply_markup=reply_markup)

        send_and_pin_statuses(update, context)

    else:
        update.message.reply_text(OUT_MESSAGES['unregistered_user'])


def statuslegend(update, context):
    user_id = update.effective_chat.id
    if user_id in users:
        send_and_pin_statuses(update, context)
    else:
        update.message.reply_text(OUT_MESSAGES['unregistered_user'])


def help(update, context):
    user_id = update.effective_chat.id
    if user_id in users:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=OUT_MESSAGES['help'],
                                 parse_mode='Markdown')

    else:
        update.message.reply_text(OUT_MESSAGES['unregistered_user'])


def send_and_pin_statuses(update, context):
    statuses_msg = context.bot.send_message(chat_id=update.effective_chat.id,
                                            text=OUT_MESSAGES['statuses'],
                                            parse_mode='Markdown')

    my_bot.unpinAllChatMessages(chat_id=update.effective_chat.id)
    my_bot.pinChatMessage(chat_id=update.effective_chat.id, message_id=statuses_msg.message_id)


def handle_query(update, context):
    user_id = update.effective_chat.id
    if user_id not in users:
        update.message.reply_text(OUT_MESSAGES['unregistered_user'])
    else:
        text = update.message.text
        matching_scenarios = get_scenarios(text)
        reply = make_scenario_info_string(matching_scenarios)

        if not matching_scenarios and is_team_name(text.strip().lower()):
            update.message.reply_text(OUT_MESSAGES['no_scenarios_for_your_team'])

        elif not matching_scenarios:
            update.message.reply_text(OUT_MESSAGES['wrong_input'])

        elif len(matching_scenarios) == 1:
            scenario_name = matching_scenarios[0]['name']
            button1 = InlineKeyboardButton(text='Повысить приоритет', callback_data=f'up_priority, {scenario_name}')
            button2 = InlineKeyboardButton(text='Понизить приоритет', callback_data=f'down_priority, {scenario_name}')
            button3 = InlineKeyboardButton(text='Предложить срок', callback_data=f'suggest_deadline, {scenario_name}')
            keyboard_inline = InlineKeyboardMarkup([[button1, button2], [button3]])
            update.message.reply_text(reply, parse_mode='Markdown', reply_markup=keyboard_inline)

        else:
            update.message.reply_text(reply, parse_mode='Markdown')


def handle_priority_change(update, context):
    query = update.callback_query
    data = query.data.split(',')
    action_type = data[0]
    scenario_name = data[1].strip()
    user = update.callback_query.from_user.first_name
    query.answer()

    global payload
    payload['scenario_name'] = scenario_name
    payload['param_name'] = 'suggested_priority'
    payload['value'] = '🔺high' if action_type == ACTION_TYPES['up_priority'] else 'low'
    payload['meta'] = f"{user} {datetime.now().strftime('%d.%m %H:%M:%S')}"

    reply = f'Попробуем поднять приоритет у {scenario_name}. Если получится, сообщим' if action_type == ACTION_TYPES[
        'up_priority'] else f'С радостью понизим приоритет у {scenario_name}'

    send_update(payload)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)


def handle_deadline_change(update, context):
    query = update.callback_query
    data = query.data.split(',')
    scenario_name = data[1].strip()
    query.answer()

    global payload
    payload['scenario_name'] = scenario_name

    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Введи желаемую дату в формате дд.мм')
    return date_input


def handle_date_input(update, context):
    input_text = update.message.text
    is_correct_date = bool(re.match("(0[1-9]|[12][0-9]|3[01]).(0[1-9]|1[0-2])", input_text))
    input_date = datetime.strptime(input_text, '%d.%m').replace(year=datetime.today().year)

    if input_date < datetime.now():
        update.message.reply_text(f'Махнём в прошлое? Сосредоточься 😄')
        return date_input

    if is_correct_date:
        user = update.message.chat.first_name

        global payload
        payload['param_name'] = 'suggested_deadline'
        payload['value'] = input_text
        payload['meta'] = f"{user} {datetime.now().strftime('%d.%m %H:%M:%S')}"
        send_update(payload)
        update.message.reply_text(
            f'Попробуем изменить срок у {payload["scenario_name"]} на {input_text}. Cообщим, если получится')
        return ConversationHandler.END

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Некорректная дата')
        return date_input


def timeout(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Время вышло. Будь решительнее в следующий раз')
    return ConversationHandler.END


def end(update, _):
    update.message.reply_text('END')
    return ConversationHandler.END


payload = {
    'scenario_name': '',
    'param_name': '',
    'value': '',
    'meta': '',

}

date_input = ''

updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('statuslegend', statuslegend))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CallbackQueryHandler(handle_priority_change, pattern='up_priority'))
dispatcher.add_handler(CallbackQueryHandler(handle_priority_change, pattern='down_priority'))
dispatcher.add_handler(ConversationHandler(
    entry_points=[CallbackQueryHandler(handle_deadline_change)],
    states={
        date_input: [MessageHandler(Filters.text, handle_date_input)],
        ConversationHandler.TIMEOUT: [CallbackQueryHandler(timeout, pattern='suggest_deadline'),
                                      MessageHandler(Filters.text | Filters.command, timeout)],
    },

    fallbacks=[CommandHandler('end', end)],
    conversation_timeout=30
))
dispatcher.add_handler(MessageHandler(Filters.text, handle_query))
updater.start_polling()
updater.idle()
