import random, time, telebot
from telebot import types
from Processors.log import log
from Processors.user_recognition import user_recognition
'''
Telebot работает на декораторах. Получая сообщение, Бот идет сверху вниз, проверяя, подходит ли какой-то декоратор
для полученного сообщения. Тут могут быть как команды (/start/help...) так и сообщения другого типа, например простой
текст, картинки, файлы итд. Если Бот уткнулся на подходящий декоратор, то проверять следующие уже не будет, как
следствие, логику обработки того/иного сообщения или команды нужно прописывать внутри декоратора. Поэтому часть кода
унесены во вспомогательные файлы, иначе слишком много строчек.

В некоторых метах используется bot.register_next_step_handler вместо простого вызова функции. Это нужно, чтобы передать
в вызываемую функцию какое-то сообщение от пользователя. Например, когда сработал декоратор, то Бот может попросить
дополнительную информацию у пользователя. Когда информация получена, бот передаст сообщение в вызываемую функцию
как раз с помощью bot.register_next_step_handler
'''


bot = telebot.TeleBot('1879041775:AAG14Vz9P4AP4hjOGOOwYKbbFJGFSrWQEgs')
# stop это список стоп-слов, которыми можно остановить ту или иную функцию
stop = ['все', 'Все', 'ВСЕ', 'ВСе', 'всё', 'ВСё', 'ВСЁ', 'Всё', 'dct', 'Dct', 'DCt', 'DCT', 'dc`', 'Dc`', 'DC`', 'DC~']


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    '''Приветствие. Тут бот знакомится с пользователем, если прежде его не встречал и шлет список команд.'''
    from Processors.user_recognition import user_recognition
    '''user_recognition распознает пользователя, либо отдает False, если встречает пользователя впервые'''

    name = user_recognition(message.from_user.id)

    if name == False:
        '''Сценарий нового пользователя'''

        send_mess = 'Кажется, мы еще не знакомы! Как тебя зовут?'
        bot.send_message(message.from_user.id, send_mess)

        # лог занимается записью всего, что тут происходит
        log(message.text, message.from_user.username, send_mess)

        def whats_ur_name(message):
            '''Записывает имя нового пользователя в базу. excl = то, что может ввести пользователь перед своим именем'''

            excl = ['меня', 'зовут', 'я', 'а', 'тебя', 'как', 'звать', 'name', 'my', 'зови', 'пускай', 'будет']

            # строка, куда запишем имя. Затем передадим это имя в функцию new_user
            name = ''

            # перебираем текст от пользователя, убираем ненужные куски
            for el in message.text.split():
                if el not in excl:
                    name += el

            # стоит именно тут для наглядности процесса
            from Processors.user_recognition import new_user

            new_user(message.from_user.id, name)
            bot.send_message(message.from_user.id, 'Отлично, теперь давай начнем сначала')
            log(message.text, message.from_user.username, send_mess)
            time.sleep(2)

            # рекурсивно вызывает саму себя, чтобы теперь отработал else (ниже)
            send_welcome(message)

        bot.register_next_step_handler(message, whats_ur_name)

    else:
        '''Сценарий, когда пользователь уже знаком боту'''

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
    '''Отвечает за всякие штуки (stuff, очепятка). Работает на if/elif, каждое из которых обрабатывает свою команду,
    Но весь модуль (декоратор) откликается на весь перечень команд.
    *name используется, чтобы (местами) персонализировано отвечать'''

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
        '''Переворачивает любой текст'''

        send_mess = 'Все что вы напишите, будет перевернуто.\n' \
                    'Для выхода пиши "все"'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

        def reversed(message):
            '''Сам код тут'''

            if message.text in stop:
                '''Остановка фичи'''

                send_mess = 'reversed остановлен.\n' \
                            '/start для продолжения'
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.chat.id, send_mess)

            else:
                from Processors.stuff import reversed_words
                '''reversed_words разворачивает строку и отдает ее обратно'''

                send_mess = reversed_words(message.text)
                bot.send_message(message.chat.id, send_mess)
                log(message.text, message.from_user.username, send_mess)
                bot.register_next_step_handler(message, reversed)  # рекурсивно вызывает саму себя

        bot.register_next_step_handler(message, reversed)

    elif message.text == '/popka':
        '''Попка (попугай) слегка меняет текст и отдает его пользователю'''

        def popca_pross(message):
            if message.text in stop:
                '''Остановка фичи'''

                send_mess = 'Popka завершен\n' \
                            '/start для продолжения'
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.from_user.id, send_mess)

            else:
                from Processors.stuff import popka_talking

                send_mess = popka_talking(message.text)
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.from_user.id, send_mess)
                bot.register_next_step_handler(message, popca_pross)  # вызывает саму себя

        send_mess = 'Пишите что хотите, когда надоест, напишите "все".'
        bot.send_message(message.chat.id, send_mess)
        log(message.text, message.from_user.username, send_mess)
        bot.register_next_step_handler(message, popca_pross)

    elif message.text == '/time':
        '''Показывает время в любом городе (почти любом)'''

        send_mess = 'Какой город смотрим?'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

        def time_get(message):
            from Processors.time import output
            '''output делает запрос к стороннему API, чтобы достать оттуда время в каком-то городе. Так интереснее'''

            send_mess = output(message.text)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.chat.id, send_mess)

        bot.register_next_step_handler(message, time_get)

    elif message.text == '/pics':
        from PIL import Image
        '''Берет рандомную картинку из локального хранилища и кидает в пользователя'''

        t = [i for i in range(204)]  # генерируем список. его длина = количество картинок
        ran = str(random.choice(t))  # берем из списка рандомное число
        name = fr'C:\Users\Аркадий\Pictures\py\1 ({ran}).JPG'  # подставляем его в имя файла
        png = Image.open(name)  # открываем нужную картинку

        send_mess = 'Вот:'  # кидаем в пользователя текст
        bot.send_message(message.chat.id, send_mess)

        log(message.text, message.from_user.username, send_mess)
        bot.send_photo(message.from_user.id, png)  # кидаем в пользователя картинку

    elif message.text == '/weather':
        '''Делает запрос через стороннее API, получает погоду в любом городе'''

        send_mess = f'{name}, в каком городе ты живешь?'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

        def weather_pros(message):
            '''wf_output самостоятельно готовит ответ, собирает красивую строку и отдает ее.'''
            from Processors.weather_udvanced import wf_output

            send_mess = wf_output(message.text)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)

        bot.register_next_step_handler(message, weather_pros)

    elif message.text == '/food':
        '''Подсказка что поесть. Работает на клавишах, которые надо нажимать. После нажатия на какую-то кнопку, готовит
        новый набор кнопок, с другими вопросами. Тут готовится только первый набор кнопок, за остальные отвечает
        query_handler, он внизу кода'''

        # задается тип разметки для кнопок
        markup = telebot.types.InlineKeyboardMarkup()

        # далее сами кнопки (3 шт), которые добавляем в разметку
        self = types.InlineKeyboardButton(text='Готовим сами', callback_data="self")
        fast = types.InlineKeyboardButton(text='Готовое дома', callback_data="fast")
        outdoor = types.InlineKeyboardButton(text='Сходить в...', callback_data="outdoor")
        markup.add(self, fast, outdoor)

        send_mess = f'Что хочет {name}?'
        log(message.text, message.from_user.username, send_mess)

        # метод send_message берет не только сообщение, но и подготовленную разметку, которую кидает после сообщения
        bot.send_message(message.from_user.id, send_mess, reply_markup=markup)

        # вся дальнейшая работа фичи реализована в callback_query_handler, внизу Бота

    elif message.text == '/covid':
        '''Парсер, собирает информацию о Ковиде'''
        log(message.text, message.from_user.username)
        from Processors.covid import covid

        # В отличие от многих других модулей, covid сам отправляет сообщение, так что его достаточно просто вызвать
        covid(message)

    elif message.text == '/anagramm':
        '''Поиск анаграмм'''

        send_mess = f'{name}, дай текст, а я найду в нем анаграммы.\n' \
                    '\n' \
                    '*поддерживается только английский и русский'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

        def anagramms_pross(message):
            '''Механизм работы anagrams lовольно сложный, он подробно описан в другом проекте (Learning Python)'''
            from Processors.stuff import anagrams

            send_mess = anagrams(message.text)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)

        bot.register_next_step_handler(message, anagramms_pross)

    elif message.text == '/letters':
        '''Считает повторы букв'''
        send_mess = f'{name}, давай свой текст, а я посчитаю повторы букв'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

        def letters(message):
            '''Считает повторы каждой буквы в переданном тексте'''
            from Processors.stuff import letters_counter

            send_mess = letters_counter(message.text)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)

        bot.register_next_step_handler(message, letters)

    elif message.text == '/timer':
        '''Ставит таймер. Таймер работает поверх сообщений, то есть можно поставить таймер и продолжит общение
        Функционал полностью в своем файле, включая отправку сообщений'''
        from Processors.timer import timer_step1

        name = user_recognition(message.from_user.id)  # для персонального ответа
        timer_step1(message, name)

    elif message.text == '/b_day':
        '''Показывает, сколько времени осталось до дня рождения'''

        send_mess = f'Тут можно узнать, когда у кого-то будет следующий день рождения.\n' \
                    f'\n' \
                    f'Введи дату рождения в формате [Год Месяц День] через пробелы'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

        def birthday(message):
            '''age() самостоятельно проверяет введенную дату и готовит ответное сообщение'''
            from Processors.stuff import age

            send_mess = age(message.text)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.from_user.id, send_mess)

        bot.register_next_step_handler(message, birthday)

    elif message.text == '/translate':
        '''Это первый ответ на фичу-переводчик. Тут в пользователя лишь кидается предложение выбрать язык перевода'''

        send_mess = '/ru_eng\n' \
                    '/eng_ru'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.from_user.id, send_mess)

    elif message.text == '/ru_eng':
        '''Переводит с русского на английский. Работает на API от ABBYY, все (и описание) внутри файла этого модуля'''

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


