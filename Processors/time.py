import requests


def time(city) -> dict:  # это аннотация, она ничего не делает, но сообщает (тебе) что эта функция вернет словарь
    '''Запрос к какому-то API, добываем время, передаем город в http'''

    return requests.get(f'http://api.weatherapi.com/v1/timezone.json?key=fae526c9c9d24b1f8d6170008210608&q={city}').json()


def output(city):
    '''Собирает из полученного словаря (из API, выше) нужные данные, кладет в красивую строку, отдает строку'''

    all = time(city)  # all = словарь, где лежит все, что отдало API (там очень много всего)

    try:
        '''Пытаемся положит в каждую переменную свои данные из словаря'''

        loc = all['location']
        time_now = loc['localtime']
        country = loc['country']
        region = loc['region']
        city = loc['name']

        return (f'Текущая дата и время: {time_now}\n'
                f'\n'
                f'Город: {city}\n'
                f'Регион\область: {region}\n'
                f'Страна: {country}')

    except KeyError:
        return ('Нет такого города. Что с правописанием?')