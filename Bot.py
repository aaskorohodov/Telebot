import random, time, telebot
from telebot import types
from PIL import Image
from Processors.log import log
from Processors.user_recognition import user_recognition


bot = telebot.TeleBot('1879041775:AAG14Vz9P4AP4hjOGOOwYKbbFJGFSrWQEgs')
stop = ['все', 'Все', 'ВСЕ', 'ВСе', 'всё', 'ВСё', 'ВСЁ', 'Всё', 'dct', 'Dct', 'DCt', 'DCT', 'dc`', 'Dc`', 'DC`', 'DC~']


@bot.message_handler(commands=['start'])
def send_welcome(message):
    from Processors.user_recognition import user_recognition
    name = user_recognition(message.from_user.id)

    if name == False:
        send_mess = 'Кажется, мы еще не знакомы! Как тебя зовут?'
        bot.send_message(message.from_user.id, send_mess)
        log(message.text, message.from_user.username, send_mess)

        def whats_ur_name(message):
            excl = ['меня', 'зовут', 'я', 'а', 'тебя', 'как', 'звать', 'name', 'my', 'зови', 'пускай', 'будет']
            name = ''
            for el in message.text.split():
                if el not in excl:
                    name += el
            from Processors.user_recognition import new_user
            new_user(message.from_user.id, name)
            bot.send_message(message.from_user.id, 'Отлично, теперь давай начнем сначала')
            log(message.text, message.from_user.username, send_mess)
            time.sleep(2)
            send_welcome(message)

        bot.register_next_step_handler(message, whats_ur_name)

    else:
        send_mess = f'Привет {name}! Вот что умеет этот бот:\n' \
                    f'\n' \
                    f'/start – включить бота/начать общение с начала\n' \
                    f'/math – разная матиматика\n' \
                    f'/stuff – всякие штуки\n' \
                    f'/name – изменить свое имя\n' \
                    f'/lists – личные списки\n'\
                    f'\n' \
                    f'А еще могу говорить.'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)


@bot.message_handler(commands=['stuff', 'reversed', 'popka', 'time', 'pics', 'weather', 'food', 'covid', 'anagramm',
                               'letters', 'timer', 'test', 'b_day', 'translate', 'ru_eng', 'eng_ru'])
