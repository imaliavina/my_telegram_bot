import re
import telegram
import json
import requests as req
from telegram import Update, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler, CallbackQueryHandler
from datetime import datetime as dt
import requests

TOKEN = "5521870669:AAGEBlyBrJcy1Glx5L2O4qPabUchLR3E0ec"
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher


# обработка команды старт (создаем Inline клавиатуру)
def start_command(update: Update, _):
    button1 = InlineKeyboardButton('Уточнить время', callback_data='buttonA')
    button2 = InlineKeyboardButton('Посчитать сумму', callback_data='buttonB')
    button3 = InlineKeyboardButton('Узнать курс валют', callback_data='buttonC')

    markup = telegram.InlineKeyboardMarkup(inline_keyboard=[[button1], [button2], [button3]], resize_keyboard=True)

    update.message.reply_text('Добрый день! Чтобы начать работу, выберите одно из возможных действий',
                              reply_markup=markup)
    return callback


# обработка нажатия клавиш клавиатуры
def callback(update: Update, context: CallbackContext):
    query = update.callback_query
    variant = query.data
    if variant == 'buttonA':
        query.answer()
        query.edit_message_text(text=f'Время сейчас {dt.now().time()}')

    if variant == 'buttonB':
        query.answer()
        query.edit_message_text(text='Введите "Сумма: 2 числа через пробел"')

    if variant == 'buttonC':
        query.answer()
        query.edit_message_text(text='Введите "Валюта: кодировка"')


def curr_command(update: Update, context: CallbackContext):
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    print(data)
    msg = update.message.text
    print(msg)
    item = msg.split(': ')[1]
    value = data['Valute'][item]['Value']
    update.message.reply_text(f'Курс {item} сейчас: {value}')


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def sum_command(update: Update, context: CallbackContext):
    msg = update.message.text
    print(msg)
    items = msg.split() # /sum 123 534543
    x = int(items[1])
    y = int(items[2])
    update.message.reply_text(f'{x} + {y} = {x+y}')


# Хендлеры
start_command_handler = CommandHandler('start', start_command)
hello_handler = MessageHandler(Filters.regex('Привет'), hello)
sum_handler = MessageHandler(Filters.regex('Сумма: '), sum_command)
curr_handler = MessageHandler(Filters.regex('Валюта: '), curr_command)
callback_button_handler = CallbackQueryHandler(callback=callback, pattern=None, run_async=False)


# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(callback_button_handler)
dispatcher.add_handler(hello_handler)
dispatcher.add_handler(sum_handler)
dispatcher.add_handler(curr_handler)

# Начинаем поиск обновлений
updater.start_polling()
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()