@bot.message_handler(commands=['math', 'calc', 'area', 'bmi', 'fib', 'odd_even'])
def math_handler(message):
    '''Обрабатывает команды модуля math. Декоратор откликается на весь перечень своих команд, а за обработку конкретной
    команды отвечает if'''

    if message.text == '/math':
        '''Общий ответ на модуль math. Кидает доступные фичи'''

        send_mess = 'Это матиматический модуль. Вот что я умею:\n' \
                    '\n' \
                    '/calc – калькулятор\n' \
                    '/area – площадь прямоугольника\n' \
                    '/bmi – рассчет массы тела\n' \
                    '/fib – число фибоначи\n' \
                    '/odd_even – четное или нечетное число'
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
            '''Сам обработчик калькулятора'''

            if message.text in stop:
                '''Закрытие калькулятора'''

                send_mess = 'Калькулятор закрыт.\n' \
                            '/start для продолжения'
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.from_user.id, send_mess)

            else:
                '''Калькулятор лежит в calc. Работает на eval'''
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
        '''Прежде чем посчитать BMI, Бот спрашивает вес и рост'''

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
                '''В BMI передает полученный вес и рост. bmi() готовит ответ.'''
                from Processors.math import bmi

                weight = message.text
                send_mess = bmi(height, weight)
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.chat.id, send_mess)

            bot.register_next_step_handler(message, weight)
        bot.register_next_step_handler(message, height)

    elif message.text == '/fib':
        send_mess = 'Напиши номер числа фибоначчи, а я покажу это число\n' \
                    '\n' \
                    '!!! Обрати внимание, что телеграмм не даст отправить слишком большое письмо. ' \
                    'Числа по номеру свыше ~15000 могут не пройти'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

        def fib_call(message):
            '''Очень простой способ, реализован в своем файле'''
            from Processors.math import fib

            send_mess = fib(message)
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.chat.id, send_mess)

        bot.register_next_step_handler(message, fib_call)

    elif message.text == '/odd_even':
        '''Проверяет число на четное или нечетное'''

        send_mess = 'Напиши число, а я проверю, четное оно или нет, используя лябда-выражение!' \
                    '(но ты не увидишь, как я это делаю)'
        log(message.text, message.from_user.username, send_mess)
        bot.send_message(message.chat.id, send_mess)

        def odd_even_pross(message):
            from Processors.math import clean_text_return_number

            number = clean_text_return_number(message.text)
            '''clean_text_return_number возвращает число, очищенное от любых других символов. Если в тексте не было 
            ни одного числа, то он вернет "Это не число", сработает блок if ниже.'''

            if number == 'Это не число':
                send_mess = 'Это не число. /odd_even'
                log(message.text, message.from_user.username, send_mess)
                bot.send_message(message.chat.id, send_mess)
                return  # выходит из цикла, чтобы не вызвать код ниже

            result = (lambda x: x % 2 and 'нечетное' or 'четное')(number)
            ''' В теле лямбды сначала идет and. Ему все равно, что там лежит, он просто проверяет, истинно это или ложно
            и возвращает последнее истинное значение, либо первое ложное. Если x % 2 = 1 (нечетное), то это истина, 
            and вернет "нечетное, в ином случае (если x % 2 = 0) вернется 0, потому что 0 = False.
                Затем срабатывает or, если ему досталось "нечетное", то он сравнит две истины и вернет первую. Если ему
            передали 0, то он вернет истину (т.е. "четное"). Вот и все.'''

            send_mess = f'Число {number} {result}. /odd_even'
            log(message.text, message.from_user.username, send_mess)
            bot.send_message(message.chat.id, send_mess)

        bot.register_next_step_handler(message, odd_even_pross)


