import datetime


def log(user_mess, name='user', bot_mess=' '):
    try:
        f = open(r'C:\Users\Аркадий\Pictures\py\123123.txt', 'a')
        time = datetime.datetime.now()

        f.write(f'\n'
                f'{time}\n'
                f'{name}: {user_mess}\n'
                f'BOT: {bot_mess}\n'
                f'\n')
    except:
        pass
