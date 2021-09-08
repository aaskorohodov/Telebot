import pickle


def user_recognition(user_id):
    try:
        with open('users.txt', 'rb') as file:
            users = pickle.load(file)
    except EOFError:
        users = {}

    if user_id in users:
        name = users[user_id]
        return name
    else:
        return False

def new_user(user_id, name):
    try:
        with open('users.txt', 'rb') as file:
            users = pickle.load(file)
    except EOFError:
        users = {}
        users[user_id] = name

    users[user_id] = name

    with open('users.txt', 'wb') as file:
        pickle.dump(users, file)


def name_change(id, new_name):
    with open('users.txt', 'rb') as file:
        users = pickle.load(file)

    users[id] = new_name

    with open('users.txt', 'wb') as file:
        pickle.dump(users, file)