@bot.message_handler(commands=['lists'])
def list_handler(message):
    '''Ворочает списками. Ниже 5 списков = слова-триггеры (команды) и user_id (чтобы показывать только ваши списки)'''

    basket = ['Корзина', 'корзина', 'rjhpbyf', 'Rjhpbyf']
    restore_pls = ['Восстанови', 'восстанови', 'Востанови', 'востанови', 'восстановить', 'Восстановить', 'востановить', 'Востановить']
    del_pls = ['удали', 'Удали', 'удали:', 'Удали:', 'удалить', 'Удалить', 'удалить:', 'Удалить:', 'elfkb', 'elfkbnm', 'Elfkb', 'Elfkbnm']
    add_pls = ['добавь', 'Добавь', 'добавить', 'Добавить', 'добавь:', 'Добавь:', 'добавить:', 'Добавить:']
    random_pls = ['рандом', 'Рандом', 'hfyljv', 'Hfyljv']
    user_id = message.from_user.id

    from Processors.Lists.lists import your_lists

    # возвращает готовое сообщение со списками, либо "у вас нет списков"
    send_mess = your_lists(user_id)
    bot.send_message(message.chat.id, send_mess)

    # Отрабатывает ситуацию отсутствия списков. Включается, если бот не нашел списков (смотрит на сообщение Бота)
    if send_mess == 'У вас нет списков, давайте сделаем их.':

        # немного ждет с последнего сообщения, чтобы не прилетало кучей
        time.sleep(1)

        # просит название списка
        send_mess = 'Какое будет название списка?'
        bot.send_message(message.chat.id, send_mess)

        def first_list_creation(message):
            '''Просит элементы списка от пользователя и запоминает имя списка'''

            list_name = message.text
            send_mess = f'Отлично, список {list_name} почти готов. Чтобы наполнить его, пиши элементы, ' \
                        f'каждый с новой строки'
            bot.send_message(message.chat.id, send_mess)

            def first_list_elements(message):
                '''Создает список с помощью new_list, затем показывает содержание списка с помощью items_in_list,
                затем отправляется в начало list_handler'''
                from Processors.Lists.lists import new_list, items_in_list

                send_mess = new_list(user_id, list_name, message)
                bot.send_message(message.chat.id, send_mess)
                time.sleep(1.5)

                send_mess = items_in_list(user_id, list_name, True)
                bot.send_message(message.chat.id, send_mess)
                time.sleep(1.5)

                list_handler(message)

            bot.register_next_step_handler(message, first_list_elements)
        bot.register_next_step_handler(message, first_list_creation)

    # else срабатывает, если у пользователя есть списки. На этом этапе Бот уже кинул перечень списков, теперь
    # пользователь может что-то с ними сделать, но нам нужно сообщение от пользователя с командом.
    # поэтому в else есть register_next_step_handler, который ждет сообщения, а затем обрабатывает его блоками if
    else:
        def what_to_do(message):
            if message.text.startswith('удали') or message.text.startswith('Удали'):
                '''Удаление списка'''
                from Processors.Lists.lists import delete_list

                # перемещает список в корзину и готовит ответ
                send_mess = delete_list(user_id, message.text)
                bot.send_message(message.chat.id, send_mess)
                time.sleep(1.5)  # немного ждет, затем кидает в начало списков
                list_handler(message)

            elif message.text in basket:
                '''Показывает содержание корзины.'''
                from Processors.Lists.lists import basket_lists

                send_mess = basket_lists(user_id)  # готовит ответ, затем идет блок if
                bot.send_message(message.chat.id, send_mess)

                def restore(message):
                    '''Может либо восстановить список из корзины (блок for), либо вернуться в начало меню списков'''

                    for el in restore_pls:
                        '''Проверяет, не начинается ли сообщение с триггера "Восстанови" '''

                        if message.text.startswith(el):
                            from Processors.Lists.lists import restore_from_basket

                            send_mess = restore_from_basket(user_id, message.text)  # восстанавливает список
                            bot.send_message(message.chat.id, send_mess)
                            time.sleep(1.5)

                            list_handler(message)
                            '''Так как мы в цикле, то нам нужно его прервать, в случае триггера. Это делает return.
                            Возможна ситуация срабатывания нескольких триггеров (Удали = Удали/Удалить/Удалить:...)'''
                            return

                    list_handler(message)

                if send_mess == 'Ваша корзина пуста':
                    time.sleep(1.5)
                    list_handler(message)
                else:
                    bot.register_next_step_handler(message, restore)

            elif message.text.startswith('Новый список') or message.text.startswith('новый список'):
                '''Отрабатывает создание нового списка'''

                send_mess = 'Какое будет название списка?'
                bot.send_message(message.chat.id, send_mess)

                def new_list_creation(message):
                    list_name = message.text
                    send_mess = f'Отлично, список {list_name} почти готов. Чтобы наполнить его, пиши элементы, ' \
                                f'каждый с новой строки'
                    bot.send_message(message.chat.id, send_mess)

                    def new_list_elements(message):
                        '''Завершает создание нового списка. Кидает подтверждение создания, содержание нового списка и
                        возвращается в начало меню списка'''
                        from Processors.Lists.lists import new_list, items_in_list

                        send_mess = new_list(user_id, list_name, message)
                        bot.send_message(message.chat.id, send_mess)
                        time.sleep(1.5)

                        send_mess = items_in_list(user_id, list_name, True)
                        bot.send_message(message.chat.id, send_mess)
                        time.sleep(1.5)

                        list_handler(message)

                    bot.register_next_step_handler(message, new_list_elements)
                bot.register_next_step_handler(message, new_list_creation)

            else:
                '''Отрабатывает в случае, если выше if не были активированы. Показывает содержание списка, имеет свои
                триггеры, которые работают с элементами списка. Если триггеры выше не сработали, и триггеры ниже
                тоже не сработают, то выйдет из меню списков и передаст сообщение в менеджер общения'''
                from Processors.Lists.lists import items_in_list

                send_mess, list_name = items_in_list(user_id, message.text)
                bot.send_message(message.chat.id, send_mess)

                def items_handler(message):
                    '''Проверяет, есть ли триггеры для работы с элементами списка'''

                    for el in del_pls:
                        '''Удаление элемента'''

                        if message.text.startswith(el):
                            from Processors.Lists.lists import delete_items

                            send_mess = delete_items(user_id, message.text, list_name)  # удаляет элемент, готовит ответ
                            bot.send_message(message.chat.id, send_mess)
                            time.sleep(1.5)
                            list_handler(message)
                            return  # нужен, так как мы в цикле. Цикл нужно сломать (мы уще и в функции)

                    for el in add_pls:
                        '''Добавление элемента'''

                        if message.text.startswith(el):
                            from Processors.Lists.lists import add_items

                            send_mess = add_items(user_id, message.text, list_name)
                            bot.send_message(message.chat.id, send_mess)
                            time.sleep(1.5)

                            list_handler(message)
                            return

                    for el in basket:
                        '''Триггер на проверку корзины конкретного списка'''

                        if message.text.startswith(el):
                            from Processors.Lists.lists import basket_items

                            send_mess = basket_items(user_id, list_name)  # смотрит элементы в корзине списка
                            bot.send_message(message.chat.id, send_mess)

                            if send_mess.endswith('пуста'):
                                '''Работает в случае, если корзина этого списка пуста'''

                                send_mess = '/lists'
                                bot.send_message(message.chat.id, send_mess)

                            def restore_or_skip(message):
                                '''Находясь в корзине списка, проверяет, есть ли триггер к восстановлению элемента'''

                                for el in restore_pls:
                                    if message.text.startswith(el):
                                        from Processors.Lists.lists import restore_items

                                        send_mess = restore_items(user_id, list_name, message.text)
                                        bot.send_message(message.chat.id, send_mess)
                                        time.sleep(1.5)

                                        list_handler(message)
                                        return

                                list_handler(message)

                            bot.register_next_step_handler(message, restore_or_skip)

                    for el in random_pls:
                        '''Триггер на рандомный элемент в списке'''

                        if message.text.startswith(el):
                            '''random_item сам отправляет сообщение и делает все, что нужно. Остается только
                            предложить пользователю вернуться в начало меню'''
                            from Processors.Lists.lists import random_item

                            random_item(user_id, list_name, message)
                            time.sleep(2)
                            bot.send_message(message.chat.id, '/lists')


                if send_mess.startswith('У вас нет списка'):
                    '''Выход из меню списков. Работает, если не не удалось найти списка с нужным именем'''

                    time.sleep(1.5)
                    messages(message)
                else:
                    bot.register_next_step_handler(message, items_handler)

        bot.register_next_step_handler(message, what_to_do)


