import random
import sqlite3


def technical():
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
        return 'У вас нет списков, давайте сделаем их.'

    else:
        lists = ''
        lists_counter = []
        '''lists = финальная строка, которую отправим пользователю. lists_counter нужен, чтобы не повторять список,
        ведь как было сказано выше, тут будут повторы названия списка.
        *my_lists = список кортежей, поэтому:...'''
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
            basket_lists = 0
            lists_in_use = 0
            cur.execute(f'SELECT count(DISTINCT list_name) FROM lists WHERE userid = {user_id}')

            for el in cur:
                lists_in_use = el[0]

            cur.execute(f'SELECT count(DISTINCT list_name) FROM lists_basket WHERE userid = {user_id}')
            for el in cur:
                basket_lists = el[0]

            return lists_in_use, basket_lists

        lists_in_use, basket_lists = all_lists_you_have()

        return f'Ваши списки:\n{lists}\n\n' \
               f'Всего списков: {lists_in_use}\n' \
               f'Списков в корзине: {basket_lists}\n\n' \
               f'Можно:\n' \
               f'– написать название списка, чтобы я показал что в нем\n' \
               f'– написать "Удали НАЗВАНИЕ СПИСКА"\n'\
               f'– написать "Новый список"\n'\
               f'– если у тебя есть списки в корзине, напиши "Корзина"\n'


def basket_lists(user_id):
    '''Эта функция показывает списки в корзине'''
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f'SELECT lists_basket.list_name FROM lists_basket WHERE userid = {user_id}')
    my_lists = cur.fetchall()

    if len(my_lists) == 0:
        '''Проверяется, не пуста ли корзина'''
        return 'Ваша корзина пуста'
    else:
        lists = ''
        lists_counter = []

        for tupl in my_lists:
            for el in tupl:
                if el not in lists_counter:
                    lists += f'– {el}\n'
                    lists_counter.append(el)
        return f'В корзине:\n{lists}\nЕсли хочешь восстановить список, напиши "Восстанови НАЗВАНИЕ СПИСКА"\n\n' \
               f'Или напиши что угодно другое, и в тебя прилетит меню списков'


def items_in_list(user_id, list_name):
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT list_items FROM lists WHERE list_name = '{list_name}' AND userid = {user_id}""")

    '''Тут {list_name} стоит в кавычках, потому что иначе, при распаковке {list_name} питон убирает кавычки, а они
    нужны для SQL запроса.'''

    all_results = cur.fetchall()

    if len(all_results) > 0:
        mess = f'{list_name}:\n'  # подготавливаем шаблон ответа

        for tupl in all_results:
            '''Аналогично описанию выше (your_lists) – распаковываем список, в нем распаковываем кортежи.'''
            for el in tupl:
                mess += f'– {el}\n'
                '''Что там лежит, кладем в ответ'''

        mess += '\n\nЧтобы добавить элемент в этот список, пиши "Добавить:\n' \
                'Элемент (с новой строки)\n' \
                'Ещё элемент (с новой строки)"\n\n' \
                'Чтобы удалить элемент, пиши "Удали:\n' \
                'Элемент (с новой строки)\n' \
                'Ещё элемент (с новой строки)"\n\n' \
                'Чтобы проверить корзину этого списка, напиши "Корзина"\n\n' \
                'Рандомный элемент из списка – напиши Рандом\n\n' \
                '*есть чувствительность к регистру.\n' \
                '**я различаю элементы по новой строке, так что можно сделать 1 элемент из кучи слов'
        return mess, list_name

    else:
        mess = f'У вас нет списка {list_name}'
        return mess, list_name


def random_item(user_id, list_name, message):
    import telebot
    bot = telebot.TeleBot('1879041775:AAG14Vz9P4AP4hjOGOOwYKbbFJGFSrWQEgs')

    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT list_items FROM lists WHERE list_name = '{list_name}' AND userid = {user_id}""")

    all_items = cur.fetchall()
    print(all_items)
    random_from_here = []

    for tupl in all_items:
        for el in tupl:
            random_from_here.append(el)

    start_el = random_from_here[0]
    msq = bot.send_message(message.chat.id, start_el)
    a = random.randint(1, 30)
    for i in range(0, len(random_from_here)):
        for y in range(0, len(random_from_here) - 1):
            local_el = random_from_here[y + 1]
            bot.edit_message_text(local_el, chat_id=message.chat.id, message_id=msq.message_id)
            a -= 1
            print(a)
            if a < 0:
                return