def staff_handler(message):
    name = user_recognition(message.from_user.id)
    if message.text == '/stuff':
        send_mess = '/reversed – слова наоборот\n' \
                    '/popka – попугай\n' \
                    '/time – узнать время в любом городе\n' \
                    '/weather – узнать погоду\n' \
                    '/food – подскажет что поесть\n' \
                    '/pics – даст случайную картинку\n' \
                    '/covid – даст статистику по ковиду\n' \
                    '/anagramm – поиск анаграмм\n' \
                    '/letters – считает повторы букв\n' \
                    '/timer – таймер\n' \
                    '/b_day – время до дня рождения\n' \
                    '/translate – переводчик'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

    elif message.text == '/reversed':
        send_mess = 'Все что вы напишите, будет перевернуто.\n' \
                    'Для выхода пиши "все"'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

        def reversed(message):
            if message.text in stop:
                send_mess = 'reversed остановлен.\n' \
                            '/start для продолжения'
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.chat.id, send_mess)
            else:
                from Processors.stuff import reversed_words
                send_mess = reversed_words(message.text)
                bot.send_message(message.chat.id, send_mess)
                log(message.text, message.from_user.username, send_mess)
                bot.register_next_step_handler(message, reversed)

        bot.register_next_step_handler(message, reversed)

    elif message.text == '/popka':
        def popca_pross(message):
            if message.text in stop:
                send_mess = 'Popka завершен\n' \
                            '/start для продолжения'
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.from_user.id, send_mess)
            else:
                from Processors.stuff import popka_talking
                send_mess = popka_talking(message.text)
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.from_user.id, send_mess)
                bot.register_next_step_handler(message, popca_pross)

        send_mess = 'Пишите что хотите, когда надоест, напишите "все".'
        bot.send_message(message.chat.id, send_mess)
        log(message.text, message.from_user.username, send_mess)
        bot.register_next_step_handler(message, popca_pross)

    elif message.text == '/time':
        send_mess = 'Какой город смотрим?'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

        def time_get(message):
            from Processors.time import output
            send_mess = output(message.text)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.chat.id, send_mess)

        bot.register_next_step_handler(message, time_get)

    elif message.text == '/pics':
        t = [i for i in range(204)]
        ran = str(random.choice(t))
        name = fr'C:\Users\Аркадий\Pictures\py\1 ({ran}).JPG'
        png = Image.open(name)
        send_mess = 'Вот:'
        bot.send_message(message.chat.id, send_mess)
        log(message.text, message.from_user.username, send_mess)
        bot.send_photo(message.from_user.id, png)

    elif message.text == '/weather':
        send_mess = f'{name}, в каком городе ты живешь?'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

        def weather_pros(message):
            from Processors.weather_udvanced import wf_output
            send_mess = wf_output(message.text)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)

        bot.register_next_step_handler(message, weather_pros)

    elif message.text == '/food':
        markup = telebot.types.InlineKeyboardMarkup()

        self = types.InlineKeyboardButton(text='Готовим сами', callback_data="self")
        fast = types.InlineKeyboardButton(text='Готовое дома', callback_data="fast")
        outdoor = types.InlineKeyboardButton(text='Сходить в...', callback_data="outdoor")
        markup.add(self, fast, outdoor)

        send_mess = f'Что хочет {name}?'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess, reply_markup=markup)

    elif message.text == '/covid':
        log(message.text, message.from_user.username)
        from Processors.covid import covid
        covid(message)

    elif message.text == '/anagramm':
        send_mess = f'{name}, дай текст, а я найду в нем анаграммы.\n' \
                    '\n' \
                    '*поддерживается только английский и русский'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

        def anagramms_pross(message):
            from Processors.stuff import anagrams
            send_mess = anagrams(message.text)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)

        bot.register_next_step_handler(message, anagramms_pross)

    elif message.text == '/letters':
        send_mess = f'{name}, давай свой текст, а я посчитаю повторы букв'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

        def letters(message):
            from Processors.stuff import letters_counter
            send_mess = letters_counter(message.text)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)

        bot.register_next_step_handler(message, letters)

    elif message.text == '/timer':
        from Processors.timer import timer_step1
        name = user_recognition(message.from_user.id)
        timer_step1(message, name)

    elif message.text == '/b_day':
        send_mess = f'Тут можно узнать, когда у кого-то будет следующий день рождения.\n' \
                    f'\n' \
                    f'Введи дату рождения в формате [Год Месяц День] через пробелы'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

        def birthday(message):
            from Processors.stuff import age
            send_mess = age(message.text)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)

        bot.register_next_step_handler(message, birthday)

    elif message.text == '/translate':
        send_mess = '/ru_eng\n' \
                    '/eng_ru'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

    elif message.text == '/ru_eng':
        send_mess = 'Могу перевести слово или простую фразу. Пиши'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

        def ru_eng(message):
            from Processors.translation import ru_eng
            send_mess = ru_eng(message)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)
            time.sleep(2)
            send_mess = 'Еще?\n' \
                        '/ru_eng\n' \
                        '/eng_ru'
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)

        bot.register_next_step_handler(message, ru_eng)

    elif message.text == '/eng_ru':
        send_mess = 'Могу перевести слово или простую фразу. Пиши'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

        def eng_ru(message):
            from Processors.translation import eng_ru
            send_mess = eng_ru(message)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)
            time.sleep(2)
            send_mess = 'Еще?\n' \
                        '/ru_eng\n' \
                        '/eng_ru'
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)

        bot.register_next_step_handler(message, eng_ru)


