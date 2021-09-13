def wf(city):
    '''Добывает словарь с данными о погоде'''
    import requests
    return requests.get(f'https://api.weatherapi.com/v1/forecast.json?key=fae526c9c9d24b1f8d6170008210608&q={city}&days=3&lang=ru&aqi=no&alerts=no').json()


def date_translation(forecast_date):
    '''Переписывает не самую красивую дату из данных API. Создает из изначальной даты список, затем меняет день и месяц
    в самом себе (в списке) используя два словаря ниже (в словарях ключ = как было, значение = как надо), затем список
    преобразуется обратно в строку'''
    b = list(forecast_date.split('-'))

    num_to_month = {'01': 'января',
                    '02': 'февраля',
                    '03': 'марта',
                    '04': 'апреля',
                    '05': 'мая',
                    '06': 'июня',
                    '07': 'июля',
                    '08': 'августа',
                    '09': 'сентября',
                    '10': 'октября',
                    '11': 'ноября',
                    '12': 'декабря'
                    }

    correct_day = {'01': '1',
                   '02': '2',
                   '03': '3',
                   '04': '4',
                   '05': '5',
                   '06': '6',
                   '07': '7',
                   '08': '8',
                   '09': '9',
                   '10': '10',
                   '11': '11',
                   '12': '12',
                   '13': '13',
                   '14': '14',
                   '15': '15',
                   '16': '16',
                   '17': '17',
                   '18': '18',
                   '19': '19',
                   '20': '20',
                   '21': '21',
                   '22': '22',
                   '23': '23',
                   '24': '24',
                   '25': '25',
                   '26': '26',
                   '27': '27',
                   '28': '28',
                   '29': '29',
                   '30': '30',
                   '31': '31',
                   }

    c = f'{correct_day[b[2]]} {num_to_month[b[1]]}'
    return c


def wf_output(city):
    '''Добывает погоду'''

    try:
        '''try на случай неверного названия города. Далее в разные переменные кладем нужные строки, чтобы потом собрать
        ответ в одну строку'''

        data = wf(city)  # получаем словарь

        location = f"{data['location']['name']}, {data['location']['country']}"  # это название города + область\штат\..

        # блок ниже представляет погоду на сегодня. Тут выше детальность
        cloud_perc_current = data['current']['cloud']
        text_current = data['current']['condition']['text']
        humidity_current = data['current']['humidity']
        is_day_current = data['current']['is_day']
        temp_current = data['current']['temp_c']
        wind_speed = data['current']['wind_kph']

        # каждый из блоков ниже представляет прогноз на 1 сутки вперед
        forecast1_date = data['forecast']['forecastday'][0]['date']
        forecast1_humidity = data['forecast']['forecastday'][0]['day']['avghumidity']
        forecast1_text = data['forecast']['forecastday'][0]['day']['condition']['text']
        forecast1_rain_chance = data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
        forecast1_max_t = data['forecast']['forecastday'][0]['day']['maxtemp_c']
        forecast1_min_t = data['forecast']['forecastday'][0]['day']['mintemp_c']

        forecast2_date = data['forecast']['forecastday'][1]['date']
        forecast2_humidity = data['forecast']['forecastday'][1]['day']['avghumidity']
        forecast2_text = data['forecast']['forecastday'][1]['day']['condition']['text']
        forecast2_rain_chance = data['forecast']['forecastday'][1]['day']['daily_chance_of_rain']
        forecast2_max_t = data['forecast']['forecastday'][1]['day']['maxtemp_c']
        forecast2_min_t = data['forecast']['forecastday'][1]['day']['mintemp_c']

        forecast3_date = data['forecast']['forecastday'][2]['date']
        forecast3_humidity = data['forecast']['forecastday'][2]['day']['avghumidity']
        forecast3_text = data['forecast']['forecastday'][2]['day']['condition']['text']
        forecast3_rain_chance = data['forecast']['forecastday'][2]['day']['daily_chance_of_rain']
        forecast3_max_t = data['forecast']['forecastday'][2]['day']['maxtemp_c']
        forecast3_min_t = data['forecast']['forecastday'][2]['day']['mintemp_c']

        # блок if проверяет одно из значений словаря, чтобы определить, село ли солнце. Немного меняет ответ
        if is_day_current == 1:
            is_day = 'солнце над горизонтом.'
        else:
            is_day = 'солнце село, луна в небе.'

        # обращается к функции (чуть выше), чтобы переписать дату покрасывше
        day1 = date_translation(forecast1_date)
        day2 = date_translation(forecast2_date)
        day3 = date_translation(forecast3_date)

        # далее готовится красивый ответ
        return (f'{location}\n'
                f'\n'
                f'Сейчас {text_current.lower()}, {is_day}\n'
                f'Температура: {temp_current}C\n'
                f'Облачность: {cloud_perc_current}%\n'
                f'Влажность: {humidity_current}%\n'
                f'Скорость ветра: {wind_speed} км/ч\n'
                f'\n'
                f'{day1} будет {forecast1_text.lower()}\n'
                f'Температура: {forecast1_max_t} днем, {forecast1_min_t} ночью\n'
                f'Вероятность осадков: {forecast1_rain_chance}%\n'
                f'Влажность: {forecast1_humidity}\n'
                f'\n'
                f'{day2} будет {forecast2_text.lower()}\n'
                f'Температура: {forecast2_max_t} днем, {forecast2_min_t} ночью\n'
                f'Вероятность осадков: {forecast2_rain_chance}%\n'
                f'Влажность: {forecast2_humidity}\n'
                f'\n'
                f'{day3} будет {forecast3_text.lower()}\n'
                f'Температура: {forecast3_max_t} днем, {forecast3_min_t} ночью\n'
                f'Вероятность осадков: {forecast3_rain_chance}%\n'
                f'Влажность: {forecast3_humidity}\n'
                )

    except KeyError:
        '''Сценарий неверного города. API вернет другой словарь (а может пустой) так что по некоторым ключам в нем 
        будет пусто, вылезет ошибка. Ее и ловим.'''

        return (f'Не вижу такого города на этой планете.\n'
                f'Попробуй еще раз /weather')