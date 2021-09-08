import sqlite3 as sq


def file():
    with sq.connect('lists.db') as con:
        cur = con.cursor()

        cur.execute('''CREATE TABLE Lists (
        id INTEGER,
        lists_name TEXT,
        content TEXT
        )''')


def lists_checker(message):
    user_id = message.from_user.id
    with sq.connect('lists.db') as con:
        cur = con.cursor()

        cur.execute(f'''
        SELECT lists_name FROM lists
        WHERE id = {user_id}
        GROUP BY lists_name
        ''')
        res = cur.fetchall()
        print(res)

        send_mess = f'Ваши списки:\n'
        commands = []

        if res == []:
            print('У вас нет списков')
            return 'У вас нет списков', None
        else:
            for el in res:
                send_mess += f'\n/{el[0]}'
                commands.append(el[0])

            print(send_mess)
            print(commands)
            return send_mess, commands


def list_creating(message):
    list_name = message.text
    user_id = message.from_user.id
    with sq.connect('lists.db') as con:
        cur = con.cursor()

        cur.execute(f'''
        INSERT INTO lists VALUES({user_id}, '{list_name}', '')
        ''')

    send_mess, commands = lists_checker(message)
    return send_mess, commands


def items(message):
    list_name = message.text
    list_name = list_name.replace('/', '')
    user_id = message.from_user.id
    with sq.connect('lists.db') as con:
        cur = con.cursor()
        cur.execute(f'''
        SELECT content FROM lists
        WHERE id = {user_id} and
        lists_name = '{list_name}'
        ''')

        res = cur.fetchall()

        send_mess = f'Список {list_name}:\n'
        for el in res:
            send_mess += f'\n{el[0]}'

        add = f'\n\n' \
              f'Чтобы удалить элемент(ы) из списка, напишите:\n"удалить элемент элемент элемент"\n\n' \
              f'Чтобы добавить элемент(ы) в список, напишите: \n"добавить элемент элемент элемент"'
        send_mess += add
        return send_mess, list_name


#items('bugs', 307136361)

