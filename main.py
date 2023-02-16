import telebot
from telebot import types
import json
from mixins import Getallmixin, Createmixin, Updatemixin, Deletemixin

class Interface(Getallmixin, Createmixin, Updatemixin, Deletemixin):
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
inline_keyboard.add(inline_button1, inline_button2, inline_button3, inline_button4)

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, f'Hello!, {message.from_user.first_name}')
    bot.send_message(message.chat.id, 'Choose one from below: ', reply_markup=inline_keyboard)

def menu(message: types.Message):
    bot.send_message(message.chat.id, 'Choose one from below: ', reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == 'read_all')
def send_todo(callback: types.CallbackQuery):
    res = json.dumps(interface.get_all(HOST), indent=4, ensure_ascii=False)
    bot.send_message(callback.message.chat.id, res)
    menu(callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'create')
def create_new(callback: types.CallbackQuery):
    messages = bot.send_message(callback.message.chat.id, 'Write your ToDo')
    bot.register_next_step_handler(messages, create_title)

def create_title(message):
    response = message.text
    if len(response.split()) == 1:
        result = interface.create(HOST, response)
        if result == '1':
            bot.send_message(message.chat.id, 'Created! :)')
            menu(message)
        elif result == '0':
            bot.send_message(message.chat.id, 'Error!')
            menu(message)
    elif len(response.split()) > 1:
        input_from_customer = response.split()

        result = interface.create(HOST, input_from_customer[0], input_from_customer[1])
        if result == '1':
            bot.send_message(message.chat.id, 'Created! :)')
            menu(message)
        elif result == '0':
            bot.send_message(message.chat.id, 'Error!')
            menu(message)

@bot.callback_query_handler(func=lambda callback: callback.data == 'update')
def update(callback: types.CallbackQuery):
    message = bot.send_message(callback.message.chat.id, 'Type ID and Dont write if false')
    bot.register_next_step_handler(message, update_title)

def update_title(message):
    response = message.text.split()
    if len(response) == 2:
        result = interface.update(HOST, response[0], response[1])
        bot.send_message(message.chat.id, result)
        menu(message)
    elif len(response) > 2:
        result = interface.update(HOST, response[0], response[1], response[2])
        bot.send_message(message.chat.id, result)
        menu(message)

@bot.callback_query_handler(func=lambda callback: callback.data == 'delete')
def delete(callback: types.CallbackQuery):
    res = json.dumps(interface.get_all(HOST), indent=4, ensure_ascii=False)
    message = bot.send_message(callback.message.chat.id, f'{res}\n Write ID to delete')
    bot.register_next_step_handler(message, answer)

def answer(message):
    response = message.text
    result = interface.delete(HOST, response)
    bot.send_message(message.chat.id, result)
    menu(message)
        
bot.polling()