@bot.message_handler(commands=['math', 'calc', 'area', 'bmi', 'fib'])
def math_handler(message):
    if message.text == '/math':
        send_mess = 'Это матиматический модуль. Вот что я умею:\n' \
                    '\n' \
                    '/calc – калькулятор\n' \
                    '/area – площадь прямоугольника\n' \
                    '/bmi – рассчет массы тела\n' \
                    '/fib - число фибоначи'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

    elif message.text == '/calc':
        send_mess = 'Это калькулятор. Вводите выражения "как обычно", а я попробую их посчитать.\n' \
                    'Например: "2*5", "5/5", "5+4" и так далее.\n' \
                    '\n' \
                    'Когда надоест, отправьте мне "все"'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

        def calc_pros(message):
            if message.text in stop:
                send_mess = 'Калькулятор закрыт.\n' \
                            '/start для продолжения'
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.from_user.id, send_mess)
            else:
                from Processors.calc import calc
                send_mess = calc(message.text)
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.from_user.id, send_mess)
                bot.register_next_step_handler(message, calc_pros)

        bot.register_next_step_handler(message, calc_pros)

    elif message.text == '/area':
        send_mess = 'Тут можно поссчитать площадь прямоугольника.\n' \
                    'Когда надоест, напиши "все"\n' \
                    '\n' \
                    'Введите две стороны'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

        def area_handler(message):
            if message.text in stop:
                send_mess = 'area остановлен.\n' \
                            '/start для продолжения'
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.chat.id, send_mess)
            else:
                from Processors.math import area
                send_mess = area(message.text)
                bot.send_message(message.chat.id, send_mess)
                log(message.text, message.from_user.username, send_mess)
                bot.register_next_step_handler(message, area_handler)

        bot.register_next_step_handler(message, area_handler)

    elif message.text == '/bmi':
        send_mess = 'Тут можно рассчитать индекс массы тела.'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)
        time.sleep(1.5)
        send_mess = 'Какой у тебя рост?'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

        def height(message):
            height = message.text
            send_mess = 'А какой вес?'
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.chat.id, send_mess)

            def weight(message):
                weight = message.text
                from Processors.math import bmi
                send_mess = bmi(height, weight)
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.chat.id, send_mess)

            bot.register_next_step_handler(message, weight)
        bot.register_next_step_handler(message, height)

    elif message.text == '/fib':
        send_mess = 'Напиши номер числа фибоначи, а я покажу это число\n' \
                    '\n' \
                    '!!! Обрати внимание, что телеграмм не даст отправить слишком большое письмо. ' \
                    'Числа по номеру свыше ~15000 могут не пройти'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

        def fib_call(message):
            from Processors.math import fib
            send_mess = fib(message)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.chat.id, send_mess)

        bot.register_next_step_handler(message, fib_call)


