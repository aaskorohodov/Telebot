import pickle
'''pickle используется, так как тип хранения = словарь, который лежит в txt файле'''


def user_recognition(user_id):
    '''Распознает пользователя'''
    try:
        with open('users.txt', 'rb') as file:
            users = pickle.load(file)
    except EOFError:
        '''На случай пустого файла (нет ни одного пользователя) создается пустой словарь, чтобы дальше все работало'''
        users = {}

    if user_id in users:
        name = users[user_id]
        return name
    else:
        return False


def new_user(user_id, name):
    '''Создает нового пользователя'''
    try:
        with open('users.txt', 'rb') as file:
            users = pickle.load(file)
    except EOFError:
        '''На случай пустого файла'''
        users = {}
        users[user_id] = name  # в ключ кладем id, в значение кладем имя

    users[user_id] = name  # если же файл не пустой, то делаем все аналогично

    with open('users.txt', 'wb') as file:  # пишем в файл
        pickle.dump(users, file)


def name_change(id, new_name):
    '''Меняет имя пользователя'''
    with open('users.txt', 'rb') as file:
        users = pickle.load(file)

    users[id] = new_name  # переписывает имя, обращаясь по id

    with open('users.txt', 'wb') as file:
        pickle.dump(users, file)