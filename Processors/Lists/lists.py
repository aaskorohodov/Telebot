import sqlite3


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
        ведь как было сказано выше, тут будут повторы названия списка. *my_lists = список кортежей, поэтому:'''
        for tupl in my_lists:
            '''Для каждого кортежа в списке (а в кортеже одно название списка)'''
            for el in tupl:
                '''Распаковываем кортеж'''
                if el not in lists_counter:
                    '''Если это название списка еще не встречалось:'''
                    lists += f'– {el}\n'
                    lists_counter.append(el)
                    '''Тут собирается финальная строка и список с названиями списков'''
        return f'Ваши списки:\n{lists}\nМожно:\n' \
               f'– написать название списка, чтобы я показал что в нем\n' \
               f'– написать "Удали НАЗВАНИЕ СПИСКА"\n'\
               f'– написать "Новый список"'\
               f'– если у тебя есть списки в корзине, напиши "Корзина"\n'


def basket_lists(user_id):
    '''Эта функция показывает списки в корзине'''
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f'SELECT lists.list_name FROM lists WHERE userid = {user_id}')
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
                '*есть чувствительность к регистру.\n' \
                '**я различаю элементы по новой строке, так что можно сделать 1 элемент из кучи слов'
        return mess

    else:
        mess = f'у вас нет списка {list_name}\n/lists'
        return mess


def delete_list(user_id, text):
    '''Функция перемещает список в "корзину"'''
    text = text.replace('удали ', '', 1)
    list = text.replace('Удали ', '', 1)
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f'''SELECT list_name FROM lists WHERE list_name = '{list}' AND userid = {user_id}''')
    all_lists = cur.fetchall()
    if len(all_lists) > 0:
        basket_id = int(str(user_id) + '55555')
        cur.execute(f'''UPDATE lists SET userid = {basket_id} WHERE list_name = '{list}' AND userid = {user_id};''')
        conn.commit()
        mess = f'Список "{list}" перемещен в корзину'
        return mess
    else:
        return f'Списка {list} не нахожу в твоих списках'


def restore_from_basket(basket_id, text):
    '''Функция возвращает список из "корзины"'''
    text = text.replace('Восстанови ', '', 1)
    text = text.replace('восстанови ', '', 1)
    text = text.replace('Востанови ', '', 1)
    list = text.replace('востанови ', '', 1)

    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()
    cur.execute(f'''SELECT list_name FROM lists WHERE list_name = '{list}' AND userid = {basket_id}''')
    all_lists = cur.fetchall()
    if len(all_lists) > 0:
        restored_id = int(str(basket_id).replace('55555', '', 1))
        cur.execute(f'''UPDATE lists SET userid = {restored_id} WHERE list_name = '{list}' AND userid = {basket_id};''')
        conn.commit()
        mess = f'Список "{list}" возвращен из корзины'
        return mess
    else:
        return f'Что-то пошло не так, проверь правильно ли ты написал название списка. Я не бог, а машина – ' \
               f'мне нужны четкие циферы и буковы.'


def new_list(user_id, list_name, message):
    print('new_list running')
    text = message.text
    print(text)
    conn = sqlite3.connect(r'Processors/Lists/my_lists.db')
    cur = conn.cursor()

    items = text.split('\n')
    print(items)
    for item in items:
        insertion = (user_id, list_name, item)
        print('insertion:', insertion)
        cur.execute(f'''INSERT INTO lists(userid, list_name, list_items)
                            VALUES
                            (?, ?, ?)''', insertion)
    conn.commit()

    mess = f'Список {list_name} готов'
    return mess



def delete_expand(user_id, text):
    text = text.replace('удали:\n', '', 1)
    lists = text.replace('Удали:\n', '', 1)
    print(lists)
    lists = lists.split('\n')
    print(lists)


def insert(user_id, list, item):
    insertion = (user_id, list, item)
    conn = sqlite3.connect('my_lists.db')
    cur = conn.cursor()
    cur.execute(f'''INSERT INTO lists(userid, list_name, list_items)
                    VALUES
                    (?, ?, ?)''', insertion)
    conn.commit()


def insert_into_existing_list(user_id, my_list, mess_text):
    items = []
    for el in mess_text.split('\n'):
        items.append(el)

    conn = sqlite3.connect('my_lists.db')
    cur = conn.cursor()
    cur.execute(f'SELECT lists.list_name FROM lists WHERE userid = {user_id}')
    all_lists = cur.fetchall()

    for tupl in all_lists:
        for el in tupl:
            if el == my_list:
                for el in items:
                    insert(user_id, my_list, el)
            else:
                pass