def delete_list(user_id, text):
    '''Функция перемещает список в "корзину"'''

    def replace_delete(text):
        del_pls = ['удали ', 'Удали ', 'удали: ', 'Удали: ', 'удалить ', 'Удалить ', 'удалить: ', 'Удалить: ', 'elfkb ', 'elfkbnm ', 'Elfkb ', 'Elfkbnm ']
        for el in del_pls:
            if text.startswith(el):
                text = text.replace(el, '', 1)
                return text

    list_name = replace_delete(text)

    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM lists WHERE list_name = '{list_name}' AND userid = {user_id}''')
    list_to_delete = cur.fetchall()
    if len(list_to_delete) > 0:
        for el in list_to_delete:
            cur.execute(f'''INSERT INTO lists_basket(userid, list_name, list_items) 
                        VALUES
                        (?, ?, ?)
                        ''', el)
        cur.execute(f'''DELETE FROM lists where userid = {user_id} AND list_name = '{list_name}';''')
        conn.commit()
        mess = f'Список "{list_name}" перемещен в корзину'
        return mess
    else:
        return f'Списка {list_name} не нахожу в твоих списках'


def restore_from_basket(user_id, text):
    '''Функция возвращает список из "корзины"'''
    def replace_restore(text):
        restore_pls = ['Восстанови ', 'восстанови ', 'Востанови ', 'востанови ', 'Восстановить ', 'восстановить ', 'Востановить ', 'востановить ']
        for el in restore_pls:
            if text.startswith(el):
                text = text.replace(el, '', 1)
                return text

    list_name = replace_restore(text)

    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM lists_basket WHERE list_name = '{list_name}' AND userid = {user_id}''')
    all_lists = cur.fetchall()
    if len(all_lists) > 0:
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
    text = message.text
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    items = text.split('\n')
    for item in items:
        insertion = (user_id, list_name, item)
        print(insertion)
        cur.execute(f'''INSERT INTO lists(userid, list_name, list_items)
                            VALUES
                            (?, ?, ?)''', insertion)
    conn.commit()

    mess = f'Список {list_name} готов'
    return mess


def delete_items(user_id, text, list_name):
    print('delete_items running')

    def replace_deletion(text):
        print('replace_deletion running')
        del_pls = ['удали\n', 'Удали\n', 'удали:\n', 'Удали:\n', 'удалить\n', 'Удалить\n', 'удалить:\n', 'Удалить:\n']
        for el in del_pls:
            if text.startswith(el):
                text = text.replace(el, '', 1)
                print(text)
                return text

    text = replace_deletion(text)
    print('Prepeared text: ', text)
    items_to_delete = text.split('\n')
    print('items_to_delete: ', items_to_delete)
    if len(items_to_delete) == 0:
        mess = 'Нечего удалять\n' \
               '/lists'
        return mess
    else:
        print('else 1 is rinnung')
        is_there_anything = []
        for el in items_to_delete:
            conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
            cur = conn.cursor()

            print('user_id, list_name, el: ', user_id, list_name, el)
            cur.execute(f'''
                        SELECT userid, list_name, list_items FROM lists WHERE userid = {user_id} 
                        AND list_name = '{list_name}' AND list_items = '{el}'
                        ;''')
            line = cur.fetchone()
            print('line = ', line)
            try:
                print('Trying to append')
                is_there_anything.append(line[0])
            except Exception as e:
                print('Exeption: ', e)

        print(is_there_anything)

        if len(is_there_anything) == 0:
            print('is_there_anything = 0 running')
            mess = 'Таких элементов не обнаружено! Проверь регистр (заглавные буквы) и правописание. ' \
                   'Также обрати внимание, что символ – не относится к элементу. Сложновато, но ты быстро вкатишься.'
            return mess
        else:
            print('else 2 is running')
            deleted_items = []
            not_deleted_items = []
            for el in items_to_delete:
                print('items_to_delete running')
                conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
                cur = conn.cursor()

                cur.execute(f'''
                SELECT userid, list_name, list_items FROM lists WHERE userid = {user_id} 
                AND list_name = '{list_name}' AND list_items = '{el}'
                ;''')
                line = cur.fetchone()
                print('line = ', line)
                if line is None:
                    not_deleted_items.append(el)
                else:
                    print('else 3 in running')
                    cur.execute(f'''
                    INSERT INTO items_basket(userid, list_name, list_items) 
                        VALUES
                        (?, ?, ?)
                        ''', line)
                    print('INSERT INTO items_basket done')
                    cur.execute(f'''
                    DELETE FROM lists WHERE userid = {user_id} AND list_name = '{list_name}' AND list_items = '{el}';
                    ''')
                    print('DELETE FROM lists done')
                    deleted_items.append(line[2])
                    print('deleted_items appending: ', line[2])

                conn.commit()

            print('deleted_items: ', deleted_items)
            print('not_deleted_items: ', not_deleted_items)

            mess1 = 'Удалено:\n'
            mess2 = '\nНе найдено:\n'

            for el in deleted_items:
                mess1 += f'– {el}\n'
            for el in not_deleted_items:
                mess2 += f'– {el}\n'

            if len(mess2.split('\n')) == 2:
                pass
            else:
                mess1 += mess2

            is_there_list = []

            def is_there_list_left():
                nonlocal mess1
                conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
                cur = conn.cursor()

                cur.execute(f'''
                                SELECT userid, list_name, list_items FROM lists WHERE userid = {user_id} 
                                AND list_name = '{list_name}' AND list_items = '{el}'
                                ;''')
                line = cur.fetchone()
                print('line = ', line)

                if line is None:
                    print('line is none')
                    pass
                else:
                    is_there_list.append(line)

                if len(is_there_list) != 0:
                    mess_no_list = f'\nСписок {list_name} теперь пустой и будет лежать в корзине'
                    mess1 += mess_no_list

            is_there_list_left()

            print('prepeared message: ', mess1)
            return mess1


