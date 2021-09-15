from Processors.user_recognition import user_recognition


def clean_num(text):
    '''Очищает строку от символов, оставляя только цифры'''

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
    '''Считает площадь прямоугольника'''

    # символы, которые нужно убрать из переданного текста (если они есть)
    alphabet = 'abcdefghijklmnopqrstuvwxyz\|/абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    # сюда запишем то, что осталось (это должно стать сторонами прямоугольника)
    num = ''

    for el in text:
        if el not in alphabet:
            num += el

    num = num.split()
    if len(num) != 2:
        return 'Что-то не получается'

    else:
        try:
            res = str(float(num[0]) * float(num[1]))
        except:
            res = 'Что-то не то'

        return res


def bmi(h, w):
    '''Считает массу тела. Дает слегка разный ответ'''

    # очищаем переданный вес и рост от возможных букв
    weight = clean_num(w)
    hight = clean_num(h)

    # пробуем посчитать индекс, округляем результат
    try:
        bmi = round(weight / ((hight / 100) ** 2), 1)
    except ZeroDivisionError:
        return 'Давай нормально. /bmi'

    # шаблон ответа
    bmi_res = f'Твой индекс массы тела: {str(bmi)}.\n' \
              f'\n'

    # добавляем к шаблону разный кусок, в зависимости от получившегояс BMI

    if bmi < 18.5:
        return bmi_res + 'ИМТ ниже 18.5 считается дифицитным. /food '
    elif bmi < 25:
        return bmi_res + 'ИМТ от 18,5 до 24,9 считается нормой. /food'
    else:
        return bmi_res + 'ИМТ выше 25 считается избыточным.'


def fib(message):
    '''Считает фибоначчи. Предварительно чистить полученное сообщение от возможных лишних символов. name нужен
    для персонального ответа'''

    name = user_recognition(message.from_user.id)
    c_num = ''
    alphabet = 'abcdefghijklmnopqrstuvwxyz\|/абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    # чистим сообщение
    for el in message.text:
        if el not in alphabet:
            c_num += el

    # пробуем сделать из сообщения число
    try:
        c_num = int(c_num)
    except:
        return f'{name}, ты вводишь что-то не то\n' \
               f'/fib'

    # проверяем, что в сообщении не 0
    if int(c_num) == 0:
        return '0'

    # считаем число фибоначчи
    one, two = 0, 1
    for i in range(c_num - 1):
        one, two = two, one + two

    return str(two)