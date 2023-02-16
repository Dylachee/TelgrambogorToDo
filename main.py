import telebot
from telebot import types
import json
from mixins import Getallmixin, Getonemixin, Createmixin, Updatemixin, Deletemixin

class Interface(Getallmixin,Getonemixin, Createmixin, Updatemixin, Deletemixin):
    pass

interface = Interface()
token = '6134936077:AAFU73VCKd8DYS4pv-8kmtLtT1vk2AK5K-A'
bot = telebot.TeleBot(token)
HOST = 'http://3.67.196.232/'


inline_keyboard = types.InlineKeyboardMarkup()
inline_button1 = types.InlineKeyboardButton('View all ToDo', callback_data='read_all')
inline_button2 = types.InlineKeyboardButton('Create', callback_data='create')
inline_button3 = types.InlineKeyboardButton('Update', callback_data='update')
inline_button4 = types.InlineKeyboardButton('Delete', callback_data='delete')
inline_button5 = types.InlineKeyboardButton('View by ID', callback_data='read_one')
inline_keyboard.add(inline_button1, inline_button5, inline_button2, inline_button3, inline_button4)

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, f'Hello!, {message.from_user.first_name}')
    bot.send_message(message.chat.id, 'Choose one from below: ', reply_markup=inline_keyboard)

def start2(message: types.Message):
    bot.send_message(message.chat.id, 'Choose one from below: ', reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == 'read_all')
def read_and_send_todo(callback: types.CallbackQuery):
    res = json.dumps(interface.get_all_todo(HOST), indent=4, ensure_ascii=False)
    bot.send_message(callback.message.chat.id, res)
    start2(callback.message)

@bot.callback_query_handler(func=lambda callback: callback.data == 'read_one')
def read_one_todo(callback: types.CallbackQuery):
    msg = bot.send_message(callback.message.chat.id, 'Type ID')
    bot.register_next_step_handler(msg, read_one)
def read_one(message):
    response = message.text
    result = json.dumps(interface.retrieve_todo(HOST, response), indent=4, ensure_ascii=False)
    bot.send_message(message.chat.id, result)
    start2(message)

@bot.callback_query_handler(func=lambda callback: callback.data == 'create')
def create_new_todo(callback: types.CallbackQuery):
    messages = bot.send_message(callback.message.chat.id, 'Write only one, if is_done = False\nWrire one name and 1 use space if is_done = True')
    bot.register_next_step_handler(messages, create_title)

def create_title(message):
    response = message.text
    if len(response.split()) == 1:
        result = interface.create_todo(HOST, response)
        if result == '1':
            bot.send_message(message.chat.id, 'Created! :)')
            start2(message)
        elif result == '0':
            bot.send_message(message.chat.id, 'Error!')
            start2(message)
    elif len(response.split()) > 1:
        input_from_customer = response.split()

        result = interface.create_todo(HOST, input_from_customer[0], input_from_customer[1])
        if result == '1':
            bot.send_message(message.chat.id, 'Created! :)')
            start2(message)
        elif result == '0':
            bot.send_message(message.chat.id, 'Error!')
            start2(message)

@bot.callback_query_handler(func=lambda callback: callback.data == 'update')
def update_todo_bot(callback: types.CallbackQuery):
    message = bot.send_message(callback.message.chat.id, 'Type ID and Dont write if false')
    bot.register_next_step_handler(message, update_title)

def update_title(message):
    response = message.text.split()
    if len(response) == 2:
        result = interface.update_todo(HOST, response[0], response[1])
        bot.send_message(message.chat.id, result)
        start2(message)
    elif len(response) > 2:
        result = interface.update_todo(HOST, response[0], response[1], response[2])
        bot.send_message(message.chat.id, result)
        start2(message)

@bot.callback_query_handler(func=lambda callback: callback.data == 'delete')
def delete_todo_bot(callback: types.CallbackQuery):
    res = json.dumps(interface.get_all_todo(HOST), indent=4, ensure_ascii=False)
    message = bot.send_message(callback.message.chat.id, f'{res}\n Write ID to delete')
    bot.register_next_step_handler(message, answer)

def answer(message):
    response = message.text
    result = interface.delete_todo(HOST, response)
    bot.send_message(message.chat.id, result)
    start2(message)
        
bot.polling()