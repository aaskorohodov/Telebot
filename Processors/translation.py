import requests


def ru_eng(message):
    '''Готовит перевод, пакует его в строку и отдает эту строку. Работает на API от ABBYY'''

    # наш текст для перевода
    word = message.text

    # запрос для авторизации, для перевода, ключ авторизации и заголовки для HTTP-запроса. Все из инструкции ABBYY
    URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
    URL_TRANSLATE = 'https://developers.lingvolive.com/api/v1/Minicard'
    KEY = 'ODRlNGU0NDctOWU2ZS00ZTcxLTk5ZWYtNjI2ZTA0MzYwOGU3OmQwN2E5YjVhMDg2MjQwYTI5ZDU3NjA1Y2NiODI3ZjRj'
    headers_auth = {'Authorization': 'Basic ' + KEY}

    # выполняем авторизацию. Требуется передать запрос с определенными заголовками (POST-запрос)
    auth = requests.post(URL_AUTH, headers=headers_auth)

    if auth.status_code == 200:
        '''Если авторизация прошла успешно, то делаем запрос на перевод. Тут нужны другие заголовки, которые мы
        получаем в ответе на авторизацию'''

        token = auth.text
        headers_translate = {'Authorization': 'Bearer ' + token}

        # это словарь, который показывает что переводить, с какого языка и на какой (код языка с сайта ABBYY)
        params = {'text': word,
                  'srcLang': 1049,
                  'dstLang': 1033}

        # делаем запрос (get), извлекаем словарь, из него перевод
        r = requests.get(URL_TRANSLATE, headers=headers_translate, params=params)
        r = r.json()
        try:
            return r['Translation']['Translation']
        except:
            return 'Перевод не найден'

    else:
        return 'Сервис перевода сейчас недоступен. Попробуйте позднее'


def eng_ru(message):
    '''Полностью аналогичен описанию выше, кроме направления перевода'''
    word = message.text

    URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
    URL_TRANSLATE = 'https://developers.lingvolive.com/api/v1/Minicard'
    KEY = 'ODRlNGU0NDctOWU2ZS00ZTcxLTk5ZWYtNjI2ZTA0MzYwOGU3OmQwN2E5YjVhMDg2MjQwYTI5ZDU3NjA1Y2NiODI3ZjRj'

    headers_auth = {'Authorization': 'Basic ' + KEY}

    auth = requests.post(URL_AUTH, headers=headers_auth)

    if auth.status_code == 200:
        token = auth.text
        headers_translate = {'Authorization': 'Bearer ' + token}

        params = {'text': word,
                  'srcLang': 1033,
                  'dstLang': 1049}

        r = requests.get(URL_TRANSLATE, headers=headers_translate, params=params)
        r = r.json()
        try:
            return r['Translation']['Translation']
        except:
            return 'Перевод не найден'

    else:
        return 'Сервис перевода сейчас недоступен. Попробуйте позднее'