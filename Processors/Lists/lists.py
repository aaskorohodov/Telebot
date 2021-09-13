import random
import sqlite3
import time


def technical():
    '''Это технические функции для создания базы и таблиц'''
    def base_creation():
        '''Создание базы и таблицы'''
        conn = sqlite3.connect('my_lists.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS lists(
        userid INT,
        list_name TEXT,
        list_items TEXT);
        ''')
        conn.commit()

    def basket_items_creation():
        conn = sqlite3.connect('my_lists.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS items_basket(
            userid INT,
            list_name TEXT,
            list_items TEXT);
            ''')
        conn.commit()

    def basket_lists_creation():
        conn = sqlite3.connect('my_lists.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS lists_basket(
                userid INT,
                list_name TEXT,
                list_items TEXT);
                ''')
        conn.commit()


def your_lists(user_id):
    '''Эта функция показывает все списки в базе'''

    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    '''Так как функция импортируется и вызывается из другого места (Bot.py), то нужно указать путь до базы'''

    cur = conn.cursor()
    cur.execute(f'SELECT lists.list_name FROM lists WHERE userid = {user_id}')
    my_lists = cur.fetchall()
    '''my_lists = список кортежей, где каждый кортеж = название списка. Ввиду конструкции базы, где строка = id, список
    и содержание списка, будут повторы, то есть название списка будет повторятся столько раз, сколько есть в этом
    списке элементов. С этим разберемся ниже.'''

    if len(my_lists) == 0:
        '''Это проверка на наличие открытых (доступных, не в корзине) списков'''
        return 'У вас нет списков, давайте сделаем их.'

    lists = ''
    lists_counter = []
    '''lists = финальная строка, которую отправим пользователю. lists_counter нужен, чтобы не повторять список,
    ведь как было сказано выше, тут будут повторы названия списка. Впрочем, ниже проблема повторов решена еще на стороне
    SQL-запроса. *my_lists = список кортежей, поэтому:...'''
    for tupl in my_lists:
        '''...для каждого кортежа в списке (а в кортеже одно название списка)...'''
        for el in tupl:
            '''...распаковываем кортеж'''
            if el not in lists_counter:
                '''Если это название списка еще не встречалось:'''
                lists += f'– {el}\n'
                lists_counter.append(el)
                '''Тут собирается финальная строка и список с названиями списков'''

    def all_lists_you_have():
        '''Считает сколько у вас всего открытых списков и списков в корзине'''
        basket_lists = 0
        lists_in_use = 0
        cur.execute(f'SELECT count(DISTINCT list_name) FROM lists WHERE userid = {user_id}')
        '''count(DISTINCT list_name) отдает число уникальных списков (не считает повторы).
        Этот запрос смотрит на активные списки'''

        for el in cur:
            '''Объект Cursor поддерживает перебор. Но в нем всего 1 значение (число списков). Ниже все аналогично 
            для списков в корзине'''
            lists_in_use = el[0]

        cur.execute(f'SELECT count(DISTINCT list_name) FROM lists_basket WHERE userid = {user_id}')
        for el in cur:
            basket_lists = el[0]

        return lists_in_use, basket_lists  # возвращается 2 числа, названия говорящие

    lists_in_use, basket_lists = all_lists_you_have()

    '''Далее формируется ответ'''
    return f'Ваши списки:\n{lists}\n\n' \
           f'Всего списков: {lists_in_use}\n' \
           f'Списков в корзине: {basket_lists}\n\n' \
           f'Можно:\n' \
           f'– написать название списка, чтобы я показал что в нем\n' \
           f'– написать "Удали НАЗВАНИЕ СПИСКА"\n'\
           f'– написать "Новый список"\n'\
           f'– если у тебя есть списки в корзине, напиши "Корзина"\n\n' \
           f'Для выхода, напиши что-угодно другое'


def basket_lists(user_id):
    '''Эта функция показывает списки в корзине'''
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f'SELECT lists_basket.list_name FROM lists_basket WHERE userid = {user_id}')
    my_lists = cur.fetchall()

    if len(my_lists) == 0:
        '''Проверяется, не пуста ли корзина'''
        return 'Ваша корзина пуста'

    lists = ''  # строка со списками, часть ответа
    lists_counter = []  # собирает уникальные списки

    for tupl in my_lists:
        '''Распаковывает SQL-ответ (там список кортежей)'''
        for el in tupl:
            if el not in lists_counter:
                lists += f'– {el}\n'
                lists_counter.append(el)

    return f'В корзине:' \
           f'\n{lists}\n' \
           f'Если хочешь восстановить список, напиши:\n' \
           f'"Восстанови НАЗВАНИЕ СПИСКА" (в 1 строку)\n\n' \
           f'Или напиши что угодно другое, и в тебя прилетит меню списков'


def items_in_list(user_id, list_name, trigger=False):
    '''Проверяет, что лежит в конкретном списке'''
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT list_items FROM lists WHERE list_name = '{list_name}' AND userid = {user_id}""")

    '''Тут {list_name} стоит в кавычках, потому что иначе, при распаковке {list_name} питон убирает кавычки, а они
    нужны для SQL запроса.'''

    all_results = cur.fetchall()

    if len(all_results) > 0:
        '''Проверка, если такой список. Если нет, работает else'''

        mess = f'{list_name}:\n'  # подготавливаем шаблон ответа

        for tupl in all_results:
            '''Аналогично описанию выше – распаковываем список, в нем распаковываем кортежи.'''
            for el in tupl:
                mess += f'– {el}\n'
                '''Что там лежит, кладем в ответ'''

        '''mess это ответ. Также возвращается list_name (он был принят этой функцией). list_name нужен дальше, в
        основном теле Бота'''
        if trigger == False:
            mess += '\n\nЧтобы добавить элемент в этот список, пиши:\n"Добавить:\n' \
                    'Элемент (с новой строки)\n' \
                    'Ещё элемент (с новой строки)"\n\n' \
                    'Чтобы удалить элемент, пиши:\n"Удали:\n' \
                    'Элемент (с новой строки)\n' \
                    'Ещё элемент (с новой строки)"\n\n' \
                    'Чтобы проверить корзину этого списка, напиши "Корзина"\n\n' \
                    'Рандомный элемент из списка – напиши Рандом\n\n' \
                    '*есть чувствительность к регистру.\n' \
                    '**я различаю элементы по новой строке, так что можно сделать 1 элемент из кучи слов'
            return mess, list_name
        else:
            return mess

    else:
        mess = f'У вас нет списка {list_name}\n' \
               f'/lists\n' \
               f'А я пока перейду в режим общения'
        return mess, list_name


def random_item(user_id, list_name, message):
    '''Выбирает рандомный элемент списка. Message нужен, так как эта функция сама отвечает, ей нужен message,
    import telebot и адрес Бота'''
    import telebot
    bot = telebot.TeleBot('1879041775:AAG14Vz9P4AP4hjOGOOwYKbbFJGFSrWQEgs')

    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT list_items FROM lists WHERE list_name = '{list_name}' AND userid = {user_id}""")
    all_items = cur.fetchall()

    if len(all_items) == 1:
        '''Проверка, достаточно ли элементов. В ином случае, Telebot не сможет изменить сообщение и плюнет ошибкой, 
        так что надо прервать функцию.'''
        mess = 'Мало элементов для рандома!'
        bot.send_message(message.chat.id, mess)
        return

    random_from_here = []  # сюда сейчас сложим распакованные SQL-ответ (в ответе список кортежей, их надо распаковать)

    for tupl in all_items:
        for el in tupl:
            random_from_here.append(el)

    '''Бот кидает сообщение, затем изменяет его. Идея в том, чтобы быстро менять сообщение (типо барабан крутится).
    Это делается циклом, рандомность обеспечивается счетчиком, значение которого выбирается рандомно, а затем
    уменьшается. Когда счетчик достигает 0, все готово.'''

    msq = bot.send_message(message.chat.id, 'Рандом!')
    time.sleep(1)
    bot.edit_message_text('Крутите барабан!', chat_id=message.chat.id, message_id=msq.message_id)
    time.sleep(1)

    a = random.randint(1, 30)
    for i in range(0, 100):
        '''Если в ходе цикла бот не поменяет сообщение, то вылетит ошибка. Чтобы этого избежать (идти по списку кругом),
        первый цикл много раз перебирает второй, а второй проходит список с начала до конца. На каждой итерации
        значение счетчика (a) уменьшается на 1. С циклом while были какие-то проблемы, но он тут конечно уместнее.'''
        for y in range(0, len(random_from_here)):
            local_el = random_from_here[y]
            bot.edit_message_text(local_el, chat_id=message.chat.id, message_id=msq.message_id)
            a -= 1
            if a < 0:
                time.sleep(1)
                bot.send_message(message.chat.id, 'Готово!')
                return  # это прерывание цикла


def delete_list(user_id, text):
    '''Функция перемещает список в "корзину". Для корзины есть своя таблица, при перемещении данные копируются в
    lists_basket и удаляются из таблицы lists'''

    def replace_delete(text):
        '''Так как функция получает необработанный текст сообщения, сначала из него удаляется команда "Удалить"'''
        del_pls = ['удали ', 'Удали ', 'удали: ', 'Удали: ', 'удалить ', 'Удалить ', 'удалить: ', 'Удалить: ', 'elfkb ', 'elfkbnm ', 'Elfkb ', 'Elfkbnm ']
        for el in del_pls:
            if text.startswith(el):
                '''Когда найдено совпадение, оно удаляется, и удаляется всего 1 раз (вдруг есть список с таким именем)
                Совпадение точно будет найдено, так как текст уже был прочитан ранее в теле Бота, триггер уже сработал'''
                text = text.replace(el, '', 1)
                return text

    list_name = replace_delete(text)  # возвращается готовый текст с именем списка, который нужно удалить

    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM lists WHERE list_name = '{list_name}' AND userid = {user_id}''')
    '''Выбираем все строки с нужным именем списка (строк может быть несколько, поэтому ниже перебор)'''
    list_to_delete = cur.fetchall()

    if len(list_to_delete) > 0:
        '''Защита от неверного имени списка (если пользователь попросил удалить список, которого не существует)'''
        for el in list_to_delete:
            cur.execute(f'''INSERT INTO lists_basket(userid, list_name, list_items) 
                        VALUES
                        (?, ?, ?)
                        ''', el)  # это массовая передача элементов в SQL-запрос
        cur.execute(f'''DELETE FROM lists where userid = {user_id} AND list_name = '{list_name}';''')
        conn.commit()
        mess = f'Список "{list_name}" перемещен в корзину'
        return mess

    elif list_name is None:
        '''Защита от неверного запроса (название списка было передано с новой строки)'''

        return f'В одну строку, пожалуйста'
    else:
        return f'Списка {list_name} не нахожу в твоих списках'