@bot.message_handler(commands=['name'])
def name_change(message):
    '''Меняет имя. Это функция нужна чтобы принять имя пользователя, следующая уже записывает его'''

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
    '''Отвечает за общение (чат-бот)'''
    from Processors.text_respond import respond_processor
    from Processors.user_specs_checker import user_specs_checker_atention

    # извлекаем attention_status. Это 1 либо 0, показывали мы предупреждение этому пользователю или еще нет
    attention_status = user_specs_checker_atention(message.from_user.id)

    # если еще нет, то показываем. Предупреждение показывается 1 раз одному пользователю.
    if attention_status != 1:
        send_mess = 'Внимание! Бот обладает базой ответов, которую может использовать в некоторых случаях общения. ' \
                    'База обучена на общении со школьниками в интернетах, так что изобилует матом, нецензурщиной ' \
                    'и просто оборотами, которые легко можно счесть неприемлемыми. Продолжая общение с ботом вы ' \
                    'подтверждаете, что кровоточащие глазки вас не пугают.'
        bot.send_message(message.from_user.id, send_mess)
        time.sleep(5)
        send_mess = 'Модуль общения теперь активирован. Начинается общение.'
        bot.send_message(message.from_user.id, send_mess)
        time.sleep(2)

    # затем вызывается модуль общения
    send_mess = respond_processor(message)
    log(message.text, message.from_user.username, send_mess)
    bot.send_message(message.from_user.id, send_mess)


@bot.message_handler(content_types=['photo'])
def photo(message):
    '''Включается, если пользователь отправил фото'''
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