def add_items(user_id, text, list_name):
    def replace_add(text):
        print('replace_add running')
        add_pls = ['добавь\n', 'Добавь\n', 'добавить\n', 'Добавить\n', 'добавь:\n', 'Добавь:\n', 'добавить:\n', 'Добавить:\n']
        for el in add_pls:
            if text.startswith(el):
                text = text.replace(el, '', 1)
                print(text)
                return text
    try:
        items_to_add = replace_add(text).split('\n')
    except Exception:
        mess = 'Нечего добавлять\n'
        return mess

    print(items_to_add)

    mess = f'В список {list_name} обавлено:\n'

    if len(items_to_add) == 0:
        mess = 'Нечего добавлять'
        return mess
    else:
        conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
        cur = conn.cursor()
        for el in items_to_add:
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
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f"SELECT items_basket.list_items FROM items_basket WHERE userid = {user_id} AND list_name = '{list_name}'")
    my_items = cur.fetchall()

    if len(my_items) == 0:
        '''Проверяется, не пуста ли корзина'''
        return f'Корзина списка {list_name} пуста'
    else:
        lists = ''

        for tupl in my_items:
            for el in tupl:
                lists += f'– {el}\n'

        return f'В корзине списка {list_name}:\n{lists}\nЕсли хочешь восстановить элемент, напиши\n"Восстанови:\n' \
               f'ЭЛЕМЕНТ (каждый элемент с новой строки)\nЭЛЕМЕНТ\n\n' \
               f'Или напиши что угодно другое, и в тебя прилетит меню списков'


def restore_items(user_id, list_name, text):
    print('restore_items running')
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()

    def replace_restore(text):
        print('replace_restore running')

        restore_item_pls = ['Восстанови:\n', 'восстанови:\n', 'Востанови:\n', 'востанови:\n', 'Восстановить:\n', 'восстановить:\n', 'Востановить:\n', 'востановить:\n'
                            'Восстанови: \n', 'восстанови: \n', 'Востанови: \n', 'востанови: \n', 'Восстановить: \n', 'восстановить: \n', 'Востановить: \n', 'востановить: \n'
                            'Восстанови \n', 'восстанови \n', 'Востанови \n', 'востанови \n', 'Восстановить \n', 'восстановить \n', 'Востановить \n', 'востановить \n'
                            'Восстанови\n', 'восстанови\n', 'Востанови\n', 'востанови\n', 'Восстановить\n', 'восстановить\n', 'Востановить\n', 'востановить\n']
        for el in restore_item_pls:
            if text.startswith(el):
                text = text.replace(el, '', 1)
                print('text = ', text)
                return text

    try:
        items_to_restore = replace_restore(text).split('\n')
        print('items_to_restore =', items_to_restore)
    except Exception:
        items_to_restore = []

    if len(items_to_restore) == 0:
        mess = 'Таких элементов в этом списке нет'
        return mess


    mess = 'Восстановлено:\n'
    mess1 = '\nНе нашлось:\n'
    for el in items_to_restore:
        print('Перебор items_to_restore')
        cur.execute(f"""SELECT * FROM items_basket WHERE userid = {user_id} AND list_name = '{list_name}' AND list_items = '{el}'""")
        line = cur.fetchone()
        print('line =', line)

        if line is None:
            mess1 += f'– {el}\n'
            print('mess1 is now =', mess1)

        else:
            cur.execute(f"""INSERT INTO lists
                        VALUES
                        (?, ?, ?)
                        """, line)
            print('INSERT INTO lists done')

            cur.execute(F"""DELETE FROM items_basket where userid = {user_id} AND list_name = '{list_name}' AND list_items = '{el}'""")
            print('DELETE FROM items_basket done')
            mess += f'– {el}\n'
            print('mess is now =', mess)

    conn.commit()

    if mess1 != '\nНе нашлось:\n':
        mess += mess1

    if mess == 'Восстановлено:\n':
        print(r"if mess == 'Восстановлено:\n':")
        return mess1

    print('mess is finally =', mess)
    return mess
