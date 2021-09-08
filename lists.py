import pickle


def list_creating(message):
    try:
        with open('list.txt', 'rb') as file:
            lists = pickle.load(file)
    except EOFError:
        lists = {}

    mes = message.text
    user_id = str(message.from_user.id)
    new_list = {mes: []}
    lists[user_id] = new_list

    with open('list.txt', 'wb') as file:
        pickle.dump(lists, file)

    return f'Список /{mes} создан'


def listing(message, list_name):
    mes = message
    list_items = mes.split('\n')

    try:
        with open('list.txt', 'rb') as file:
            lists = pickle.load(file)
    except EOFError:
        return 'У вас нету списков'

    for el in list_items:
        lists[user_id][list_name].append(el)

    with open('list.txt', 'wb') as file:
        pickle.dump(lists, file)


def lists_reading(message):
    try:
        with open('list.txt', 'rb') as file:
            lists = pickle.load(file)
    except EOFError:
        lists = {}

    try:
        send_mess = 'Ваши списки:\n'
        commands = []

        user_id = str(message.from_user.id)
        my_lists = lists[user_id]
        for el in my_lists.keys():
            send_mess += f'/{el}\n'
            commands.append(el)
        return send_mess, commands
    except:
        return 'У вас пока нет списков', None


def items_reading(message):
    with open('list.txt', 'rb') as file:
        lists = pickle.load(file)

    mes = message.text.replace('/', '')
    print(lists)
    items = lists[str(message.from_user.id)][mes]

    send_mess = ''
    for el in items:
        send_mess += el

    if send_mess == '':
        return f'Список {mes} пуст', None