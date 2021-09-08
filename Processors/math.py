from Processors.user_recognition import user_recognition


def clean_num(text):
    alphabet = 'abcdefghijklmnopqrstuvwxyz\|/абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    num = ''
    for el in text:
        if el not in alphabet:
            num += el
    num = ''.join(num.split())
    try:
        num = float(num)
        return num
    except ValueError:
        return 0


def area(text):
    alphabet = 'abcdefghijklmnopqrstuvwxyz\|/абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    num = ''
    for el in text:
        if el not in alphabet:
            num += el
    num = num.split()
    if len(num) != 2:
        return 'Что-то не получается'
    else:
        res = str(float(num[0]) * float(num[1]))
        return res


def bmi(h, w):
    weight = clean_num(w)
    hight = clean_num(h)
    try:
        bmi = round(weight / ((hight / 100) ** 2), 1)
    except ZeroDivisionError:
        return 'Давай нормально. /bmi'
    bmi_res = f'Твой индекс массы тела: {str(bmi)}.\n' \
              f'\n'
    if bmi < 18.5:
        return bmi_res + 'ИМТ ниже 18.5 считается дифицитным. /food '
    elif bmi < 25:
        return bmi_res + 'ИМТ от 18,5 до 24,9 считается нормой. /food'
    else:
        return bmi_res + 'ИМТ выше 25 считается избыточным.'


def fib(message):
    name = user_recognition(message.from_user.id)
    c_num = ''
    alphabet = 'abcdefghijklmnopqrstuvwxyz\|/абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    for el in message.text:
        if el not in alphabet:
            c_num += el

    if int(c_num) == 0:
        return '0'

    try:
        c_num = int(c_num)
    except:
        return f'{name}, ты вводишь что-то не то\n' \
               f'/fib'

    one, two = 0, 1
    for i in range(c_num - 1):
        one, two = two, one + two
    return str(two)