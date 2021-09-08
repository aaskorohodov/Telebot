import pickle
import random
import shelve
import pandas as pd


def dict_creation_shelf():
    df = pd.read_excel(r'C:\Users\Аркадий\Downloads\good2.xls', header=None)

    first = df[0]
    second = df[1]
    third = df[2]
    repl = df[3]

    keys = list(
        map(lambda a, b, c: str(a) + ' ' + str(b) + ' ' + str(c) + str(random.randint(1, 500)), first, second, third))

    my_dict = dict(zip(keys, repl))

    shelf = shelve.open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\Deeper_respond', 'c')

    for k, v in my_dict.items():
        shelf[k] = v
    shelf.close()


def dict_open():
    my_dict = shelve.open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\Deeper_respond')

    my_dict = dict(my_dict)
    return my_dict


def dict_creation_pickle():
    df = pd.read_excel(r'C:\Users\Аркадий\Downloads\good2.xls', header=None)

    first = df[0]
    second = df[1]
    third = df[2]
    repl = df[3]

    keys = list(
        map(lambda a, b, c: str(a) + ' ' + str(b) + ' ' + str(c) + str(random.randint(1, 500)), first, second, third))

    my_dict = dict(zip(keys, repl))

    with open('deeper_look.txt', 'wb') as file:
        pickle.dump(my_dict, file)


#dict_creation_pickle()


def dict_open_pickle():
    with open('deeper_look.txt', 'rb') as file:
        my_dict = pickle.load(file)

    print(my_dict)
    print(type(my_dict))


def deeper_responde(message):
    with open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\mega_dict', 'rb') as file:
        my_dict = pickle.load(file)

    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя abcdefghijklmnopqrstuvwxyz1234567890'
    for el in message:
        if el not in alphabet:
            message = message.replace(el, '')


    def first_look(message):
        result = []
        for el in my_dict.keys():
            if message in el:
                result.append(my_dict[el])
                if len(result) > 3:
                    print(f'first_look: {result}')
                    return random.choice(result)

        if len(result) == 0:
            res = trying(message)
            return res
        else:
            print(f'first_look: {result}')
            return (random.choice(result))


    def trying(message):
        mes_list = list(message.split())
        string = ''
        for i in range(len(mes_list) - 1):
            del mes_list[0]

            for el in mes_list:
                string += el + ' '
            string = string.strip()
            trying = second_look(string)
            if trying != None:
                return trying

            string = ''


    def second_look(string):
        result = []
        for el in my_dict.keys():
            if string in el:
                result.append(my_dict[el])
                if len(result) > 3:
                    print(f'second_look {string} -> {result}')
                    return random.choice(result)
                else:
                    pass

        if len(result) == 0:
            pass
        else:
            print(f'second_look {string} -> {result}')
            return (random.choice(result))


    res = first_look(message)
    return res