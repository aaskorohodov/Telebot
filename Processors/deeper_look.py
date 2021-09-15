import pickle
import random
import shelve
import pandas as pd


def tecnical():
    '''Используются для создания подготовки словаря для этого модуля. Вызываются вручную по необходимости'''
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

    def dict_open_pickle():
        with open('deeper_look.txt', 'rb') as file:
            my_dict = pickle.load(file)

        print(my_dict)
        print(type(my_dict))


def deeper_responde(message):
    '''Модуль обращается к файлу, который представляет собой словарь. В словаре ключами являются возможные сообщения
    от пользователя, а в значениях ответы. При этом ответов может быть несколько на 1 сообщение, но словарь не может
    содержать идентичные ключи. Поэтому повторяющиеся ключи дополнены рандомным числом, например: что делаешь 0.32135
    Поиск проходит в несколько этапов, это не прямой поиск "сообщение = ключ", но первый этап прямой поиск.'''

    with open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\mega_dict', 'rb') as file:
        my_dict = pickle.load(file)

    # чистим сообщение пользователя от лишних знаков, чтобы проще найти соответствие
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя abcdefghijklmnopqrstuvwxyz1234567890'
    for el in message:
        if el not in alphabet:
            message = message.replace(el, '')

    def first_look(message):
        '''Это первый этап поиска ответа. Тут сообщение напрямую ищется в ключах словаря'''

        # в result записываются варианты ответа, чтобы потом выбрать рандомный, чтобы избежать одинаковых ответов
        result = []
        for el in my_dict.keys():
            if message in el:
                result.append(my_dict[el])

                # больше трех не ищем, как показал опыт – первые найденные ответы подходят лучше, чем некоторые в конце
                if len(result) > 3:
                    return random.choice(result)

        # (if для понятности кода) если first_look не дал ответа, то зовем trying, он поищет лучше
        if len(result) == 0:
            res = trying(message)
            return res

    def trying(message):
        '''Эта функция не ищет сама, но подготавливает текст для более глубокого поиска. Тут из сообщения удаляются
        слова по одному с конца. Получившаяся конструкция передается для дальнейшего поиска в след функцию'''

        # превращаем сообщение в список и готовим строку, куда перепишем это же сообщение, после удаления слова
        mes_list = list(message.split())
        string = ''

        # удаляем последнее слово, делаем это на 1 раз меньше, чем длина списка, чтобы не искать пустой список
        for i in range(len(mes_list) - 1):
            del mes_list[0]

            # пересобираем строку для поиска ответа
            for el in mes_list:
                string += el + ' '

            # чистим от пробельных символов с концов строки и отправляем строку в поиск
            string = string.strip()
            trying = second_look(string)

            # мы все равно возвращаем None, даже в случае неудачи, чтобы в предыдущем коде отработало другое условие
            if trying != None:
                return trying

            # обнуляем строку
            string = ''

    def second_look(string):
        '''Функция выполняет поиск по словарю, аналогична first_look'''

        result = []
        for el in my_dict.keys():
            if string in el:
                result.append(my_dict[el])
                if len(result) > 3:
                    return random.choice(result)

    res = first_look(message)
    return res