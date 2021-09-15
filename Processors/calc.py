def calc(text):
    '''Очень простой калькулятор. Работает на встроенном eval, который пытается превратить переданную строку в
    выражение.'''
    try:
        result = eval(text)
        return result

    except ZeroDivisionError:
        return ('0')

    except NameError:
        return (f'"{text}" не выражеие, я не могу такое посчитать\n'
               f'Чтобы закрыть калькулятор, напишите "все"')

    except SyntaxError:
        return (f'"{text}" не выражеие, я не могу такое посчитать\n'
                f'Чтобы закрыть калькулятор, напишите "все"')