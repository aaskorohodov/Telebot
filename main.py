import telebot
from telebot import types


bot = telebot.TeleBot('1879041775:AAG14Vz9P4AP4hjOGOOwYKbbFJGFSrWQEgs')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_mess = 'Вот что умеет этот бот:'
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Погода')
    itembtn2 = types.KeyboardButton('Калькулятор')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, send_mess, reply_markup=markup)



@bot.message_handler(content_types=['text'])
def calc(message):
    if message.text == "посчитаем":
        bot.send_message(message.from_user.id, "Пиши")
        bot.register_next_step_handler(message, calc1)

def calc1(message):
    if message.text == 'все':
        bot.register_next_step_handler(message, weather)
    else:
        result = message.text
        result = eval(result)
        bot.send_message(message.from_user.id, result)
        bot.register_next_step_handler(message, calc1)


def weather(message):
    if "погода" in message.text.lower():
        send_mess = 'https://www.gismeteo.ru/weather-yekaterinburg-4517/now/'
        bot.send_message(message.chat.id, send_mess)
    elif "калькулятор" in message.text.lower():
        send_mess = 'Калькулятор'
        bot.send_message(message.chat.id, send_mess)










@bot.message_handler(content_types=['text'])
def weather(message):
    if "погода" in message.text.lower():
        send_mess = 'https://www.gismeteo.ru/weather-yekaterinburg-4517/now/'
        bot.send_message(message.chat.id, send_mess)
    elif "калькулятор" in message.text.lower():
        send_mess = 'Калькулятор'
        bot.send_message(message.chat.id, send_mess)




@bot.message_handler(content_types=['text'])
def yes(message):
    if 'да' in message.text.lower():
        send_mess = "Отлично! Я запишу вас на вечернюю пробежку. Сообщите, если вы передумаете."
        bot.send_message(message.chat.id, send_mess)
        extra(message)
    elif 'желаю' in message.text.lower():
        send_mess = "Отлично! Я запишу вас на вечернюю пробежку. Сообщите, если вы передумаете."
        bot.send_message(message.chat.id, send_mess)
        extra(message)
    else:
        send_mess = "Жаль. Я отменю запись на вечернюю пробежку. Если передумаете – сообщите."
        bot.send_message(message.chat.id, send_mess)
        extra(message)

def extra(message):
    send_mess = "Всего доброго!"
    bot.send_message(message.chat.id, send_mess)





bot.polling(none_stop=True)