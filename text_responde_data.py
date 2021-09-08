import pickle
import random


def dict_creation():
    file = open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\answer_databse4.txt', 'r', encoding='UTF8')


    my_dict = {}

    for line in file:
        line = line.lower()

        line_clean = ''
        for el in line:
            alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя abcdefghijklmnopqrstuvwxyz1234567890/?,.!'
            if el in alphabet:
                line_clean += el

        line = line_clean
        line = line.split(r'/')
        line = line[0:2]
        if line[0] in my_dict:
            try:
                rand = random.random()
                key = str(f'{line[0]} {rand}')
                my_dict[key] = line[1]
            except:
                pass

        elif line[0] not in my_dict:
            try:
                my_dict[line[0]] = line[1]
            except:
                pass

    print(len(my_dict))

    with open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\answer_databse4_dict', 'wb') as file:
        pickle.dump(my_dict, file)


dict_creation()



def dict_creation2():
    file = open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\answer_databse3.txt', 'r', encoding='UTF8')


    my_dict = {}

    for line in file:
        line = line.lower()

        line_clean = ''
        for el in line:
            alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя abcdefghijklmnopqrstuvwxyz1234567890/?,.!'
            if el in alphabet:
                line_clean += el

        line = line_clean
        line = line.split(r'/')

        try:
            answer = line[1]
            if answer == '':
                pass
            else:
                if line[0] in my_dict:
                    try:
                        rand = random.random()
                        key = str(f'{line[0]} {rand}')
                        my_dict[key] = line[1]
                    except IndexError:
                        pass

                elif line[0] not in my_dict:
                    try:
                        my_dict[line[0]] = line[1]
                    except IndexError:
                        pass
        except:
            pass



    with open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\answer_databse3_dict', 'wb') as file:
        pickle.dump(my_dict, file)





def dict_merging():
    #with open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\answer_databse2_dict', 'wb') as file:
    #    pickle.dump(my_dict, file)

    with open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\mega_dict', 'rb') as file:
        dat3_dict = pickle.load(file)

    with open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\answer_databse4_dict', 'rb') as file:
        dat4_dict = pickle.load(file)

    print(len(dat3_dict))
    print(len(dat4_dict))

    for k, v in dat3_dict.items():
        if k in dat4_dict:
            add = f'{k} {random.random()}'
            dat4_dict[add] = v
        else:
            dat4_dict[k] = v

    print(len(dat4_dict))

    with open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\mega_dict', 'wb') as file:
        pickle.dump(dat4_dict, file)


dict_merging()


with open('C:\\Users\\Аркадий\\Pictures\\py\\Deeper_responde\\mega_dict', 'rb') as file:
    mega_dict = pickle.load(file)

    print(len(mega_dict))
    print(type(mega_dict))