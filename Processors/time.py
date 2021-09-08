import requests


def time(city) -> dict:
    return requests.get(f'http://api.weatherapi.com/v1/timezone.json?key=fae526c9c9d24b1f8d6170008210608&q={city}').json()


def output(city):
    all = time(city)
    try:
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