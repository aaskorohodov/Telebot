elif message.text == '/timer':
send_mess = 'Задайте число секунд, которые таймер будет работать'
log(message.text, message.from_user.username, send_mess)
bot.send_message(message.from_user.id, send_mess)


def timer(message):
    send_mess = 'Ready!'
    log(message.text, message.from_user.username, send_mess)
    tim = int(message.text)
    msq = bot.send_message(message.chat.id, send_mess)
    for i in range(tim + 1):
        def timer(message, i):
            time.sleep(1)
            bot.edit_message_text(i, chat_id=message.chat.id, message_id=msq.message_id)

        timer(message, i)
    send_mess = f'Таймер сработал! Прошло {tim} секунд'
    log(message.text, message.from_user.username, send_mess)
    bot.send_message(message.from_user.id, send_mess)


bot.register_next_step_handler(message, timer)