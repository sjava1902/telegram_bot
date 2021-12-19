import telebot
import time


import config
from telebot import types
import random
bot = telebot.TeleBot(config.token, parse_mode=None)
@bot.message_handler(commands = ["start"])
def send_welcome(message: types.Message):
    sti = open('msu.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.from_user.id, "Добро пожаловать, {0.first_name}! \n Я <b>{1.first_name}</b>, "
                                           "официальный бот МГУ".format(message.from_user, bot.get_me()),
                     parse_mode='html')

@bot.message_handler(commands = ["help"])
def send_help(message: types.Message):
    bot.send_message(message.from_user.id, "Я бот, есть команды start, time, random, info")

@bot.message_handler(commands = ["time"])
def send_time(message: types.Message):
    bot.send_message(message.from_user.id, time.ctime(message.date))

@bot.message_handler(commands = ["random"])
def send_random(message: types.Message):
    bot.send_message(message.from_user.id, '🎲Рандомное число: ' + str(random.randint(0, 100)))

@bot.message_handler(commands = ["info"])
def send_info(message: types.Message):
    markup_inline = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    button_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    markup_inline.add(button_yes, button_no)
    msg = bot.send_message( message.from_user.id, "Хотите узнать свой НИК и ID?",
                     reply_markup=markup_inline)



@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    # bot.edit_message_reply_markup(
    #     chat_id = call.message.chat.id,
    #     message_id=call.message.id,
    #     reply_markup=None
    # )
    bot.answer_callback_query(call.id, text='')  #удаляем часики с кнопок
    if call.data == 'yes':
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder = "Выберите..."
        )
        button_id = types.KeyboardButton("Мой ID")
        button_username = types.KeyboardButton("Мой НИК")

        markup.add(button_id, button_username, row_width=2)

        msg = bot.send_message(call.message.chat.id, text='Выберите кнопку', reply_markup=markup)
        # reply_markup = types.ReplyKeyboardRemove()
        # bot.delete_message(call.message.chat.id, msg.message_id)
       
        bot.register_next_step_handler(msg, user_answer)

    elif call.date == 'no':
        pass

def user_answer(message):

    if message.text == 'Мой ID':
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f'Ваш ID: {message.from_user.id}')
    elif message.text == 'Мой НИК':
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f'Ваше имя: {message.from_user.first_name} '
                                          f'{message.from_user.last_name} Вы ОТЧИСЛЕНЫ😢')
     # bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['text'])
def echo(message):
    bot.reply_to(message, message.text)


if __name__ == "__main__":
    bot.infinity_polling()