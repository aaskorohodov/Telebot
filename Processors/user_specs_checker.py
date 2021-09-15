import sqlite3


def user_specs_checker_atention(user_id):
    '''Проверяет атрибуты пользователя. Атрибуты хранятся в таблице, в данном случае проверяется атрибут atention,
    которые может иметь значение 1 либо NULL в SQL и 1 либо 0 в питоне. Обозначает, встречал ли пользователь
    предупреждение при общении с ботом.'''

    # устанавливаем соединение и получаем нужную строчку
    conn = sqlite3.connect(r'Processors/users_specs.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users WHERE user_id = {user_id}')
    user_specs = cur.fetchone()

    # пробуем прочитать нужную ячейку
    try:
        atention_status = user_specs[1]

        # если она пуста (есть пользователь, но нет ячейка еще не заполнялась) то записываем туда 1, назад вернем 0
        if atention_status is None:
            cur.execute(f'''UPDATE users SET atention = 1 WHERE user_id = {user_id}''')
            atention_status = 0

    # если пользователя нет совсем, то извлечь [1] не получится, fetchone вернет None. Тогда записываем пользователя
    # и сразу записываем ему 1 (показали предупреждение)
    except:
        cur.execute(f'''INSERT INTO users (user_id, atention) VALUES({user_id}, 1)''')
        atention_status = 0

    conn.commit()
    return atention_status
