import time
import telebot


bot = telebot.TeleBot('1879041775:AAG14Vz9P4AP4hjOGOOwYKbbFJGFSrWQEgs')


def weather_handler(call):
    if call.data == 'moskow':
        w = w_parcer('moscow')
        c = 'Москве'
        w_print(c, w, call)

    elif call.data == 'yekaterinburg':
        w = w_parcer('yekaterinburg')
        c = 'Екатеринбурге'
        w_print(c, w, call)


def w_print(c, w, call):
    bot.send_message(call.message.chat.id, "Получаем погоду...")
    time.sleep(3)
    bot.send_message(call.message.chat.id, f'Текущая температура в {c}: {w}')


def w_parcer(c):
    import requests, bs4
    s = requests.get('https://www.ventusky.com/ru/' + c)
    b = bs4.BeautifulSoup(s.text, "html.parser")
    t = b.select(".temperature")
    w = t[0].getText().replace(" ", "")
    return w