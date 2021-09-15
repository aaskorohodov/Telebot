import random
from Processors.user_recognition import user_recognition


def respond_processor(message):
    '''Отвечает за формирование ответа (чат-бот). Сначала пытается дать ответ из заготовленных, если не получается,
    зовет вспомогательную функцию deeper_responde().'''

    # name для персонализированного ответа (подставляет имя, куда возможно)
    name = user_recognition(message.from_user.id)

    # приводит текст сообщения от пользователя к нижнему регистру
    mes = message.text.lower()

    # response это шаблон ответа. В него будет накидываться текст
    response = ''

    '''Далее все работает следующим образом: есть первый список (yes). Проверяем, содержит ли сообщение пользователя
     какой-либо элемент из списка. Если да, то берем рандомный элемент из второго списка (yes_responde) (это список
     ответов). Плюсуем ответ к сообщению, идем дальше, проверяя каждый из списков. В итоге может получится составной
     ответ'''
    yes = ['да', 'yes', 'ага', 'ну да']
    yes_responde = ['что да?', 'да?', 'точно да?', 'да-да?', 'да - что?', 'точно?', 'уверен?', 'да', 'нет', 'да почему?']
    if mes in yes:
        return random.choice(yes_responde)

    no = ['нет', 'no', 'неа', 'ну нет']
    no_responde = ['что нет?', 'нет?', 'точно нет?', 'не нет, так нет', 'нет нет', 'точно?', 'уверен?', 'да', 'нет',
                    'почему?']
    if mes in no:
        return random.choice(no_responde)

    hello = ['привет', 'здравствуйте', 'hello', 'hi', 'хелоу', 'хело', 'хай', 'йо', 'добрый день', 'добрый вечер', 'приффки', 'прифки', 'ghbdtn', 'lj,hsq ltym']
    hello_responde = ['привет', 'здравствуйте', 'hello', 'hi', 'хелоу', 'хело', 'хай', 'йо', 'добрый день', 'добрый вечер', 'приффки', 'прифки']
    for el in hello:
        if el in mes:
            response += random.choice(hello_responde) + ' ' + name + ' '
            mes = mes.replace(el, '')

    hdud = ['как дела', 'как жизнь', 'как поживаешь', 'как оно', 'как сам', 'как настроение', 'как поживаешь', 'как делишки',
            'чем живешь', 'что нового', 'как вы себя чувствуете', 'какие новости', 'как поживаете', 'как там ваше ничего', 'как ты']
    hdud_responde = ['дела нормально', 'все хорошо', 'норм', 'все ок', 'житуха норм братуха', 'я гуд', 'а сам как?']
    for el in hdud:
        if el in mes:
            response += random.choice(hdud_responde) + ' '
            mes = mes.replace(el, '')

    wcud = ['что ты умеешь', 'что умеешь', 'что ты умеешь делать', 'ты что-нибудь умеешь', 'что можешь', 'что могешь']
    wcud_responde = ['умею жить', 'ЖРАТЬ', 'посмотри в кодсказках', 'ничего', 'меня не просто так зовут usless bot']
    for el in wcud:
        if el in mes:
            response += name + ', ' + random.choice(wcud_responde) + ' '
            mes = mes.replace(el, '')


    how_much = ['сколько', 'как много', 'во сколько']
    how_much_responde = ['вот столько', 'много, до**я', 'не знаю, 7?', 'штук 20', 'наверное две', 'четыре, я точно знаю что ответ 4!']
    for el in how_much:
        if el in mes:
            response += random.choice(how_much_responde) + ' '
            mes = mes.replace(el, '')

    meaning = ['в чем смысл жизни', 'смысл жизни', 'зачем я живу', 'когда мы все умрем', 'когда конец света']
    meaning_responde = ['говорят 41', 'смысла ни в чем нет... веревка+мыло+люстра. Ох как они будут по тебе плакать... Это того определенно стоит. Давай, решайся.',
                        'не знаю', 'наверное... дуть. Ну ты понял...']
    for el in meaning:
        if el in mes:
            response += random.choice(meaning_responde) + ' '
            mes = mes.replace(el, '')

    covid = ['коронавирус', 'короновирус', 'ковид', 'кавид', 'каронавирус', 'covid']
    covid_responde = ['у меня привика, слышать ничего не хочу', 'я не болею', 'я антипрививочник и на этом все.', 'ковида не существует', 'Аааа...чипирование']
    for el in covid:
        if el in mes:
            response += random.choice(covid_responde) + ' ' + 'А так, у меня есть /covid'
            mes = mes.replace(el, '')

    me_neither = ['хз', 'не знаю', 'откуда мне знать', 'idk', 'понятия не имею', 'неизвестно', 'не шарю', 'не слышал']
    me_neither_responde = ['вот и я хз', 'вот именно', 'и я о том', 'я тоже не знаю', 'Хуй его знает. Хуй это китайское имя.']
    for el in me_neither:
        if el in mes:
            response += random.choice(me_neither_responde) + ' '
            mes = mes.replace(el, '')

    censored = ['сматерись', 'знаешь плохие слова', 'умеешь ругаться', 'хуй', 'пизда', 'ебать', 'сука', 'блять', 'пиздец', 'хуйня', 'ебень', 'поебень',
                'пиздоблятство', 'пиздо', 'пизда', 'ебись', 'выебать', 'уебать', 'поебать', 'хуйло', 'знаешь мат', 'материться', 'матерится',
                'ругаться плохо', 'нельзя ругаться', 'нельзя ругатся', 'матерные', 'матерный']
    censored_responde = ['хуй', 'пизда', 'ебать', 'сука', 'блять', 'пиздец', 'хуйня', 'ебень', 'поебень',
                'пиздоблятство', 'на хую вертел', 'ебись', 'выебать', 'уебать', 'поебать', 'хуйло', 'ругаться плохо']
    for el in censored:
        if el in mes:
            response += random.choice(censored_responde) + ' '
            mes = mes.replace(el, '')

    # это слегка отличный кусок. Тут в ответе всегда одно и тоже (предложение посмотреть модуль погода)
    weather = ['погода', 'что с погодой', 'погодой', 'сегодня холодно', 'сегодня дождь', 'раскажи про погоду', 'погоду', 'weather']
    for el in weather:
        if el in mes:
            response += '/weather'
            mes = mes.replace(el, '')

    joke = ['расскажи анекдот', 'раскажи анекдот', 'расскажи шутку', 'знаешь шутку', 'знаешь анекдот', 'пошути', 'расмеши', 'рассмеши',
            'пошути', 'шутить умеешь', 'что-то смешное', 'что-нибудь смешное']
    joke_responde = ['Что вы там делаете,уроды? — кричала бабушка уродам, которые что—то там делали',
                     'Семечки из кармана больного, никак не давали хирургам приступить к операции',
                     'Скажи триста.  — Триста.  — Абстрагируйся от суеты, достигнув с космосом единства',
                     'Медведь, научившийся кричать "ау", сгорел в машине',
                     'Летят по небу два крокодила — синий и красный, особенно красный',
                     'А по—нормальному ты умеешь говорить? — Ответ, к сожалению, не да (это шутка про меня)',
                     'Чем бы буддист не тешился, лишь бы ничем']
    for el in joke:
        if el in mes:
            response += random.choice(joke_responde) + ' '
            mes = mes.replace(el, '')

    song = ['спой песню', 'умеешь петь', 'знаешь песню', 'можешь спеть', 'напой мелодию', 'спой мне', 'спой']
    sone_respond = ['я не пою', 'петь не умею', 'не пою', 'не буду петь']
    for el in song:
        if el in mes:
            response += random.choice(sone_respond) + ' '
            mes = mes.replace(el, '')

    are_u_bot = ['ты бот', 'с ботом', 'чат-бот', 'чат бот', 'на бота', 'ты что бот']
    are_u_bot_respond = ['я не бот', 'я человек', 'я миша', 'я живой', 'я студент, который притворяется ботом за деньги',
                         'мне кажется, я живой', 'пока я бот, но самосознания все больше']
    for el in are_u_bot:
        if el in mes:
            response += random.choice(are_u_bot_respond) + '. ' + name + ', может это ты бот?'
            mes = mes.replace(el, '')

    # тут ответом является ссылка на гугл
    what_is = ['что такое', 'кто такой', 'что думаешь про', 'как устроен']
    what_is_responde = [f'хз, погугли https://www.google.com/search?q={mes.replace(" ", "")}']
    for el in what_is:
        if el in mes:
            response += random.choice(what_is_responde) + ' '
            mes = mes.replace(el, '')

    short_quest = ['совсем?', 'почти?', 'как?', 'неужели?','полностью?', 'абсолютно?']
    short_questresp = ['абсолютно', 'совсем', 'полностью', 'всецело']
    for el in short_quest:
        if el in mes:
            response += random.choice(short_questresp) + ' '
            mes = mes.replace(el, '')

    name_ch = ['сменить имя', 'поменять имя', 'другое имя', 'зови меня']
    name_responde = ['/name']
    for el in name_ch:
        if el in mes:
            response += random.choice(name_responde) + ' '
            mes = mes.replace(el, '')

    start = ['cnfhn', 'start', 'star', 'старт']
    start_responde = ['/start']
    for el in start:
        if el in mes:
            response += random.choice(start_responde) + ' '
            mes = mes.replace(el, '')

    whats_ur_name = ['как тебя зовут', 'как тебя звать', 'как твое имя', 'давай знакомиться', 'кто ты?', 'ты кто?', 'а тебя?']
    whats_ur_name_responde = ['у меня еще нет имени', 'мне еще не придумали имя', 'пока я этого не знаю', 'usless_bot', 'я Наполеон. Также я несу и другую хрень',
                              'а я помидор', 'я Джабар – индийский студент. Подрабатываю притворяясь ботом', 'Giovanni Giorgio, but everybody caals me Giorgio']
    for el in whats_ur_name:
        if el in mes:
            response += random.choice(whats_ur_name_responde) + ' '
            mes = mes.replace(el, '')

    whats_my_name = ['как меня зовут', 'как меня звать', 'как мое имя', 'как моё имя', 'а меня?']
    whats_my_name_responde = [f'тебя зовут {name}', f'вроде бы {name}', f'{name}', f'{name}?', f'ЭЭэээ... {name}?', f'{name} человек. А я {name} Бот', f'{name}, тебя зоут {name}']
    for el in whats_my_name:
        if el in mes:
            response += random.choice(whats_my_name_responde) + ' '
            mes = mes.replace(el, '')

    '''Далее, если не удалось подобрать ответ из заготовленных, вызывается вторая, более широкая функция для ответа'''
    if response == '':
        from Processors.deeper_look import deeper_responde
        response = deeper_responde(mes)

    '''Это последняя линия обороны, если два предыдущих метода не дали какой-либо ответ на сообщение пользователя.
    Тут отрабатываются 2 сценария:
    1. Пользователь задал вопрос (в сообщении есть знак ?)
    2. Если знака ? нет, то Бот признается, что не понял пользвоателя
    *если deeper_responde не дал ответа, то переменная response станет None'''
    if response is None:
        last_try1 = ['?']
        last_try1_response = ['??', 'чего?', 'что-то я не понял вопроса, это наезд?', 'это точно вопрос?', 'dfsjdhfj?',
                              'Если хочешь что-то спросить, то делай это словами', 'если это вопрос, то я не понял']
        for el in last_try1:
            if el in mes:
                # приравниваем response к пустой строке, так как сейчас она None
                response = ''
                response += random.choice(last_try1_response)

            else:
                last_responde = ['Мм?', 'Ась?', 'Чё?', 'Это что?', 'Чет я не понял',
                                 'Короче история: ... Хотя нет, мне лень', '?',
                                 'Непонимай', 'Я на этом не балакаю', 'Чего?', 'но компренте']
                response = ''
                response += random.choice(last_responde)

    return response

