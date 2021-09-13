import requests, bs4, time, telebot
from Processors.user_recognition import user_recognition


# этот модуль сам отправляет сообщения, так что ему нужен доступ к Боту
bot = telebot.TeleBot('1879041775:AAG14Vz9P4AP4hjOGOOwYKbbFJGFSrWQEgs')


def covid(message):
    '''Парсит сайт, чтобы достать оттуда информацию о ковиде'''

    # name нужен, чтобы сделать ответ персонализированным
    name = user_recognition(message.from_user.id)

    # bs4 добывает нужные данные и кладет в две переменные
    html = requests.get('https://xn--80aesfpebagmfblc0a.xn--p1ai/')
    soup = bs4.BeautifulSoup(html.text, "html.parser")
    class_all = soup.find_all(class_='cv-countdown__item-value _accent')
    cases_today = class_all[1].getText()
    cases_all = class_all[0].getText()

    # готовим и отправляет текст
    send_mess = f'Всего случаев заражения в России: {cases_all}\n' \
                f'Случаи заражения за сегодня: {cases_today}\n' \
                f'Данный предосталенны сайтом стопкоронавирус.рф'

    # сначала отдает пользователю сообщение, записываем это в переменную, затем меняем сообщение
    msq = bot.send_message(message.chat.id, 'Получаю статистику...')
    time.sleep(0.5)  # после каждой замены немного ждем
    bot.edit_message_text("Получаю статистику....", chat_id=message.chat.id, message_id=msq.message_id)
    time.sleep(0.5)
    bot.edit_message_text("Получаю статистику.....", chat_id=message.chat.id, message_id=msq.message_id)
    time.sleep(0.5)
    bot.edit_message_text("Получаю статистику......", chat_id=message.chat.id, message_id=msq.message_id)
    time.sleep(0.5)
    bot.edit_message_text("Получаю статистику.......", chat_id=message.chat.id, message_id=msq.message_id)
    time.sleep(0.5)
    bot.edit_message_text("Получаю статистику.........", chat_id=message.chat.id, message_id=msq.message_id)
    time.sleep(0.5)
    bot.edit_message_text("Получаю статистику..........", chat_id=message.chat.id, message_id=msq.message_id)

    # когда наигрались, отправляем пользователю полученную выше статистику по Ковид
    bot.send_message(message.chat.id, send_mess)

    # немного ждем и отправляем еще сообщение (персонализированное)
    time.sleep(3)
    send_mess = f'Надеюсь, {name}, у тебя есть привика'
    bot.send_message(message.chat.id, send_mess)