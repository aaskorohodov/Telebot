def words_only(text):
    text = text.lower()
    text = text.replace('\n', ' ')
    res = ''
    alphabet = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя '
    for el in text:
        if el in alphabet:
            print(el)
            res += el
    print(res)
    return res


def reversed_words(message):
    b = ''
    for el in message[::-1]:
        b += el
    return b


def popka_talking(message):
    s2 = ''
    for el in message:
        if el.lower() == 'р' or el == 'p':
            s2 += 'ррр'
        elif el.lower() == 'е' or el == 'e':
            s2 += 'еее'
        else:
            s2 += el
    s2 += '!'
    return s2


def anagrams(text):
    def letters(word):
        '''
        Вспомогательная функция, берет слово и сортирует буквы по алфавиту.
        Из интересного join – собирает список в строку. Ставится поверх строки, тут это пустая строка ''. Если составить
        в строке какой-то символ, то в результате этот символ будет стоять через каждый элемент списка.
        '''
        let = list(word)
        let.sort()
        let = ''.join(let)

        return let


    def anagrams(text):
        '''
        Основная функция – ищет анаграмы и собирает их в словарь, где ключ = буквы, значение = слова из этих букв.
        1. Делаем пустой словарь
        2. Перебираем элементы (слова) в строке слов. Там слова с новой строки, так что делим изходную строку через \n
        3. В переборе создаем временную l, туда кладем буквы, из которых состоит каждое слово
        4. Если l нет в пустом словаре, то записываем его в ключ, а значением ставим слово, из которого эти буквы родились.
        *значение ставим в список [], потому что из этих букв могут быть и другие слова, которые можно будет положить
        в этот же список с помощью append.
        5. А если l есть в словаре, то по ключу l (в значение) кладет это слово (в список).
        '''
        an_dict = {}
        for el in text.split():
            l = letters(el)

            if l not in an_dict:
                an_dict[l] = set([el])
            else:
                an_dict[l].add(el)

        return an_dict

    def print_anagrams_in_order(text):
        '''Печатает анаграммы в порядке их количества. Для этого в список списков заносятся сначала длина значения словаря
        (т.е. сколько там в списке слов), а потом сами слова'''
        text = words_only(text)
        an_list = []
        an_dict = anagrams(text)


        for el in an_dict.values():
            if len(el) > 1:
                an_list.append((len(el), el))

        an_list.sort()

        res = ''
        if len(an_list) == 0:
            return 'Нет анаграмм'
        else:
            res += 'Вот ваши анаграммы:\n'

        n = 0

        for el in an_list:
            res += '\n' + str(n+1) + ': '
            n = n+1
            for word in el[1]:
                res += word + ' '

        return res

    res = print_anagrams_in_order(text)
    return res


def letters_counter(text):
    '''Считает буквы в переданном тексте'''

    # в первом блоке опускаем текст,чистим его от всяких лишних символов, результат кладем в clean
    text = text.lower()
    alphabet = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя1234567890'
    clean = ''
    for el in text:
        if el in alphabet:
            clean += el

    # создаем словарь, идем по всем элементам clean, кладем элемент (букву) в ключ, в значение кладем цифру 1
    # затем увеличиваем цифру на 1 при повторной встрече символа
    my_dict = {}
    for el in clean:
        if el not in my_dict:
            my_dict[el] = 1
        else:
            my_dict[el] = my_dict[el] + 1

    # не знаю точно зачем, диапазон (не помню уже), но думаю, чтобы выставить повторы в порядке возрастания
    # соответственно проходим по диапазону, для каждого значения по возрастанию ищем ключ и значение, записываем, отдаем
    res = 'Буква: повторы\n'
    for i in range(10000):
        for k, v in my_dict.items():
            if i == v:
                res += f'\n{k}:   {v}'

    return res


def age(birth_date):
    '''Считает, сколько осталось до дня рождения, готовит немного разные сообщения на разные случаи.
    Также проверяет, корректную ли дату ввел пользователь'''
    from datetime import date

    # test тестирует, корректную ли дату ввел пользователь
    test = birth_date.split()

    try:
        '''Пробуем превратить каждый элемент testa в число.'''
        for el in test:
            int(el)
    except:
        return 'Что-то не то, попробуй еще раз /b_day'

    if len(test) != 3:
        '''Проверяем, что введено 3 числа (год, день, месяц)'''
        return 'Что-то не то, попробуй еще раз /b_day'


    try:
        '''Спрашиваем у модуля date-time, существует ли такая дата'''
        birth_date = date(int(test[0]), int(test[1]), int(test[2]))
    except:
        return 'Такой даты не существует. /b_day'

    # готовим send_mess, которая станет ответом, сегодняшнею дату и считаем возраст человека
    send_mess = ''
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    '''
    При подсчете возраста используется хитрая штука (today.month, today.day) < (birth_date.month, birth_date.day)
    Мы вычитаем сравнение, что возможно – сравнение вернет True либо False, первое равняется 1 другое 0, мы буквально
    можем вычесть True/False из int, это дозволено логикой питона.
    Это нужно, чтобы определить, был ли ДР в этом году (родился 2000, сейчас 2001 – ему еще 0 или уже 1?)
    '''

    # проверяем, родился ли человек или может он очень стар. Если еще не родился, то сразу return
    if age < 0:
        return 'Это существо еще не родилось. /b_day'
    if age > 80:
        send_mess += f'Возраст: {age} лет. Это много\n'
    else:
        send_mess += f'Возраст: {age} лет\n'

    # next_birthday еще не готова. Может быть сценарий, что в этом году ДР уже был. Это пофиксит ближайший if
    next_birthday = date(today.year, birth_date.month, birth_date.day)
    this_year_bday = date(today.year, birth_date.month, birth_date.day)
    send_mess += f'Следующий день рождения: {next_birthday}\n'

    # проверяем, был ли уже ДР в этом году. Если да, то плюсуем 1 к дате следующего ДР (фиксит)
    if today > this_year_bday:
        next_birthday = date(today.year + 1, birth_date.month, birth_date.day)

    # delta это остаток до следующего дня рождения
    delta = next_birthday - today

    if delta.days == 0:
        return 'ЭТО СЕГОДНЯ!!!'
    elif delta.days < 10:
        send_mess += f'Дней до следующего дня рождения: {delta.days}! Торопитесь с подарком!\n'
    else:
        send_mess += f'Дней до следующего дня рождения: {delta.days}\n'
    send_mess += '\n' \
                 'Еще? /b_day'

    return send_mess