@bot.message_handler(commands=['lists'])
def list_handler(message):
    basket = ['Корзина', 'корзина', 'rjhpbyf', 'Rjhpbyf']
    restore_pls = ['Восстанови', 'восстанови', 'Востанови', 'востанови', 'восстановить', 'Восстановить', 'востановить', 'Востановить']
    del_pls = ['удали', 'Удали', 'удали:', 'Удали:', 'удалить', 'Удалить', 'удалить:', 'Удалить:', 'elfkb', 'elfkbnm', 'Elfkb', 'Elfkbnm']
    add_pls = ['добавь', 'Добавь', 'добавить', 'Добавить', 'добавь:', 'Добавь:', 'добавить:', 'Добавить:']
    random_pls = ['рандом', 'Рандом', 'hfyljv', 'Hfyljv']
    user_id = message.from_user.id

    from Processors.Lists.lists import your_lists
    send_mess = your_lists(user_id)  # возвращает готовое сообщение со списками, либо "у вас нет списков"
    bot.send_message(message.chat.id, send_mess)
    if send_mess == 'У вас нет списков, давайте сделаем их.':
        time.sleep(1)
        send_mess = 'Какое будет название списка?'
        bot.send_message(message.chat.id, send_mess)

        def first_list_creation(message):
            list_name = message.text
            send_mess = f'Отлично, список {list_name} почти готов. Чтобы наполнить его, пиши элементы, ' \
                        f'каждый с новой строки'
            bot.send_message(message.chat.id, send_mess)

            def first_list_elements(message):
                from Processors.Lists.lists import new_list, items_in_list
                send_mess = new_list(user_id, list_name, message)
                bot.send_message(message.chat.id, send_mess)
                time.sleep(1.5)
                list_handler(message)

            bot.register_next_step_handler(message, first_list_elements)
        bot.register_next_step_handler(message, first_list_creation)


    def what_to_do(message):
        if message.text.startswith('удали') or message.text.startswith('Удали'):
            '''Удаление списка'''
            from Processors.Lists.lists import delete_list
            send_mess = delete_list(user_id, message.text)  # перемещает список в корзину, готовит ответное сообщение
            bot.send_message(message.chat.id, send_mess)
            time.sleep(1.5)  # немного ждет, затем кидает список списков
            list_handler(message)

        elif message.text in basket:
            '''Показывает содержание корзины. Корзина основана на изменении user_id (к нему приписывается 55555 в конце,
             что и означает, что этот список в корзине)'''
            from Processors.Lists.lists import basket_lists
            send_mess = basket_lists(user_id)
            bot.send_message(message.chat.id, send_mess)

            def restore(message):
                for el in restore_pls:
                    if message.text.startswith(el):
                        from Processors.Lists.lists import restore_from_basket
                        send_mess = restore_from_basket(user_id, message.text)
                        bot.send_message(message.chat.id, send_mess)
                        time.sleep(1.5)
                        list_handler(message)
                        return

                list_handler(message)

            if send_mess == 'Ваша корзина пуста':
                time.sleep(1.5)
                list_handler(message)
            else:
                bot.register_next_step_handler(message, restore)

        elif message.text.startswith('Новый список') or message.text.startswith('новый список'):
            send_mess = 'Какое будет название списка?'
            bot.send_message(message.chat.id, send_mess)

            def new_list_creation(message):
                list_name = message.text
                send_mess = f'Отлично, список {list_name} почти готов. Чтобы наполнить его, пиши элементы, ' \
                            f'каждый с новой строки'
                bot.send_message(message.chat.id, send_mess)

                def new_list_elements(message):
                    from Processors.Lists.lists import new_list, items_in_list
                    send_mess = new_list(user_id, list_name, message)
                    bot.send_message(message.chat.id, send_mess)
                    time.sleep(1.5)
                    list_handler(message)

                bot.register_next_step_handler(message, new_list_elements)
            bot.register_next_step_handler(message, new_list_creation)

        else:
            print('else running')
            from Processors.Lists.lists import items_in_list
            send_mess, list_name = items_in_list(user_id, message.text)
            print(list_name)
            bot.send_message(message.chat.id, send_mess)

            def items_handler(message):
                print('items_handler running')
                for el in del_pls:
                    if message.text.startswith(el):
                        from Processors.Lists.lists import delete_items
                        send_mess = delete_items(user_id, message.text, list_name)
                        bot.send_message(message.chat.id, send_mess)
                        return

                for el in add_pls:
                    if message.text.startswith(el):
                        from Processors.Lists.lists import add_items, your_lists
                        send_mess = add_items(user_id, message.text, list_name)
                        bot.send_message(message.chat.id, send_mess)
                        time.sleep(1.5)
                        list_handler(message)
                        return

                for el in basket:
                    if message.text.startswith(el):
                        print('Restore items running')
                        from Processors.Lists.lists import basket_items
                        send_mess = basket_items(user_id, list_name)
                        bot.send_message(message.chat.id, send_mess)
                        if send_mess.endswith('пуста'):
                            send_mess = '/lists'
                            bot.send_message(message.chat.id, send_mess)

                        def restore_or_skip(message):
                            for el in restore_pls:
                                if message.text.startswith(el):
                                    print('restore_or_skip running')
                                    from Processors.Lists.lists import restore_items
                                    send_mess = restore_items(user_id, list_name, message.text)
                                    bot.send_message(message.chat.id, send_mess)
                                    time.sleep(1.5)
                                    list_handler(message)
                                    return

                            list_handler(message)

                        bot.register_next_step_handler(message, restore_or_skip)

                for el in random_pls:
                    if message.text.startswith(el):
                        from Processors.Lists.lists import random_item
                        random_item(user_id, list_name, message)
                        bot.send_message(message.chat.id, 'Готово!')
                        time.sleep(2)
                        bot.send_message(message.chat.id, '/lists')


            if send_mess.startswith('У вас нет списка'):
                time.sleep(1.5)
                messages(message)
            else:
                bot.register_next_step_handler(message, items_handler)

    bot.register_next_step_handler(message, what_to_do)


@bot.message_handler(commands=['name'])
def name_change(message):
    send_mess = 'Как мне тебя называть?'
    log(message.text, message.from_user.username, send_mess)
    bot.send_message(message.from_user.id, send_mess)

    def name_change(message):
        from Processors.user_recognition import name_change
        name_change(message.from_user.id, message.text)
        send_mess = 'Готово, теперь я буду звать тебя ' + message.text
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

    bot.register_next_step_handler(message, name_change)


@bot.message_handler(content_types=['text'])
def messages(message):
    global lists
    from Processors.text_respond import respond_processor
    send_mess = respond_processor(message)
    log(message.text, message.from_user.username, send_mess)
    bot.send_message(message.from_user.id, send_mess)


@bot.message_handler(content_types=['photo'])
def photo(message):
    send_mess = 'О, картинка! Что мне с ней делать?'
    log(message.text, message.from_user.username, send_mess)
    bot.send_message(message.from_user.id, send_mess)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    from Processors.food_processor import food_handler
    food_handler(call)
    from Processors.timer import timer_pross
    timer_pross(call)


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        time.sleep(0.5)