def restore_from_basket(user_id, text):
    '''Функция возвращает список из "корзины"'''

    def replace_restore(text):
        '''Функция получает текст весь текст сообщения (удали НАЗВАНИЕ_СПИСКА). Тут убираем кусок "удали".
        restore_pls это слова триггеры, по которым включается эта функция. Их и нужно удалить из текста.'''
        restore_pls = ['Восстанови ', 'восстанови ', 'Востанови ', 'востанови ', 'Восстановить ', 'восстановить ', 'Востановить ', 'востановить ']
        for el in restore_pls:
            if text.startswith(el):
                text = text.replace(el, '', 1)  # заменяем 1 раз, на случай если список имеет подобное имя
                return text

    list_name = replace_restore(text)  # list_name = имя списка, который нужно восстановить

    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM lists_basket WHERE list_name = '{list_name}' AND userid = {user_id}''')
    all_lists = cur.fetchall()
    '''Выше all_lists собирает все строки, которые содержат нужный список. Поэтому ниже перебор.
    *fetchall вернет список кортежей, поэтому ниже в cur.execute его можно передавать вторым аргументом'''

    if len(all_lists) > 0:  # > 0 это защита от неверного имени списка (если такого списка нет в корзине)
        '''Сначала переносим строки в таблицу lists (INSERT), затем удаляем из lists_basket (DELETE)'''

        for el in all_lists:
            cur.execute(f'''INSERT INTO lists(userid, list_name, list_items)
                            VALUES
                            (?, ?, ?)
                        ''', el)

        cur.execute(f'''DELETE FROM lists_basket where userid = {user_id} AND list_name = '{list_name}';''')
        conn.commit()
        mess = f'Список "{list_name}" возвращен из корзины'
        return mess
    else:
        return f'Что-то пошло не так, проверь правильно ли ты написал название списка. Я не бог, а машина – ' \
               f'мне нужны четкие циферы и буковы.'


def new_list(user_id, list_name, message):
    '''Создает новый список. Принимает message, в котором передаются элементы нового списка.'''
    text = message.text
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    items = text.split('\n')
    '''items это питоновский список, в котором содержатся элементы для списка пользователя'''

    for item in items:
        '''Перебирая элементы, мы заносим каждый в таблицу'''
        insertion = (user_id, list_name, item)
        cur.execute(f'''INSERT INTO lists(userid, list_name, list_items)
                            VALUES
                            (?, ?, ?)''', insertion)
    conn.commit()

    mess = f'Список {list_name} готов'
    return mess


def delete_items(user_id, text, list_name):
    '''Удаляет элементы из списка, перенося из в корзину'''

    def replace_deletion(text):
        '''Убирает из текста слова триггеры (del_pls)'''

        del_pls = ['удали\n', 'Удали\n', 'удали:\n', 'Удали:\n', 'удалить\n', 'Удалить\n', 'удалить:\n', 'Удалить:\n']
        for el in del_pls:
            if text.startswith(el):
                text = text.replace(el, '', 1)
                return text

    text = replace_deletion(text)  # содержит элементы, которые нужно удалить, каждый с новой строки
    items_to_delete = text.split('\n')  # превращаем текст в питоновский список, разделяя по переносу строки

    if len(items_to_delete) == 0:
        '''Защита от пустого сообщения, если пользователь ввел "удали", но не указал что удалить'''

        mess = 'Нечего удалять\n' \
               '/lists'
        return mess

    else:
        '''else для наглядности (мол, если items_to_delete != 0, то else)'''

        is_there_anything = []
        '''is_there_anything собирает строки из таблицы пользователя. Нужен чтобы проверить, есть ли у пользователя
        запрошенные к удалению элементы в таблице (вдруг опечатка)'''

        for el in items_to_delete:
            '''Перебираем заявленные к удалению элементы, каждый ищем в таблице'''

            conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
            cur = conn.cursor()
            cur.execute(f'''
                        SELECT userid, list_name, list_items FROM lists WHERE userid = {user_id} 
                        AND list_name = '{list_name}' AND list_items = '{el}'
                        ;''')
            line = cur.fetchone()  # line = кортеж с 1 элементом (может оказаться пустым)

            try:
                is_there_anything.append(line[0])
                '''Пробуем сложить любой элемент [нулевой, например] в проверочный список. Если из таблицы достали
                пустой список, то нечего будет складывать, тогда отработает исключение'''
            except Exception:
                pass

        if len(is_there_anything) == 0:
            '''Проверяем, нашлось ли хоть что-нибудь в таблице (если ли там заявленные к удалению элементы)'''

            mess = 'Таких элементов не обнаружено! Проверь регистр (заглавные буквы) и правописание. ' \
                   'Также обрати внимание, что символ – не относится к элементу. Сложновато, но ты быстро вкатишься.\n' \
                   '/lists'
            return mess
        else:
            '''deleted_items запишет все, что удалось найти и соответственно удалить.
            not_deleted_items запишет то, чего с списке пользователя не оказалось.
            Затем мы передадим это пользователю, отчитавшись о проделанной работе'''
            deleted_items = []
            not_deleted_items = []

            for el in items_to_delete:
                '''Перебираем заявленные к удалению элементы, каждый заново читаем из таблицы, переносим в корзину,
                удаляем из списка'''

                conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
                cur = conn.cursor()
                cur.execute(f'''
                SELECT userid, list_name, list_items FROM lists WHERE userid = {user_id} 
                AND list_name = '{list_name}' AND list_items = '{el}'
                ;''')
                line = cur.fetchone()

                if line is None:
                    '''Проверяем, достали мы элемент из таблицы, или его там нет. Если нет, то записываем его чтобы
                    отчитаться, а если элемент есть, то работает else'''
                    not_deleted_items.append(el)

                else:
                    '''Записывает элемент в корзину, затем удаляет из активных списков'''

                    cur.execute(f'''
                    INSERT INTO items_basket(userid, list_name, list_items) 
                        VALUES
                        (?, ?, ?)
                        ''', line)

                    cur.execute(f'''
                    DELETE FROM lists WHERE userid = {user_id} AND list_name = '{list_name}' AND list_items = '{el}';
                    ''')

                    '''line = кортеж, где на [2] стоит имя элемента. Если код дошел сюда, то кортеж НЕ пустой,
                    следовательно мы записываем элемент [2], чтобы потом отчитаться перед пользователем'''
                    deleted_items.append(line[2])

                conn.commit()

            '''Когда цикл прошел по всем элементам, остается составить ответ. Начинаем с болванок mess1 и mess2 –
            в первую пишем что мы нашли и удалили, во вторую что не смогли найти в SQL-таблице'''
            mess1 = 'Удалено:\n'
            mess2 = '\nНе найдено:\n'

            for el in deleted_items:
                '''Каждый элемент просто добавляем в mess1 и mess2 с новой строки'''
                mess1 += f'– {el}\n'
            for el in not_deleted_items:
                mess2 += f'– {el}\n'

            if len(mess2.split('\n')) == 3:
                '''Если все прошло супер-успешно и НЕ удаленных элементов нет, то нам не нужно передавать пользователю
                "Не найдено" (ведь тут будет пусто). Если разбить пустую болванку mess2 по новой строке, то в
                получившемся списке будет 3 элемента. В этой ситуации мы пропустим mess2, а иначе (else), добавим
                mess2 к mess1, что и станет нашим ответным сообщением.'''
                pass
            else:
                mess1 += mess2

    '''Далее проверяем, остался ли вообще список, после наших манипуляций, или мы все утащили в корзину'''

    def is_there_list_left():
        '''Этот кусок кода сложен в отдельную функцию, чтобы обособиться визуально'''

        nonlocal mess1  # берем mess1 из предыдущей области видимости
        conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
        cur = conn.cursor()
        cur.execute(f'''
                        SELECT userid, list_name FROM lists WHERE userid = {user_id} 
                        AND list_name = '{list_name}'
                        ;''')
        line = cur.fetchone()
        '''Берем строку из таблицы, смотрим лишь на название списка. Нас интересует любой результат, есть ли там хоть
        что-то, поэтому fetchONE сойдет'''

        if line is None:
            '''Если мы более не находим список с этим именем в таблице, значит выше мы удалили все его элементы и теперь
            он целиком лежит в корзине для элементов. Тогда нам нужно перенести все элементы в корзину для списков,
            чтобы по запросу к корзине списков, мы видели этот список.'''

            mess_no_list = f'\nСписок {list_name} теперь пустой и будет лежать в корзине'
            mess1 += mess_no_list  # Дополняем ответное сообщение

            '''Далее вытащим все элементы списка из корзины для элементов, пройдем по ним циклом и запишем все в корзину
            для списков, удалим все записи по имени списка из корзины для элементов'''
            cur.execute(f'''
            SELECT userid, list_name, list_items FROM items_basket WHERE userid = {user_id} AND list_name = '{list_name}'
            ''')
            list_for_basket = cur.fetchall()

            for el in list_for_basket:
                cur.execute(f'''
                INSERT INTO lists_basket
                        VALUES
                        (?, ?, ?)
                ''', el)

            cur.execute(f'''
            DELETE FROM items_basket WHERE userid = {user_id} AND list_name = '{list_name}';
            ''')
            conn.commit()

        '''Так как мы находимся внутри функции в другой функции, то return проводим дважды'''
        return mess1

    send_mess = is_there_list_left()
    return send_mess


def add_items(user_id, text, list_name):
    '''Добавляем элементы в список'''

    def replace_add(text):
        '''Обрезаем слова-триггеры'''
        add_pls = ['добавь\n', 'Добавь\n', 'добавить\n', 'Добавить\n', 'добавь:\n', 'Добавь:\n', 'добавить:\n', 'Добавить:\n']
        for el in add_pls:
            if text.startswith(el):
                text = text.replace(el, '', 1)
                return text

    try:
        '''Удалив триггеры, пытаемся разбить текст по новой строке. Если не получается, значит сообщение пустое.'''
        items_to_add = replace_add(text).split('\n')  # делим по новой строке результат функции. Получаем список
    except Exception:
        mess = 'Нечего добавлять\n'
        return mess

    mess = f'В список {list_name} добавлено:\n'  # болванка-ответ
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()

    for el in items_to_add:
        '''Перебирая элементы списка items_to_add мы не только добавляем их в SQL-таблицу, но и дополняем ответ'''
        insertion = (user_id, list_name, el)
        cur.execute(f'''
                    INSERT INTO lists(userid, list_name, list_items)
                    VALUES
                    (?, ?, ?)
                    ''', insertion)
        mess += f'– {el}\n'

    conn.commit()

    return mess


def basket_items(user_id, list_name):
    '''Показывает элементы списка в корзине'''
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f"SELECT items_basket.list_items FROM items_basket WHERE userid = {user_id} AND list_name = '{list_name}'")
    my_items = cur.fetchall()

    if len(my_items) == 0:
        '''Проверяется, не пуста ли корзина'''
        return f'Корзина списка {list_name} пуста'
    else:
        lists = ''  # перечень элементов в корзине (строка)

        for tupl in my_items:
            '''Распаковывается список кортежей (из ответа cur.fetchall). Каждый элемент записывается в строку'''
            for el in tupl:
                lists += f'– {el}\n'

        return f'В корзине списка {list_name}:' \
               f'\n{lists}\n' \
               f'Если хочешь восстановить элемент, напиши\n' \
               f'"Восстанови:\n' \
               f'ЭЛЕМЕНТ (каждый элемент с новой строки)\n' \
               f'ЭЛЕМЕНТ\n\n' \
               f'Или напиши что угодно другое, и в тебя прилетит меню списков'


def restore_items(user_id, list_name, text):
    '''Восстанавливает элемент из корзины'''
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()

    def replace_restore(text):
        '''Удаляет из текста слова-триггеры'''

        restore_item_pls = ['Восстанови:\n', 'восстанови:\n', 'Востанови:\n', 'востанови:\n', 'Восстановить:\n', 'восстановить:\n', 'Востановить:\n', 'востановить:\n'
                            'Восстанови: \n', 'восстанови: \n', 'Востанови: \n', 'востанови: \n', 'Восстановить: \n', 'восстановить: \n', 'Востановить: \n', 'востановить: \n'
                            'Восстанови \n', 'восстанови \n', 'Востанови \n', 'востанови \n', 'Восстановить \n', 'восстановить \n', 'Востановить \n', 'востановить \n'
                            'Восстанови\n', 'восстанови\n', 'Востанови\n', 'востанови\n', 'Восстановить\n', 'восстановить\n', 'Востановить\n', 'востановить\n']

        for el in restore_item_pls:
            if text.startswith(el):
                text = text.replace(el, '', 1)
                return text

    try:
        '''Пробуем разбить текст на элементы для восстановления. Если это не получается (пользователь дал триггер, но
        не дал элемент), то даем ответ сразу'''
        items_to_restore = replace_restore(text).split('\n')
    except Exception:
        mess = 'Таких элементов в этом списке нет'
        return mess

    '''Создаем болванки, туда будем писать что удалось восстановить, а чего нет (опечатка пользователя, например)'''
    mess = 'Восстановлено:\n'
    mess1 = '\nНе нашлось:\n'

    for el in items_to_restore:
        '''Перебираем элементы для восстановления, если клемента нет в таблице (line is None) пишем этот элемент в одно
        место, а если такой элемент есть в корзине, то возвращаем его в таблицу активных списков'''
        cur.execute(f"""SELECT * FROM items_basket WHERE userid = {user_id} AND list_name = '{list_name}' AND list_items = '{el}'""")
        line = cur.fetchone()

        if line is None:
            mess1 += f'– {el}\n'

        else:
            cur.execute(f"""INSERT INTO lists
                        VALUES
                        (?, ?, ?)
                        """, line)

            cur.execute(F"""DELETE FROM items_basket where userid = {user_id} AND list_name = '{list_name}' AND list_items = '{el}'""")
            mess += f'– {el}\n'

    conn.commit()

    '''Проверяем, все ли нашлось. Если да, то нам не нужен mess1'''
    if mess1 != '\nНе нашлось:\n':
        mess += mess1

    '''Если ничего не нашлось, то возвращаем ТОЛЬКО список того, что не нашлось (болванку mess не передаем)'''
    if mess == 'Восстановлено:\n':
        return mess1

    '''В ном случае (если все нашлось), возвращаем только mess, без второй болванки.'''
    return mess
