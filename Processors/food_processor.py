import time
import telebot
import random
from telebot import types


bot = telebot.TeleBot('1879041775:AAG14Vz9P4AP4hjOGOOwYKbbFJGFSrWQEgs')


def food_handler(call):
    if call.data == 'self':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        markup = telebot.types.InlineKeyboardMarkup()
        fat = types.InlineKeyboardButton(text='Сытно', callback_data="fat")
        middle = types.InlineKeyboardButton(text='Средне', callback_data="middle")
        sweet = types.InlineKeyboardButton(text='Сладко', callback_data="sweet")
        markup.add(fat, middle, sweet)

        bot.send_message(call.message.chat.id, 'Тип еды', reply_markup=markup)


    elif call.data == 'fast':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        markup = telebot.types.InlineKeyboardMarkup()
        h_alot = types.InlineKeyboardButton(text='Побольше', callback_data="h_alot")
        h_low = types.InlineKeyboardButton(text='Поменьше', callback_data="h_low")
        markup.add(h_alot, h_low)

        bot.send_message(call.message.chat.id, 'Сколько хотите есть?', reply_markup=markup)


    elif call.data == 'h_alot':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        blin = 'Купите готовых блинов (не замороженных) с мясом.\n' \
               'К ним потребуется молоко.'
        pasta = 'Купите готовых макарон с чем-нибудь.\n' \
                'Не забудьте взять что-то попить.'
        bulki = 'Купите много булок или другой выпечки.\n' \
                'Например сосиску в тесте + пару сладких булок.\n' \
                'Вероятно вам потребуется еще и молоко.'
        tort = 'Купите торт, например сметанник. Сожрите целиком.\n' \
               'Не забудьте чем-то запить.'
        pechenie = 'Купите овсяного печенья, съешьте всю упаковку.\n' \
                   '*Молоко обязательно.'
        doshir = '3 больших доширирака или 4 мелких.'

        h_alot = [blin, pasta, bulki, tort, pechenie, doshir]
        res = random.choice(h_alot)
        bot.send_message(call.message.chat.id, res)
        time.sleep(5)
        bot.send_message(call.message.chat.id, 'Не годится? Попробуй еще: /food')


    elif call.data == 'h_low':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        bulka = 'Съеште булку или две.\n' \
                'Обязательно возьмите молока'
        prikoli = 'Наберите немного мелкой ерунды, например:\n' \
                  '– сырок\n' \
                  '– желе' \
                  '– твикс/сникерс/баунти\n' \
                  '– небольшое печенье\n' \
                  '– банан\n' \
                  '– ...'
        salat = 'Купите готовый салат.'
        krek = 'Купите крекер "нежный, который обычный, слегка соленый.\n' \
               'Купите сыр, положите на крекер.'
        tvorog = 'Купите творог со сгушенкой.'
        kasha = 'Купите готовую кашу (быстрого приготовления). Желательно заливать горячим молоком.'
        ice_cream = 'Возбмите морожку в стаканчике, но ешьте ее печенюгой или твиксом, как ложкой.'
        cereal = 'Возьмите хлопья или мюсли. Вам потребуется молоко.'
        h_low = [bulka, prikoli, salat, krek, tvorog, cereal, kasha, ice_cream]
        res = random.choice(h_low)
        bot.send_message(call.message.chat.id, res)
        time.sleep(5)
        bot.send_message(call.message.chat.id, 'Не годится? Попробуй еще: /food')




    elif call.data == 'fat':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        shav = 'шаурму. Вам понадобится:\n' \
               '– лепешка\n' \
               '– мясо (цельное или фарш)\n' \
               '– соус (майонез, кетчуп...)\n' \
               '– овощи (салат, кукуруза, оливки...)\n'
        pasta = 'макароны с грибами. Вам понадобится:\n' \
                '– макароны\n' \
                '– грибы\n' \
                '– соус'
        pelm = 'пельмени. Вам понадобится:\n' \
               '– пельмени\n' \
               '– соус\n' \
               '– специи, опционально (лавр, перец...)'
        blin = 'блины. Вам понадобится:\n' \
               '– молоко\n' \
               '– мука\n' \
               '– яйца\n' \
               '– начинка или сгушенка (или джем)\n' \
               '*начинкой может быть банан или другой фрукт, а также шоколад\n' \
               '– соль и сахар\n' \
               '\n' \
               'Классический рецепт. Кладем в емкость::\n' \
               '– 1/2 чайной ложки соли\n' \
               '– 2 столовые ложки сахара\n' \
               '– 200 грамм муки\n' \
               '– 3 яйца\n' \
               '– 2 столовые ложки малса (любого)\n' \
               '– 50 грамм (примерно 70 мл) молока\n' \
               '\n' \
               'Взбиваем. Так как вы положиле мало молока, тесто выйдет густым, зато комочков практически не будет, ' \
               'даже если взбивать не долго и вручную.\n' \
               '\n' \
               'Теперь добавьте еще 200 грамм (большой стакан) молока. Если второй блин получился слишком толстым, ' \
               'можно долить еще молока, на такой вес муки (200 грамм) можно лить до 700 мл.'
        salat = 'салат. Много салата. Вот пример относительно легкого:\n' \
                '– 2 огурца (1 огромный, который китайский)\n' \
                '– пару помидор (можно 1 огромный)\n' \
                '– кукуруза (1 банка)\n' \
                '– оливки (1 банка)\n' \
                '– соленый оргурцы\n' \
                '– свежие грибы (шампиньоны)\n' \
                '– масло и соевый соус\n' \
                '\n' \
                'Опционально можно класть специи или готовую заправку (масло со специями).\n' \
                'Резать треубется максимально мелкими кусками (сколько хватит упорства, вплоть до кусков размером ' \
                'с ноготь.\n' \
                'После нарежки, кладите все в емкость, обильно заливайте растительным маслом, уверенно солите (до 1 ' \
                'чайной ложки), подливайте лимонный сок (можно выжать лимон), по желанию перчите, добавляйте соевый ' \
                'соус.\n' \
                '\n' \
                '*обратие внимание, что соевый соус соленый, аккуратно сочетайте его с солью – либо то, либо другое.'
        rise = 'Сделайте рис с овощами. Вам потребуется:\n' \
               '– рис\n' \
               '– огурец\n' \
               '– помидор\n' \
               '– кукуруза\n' \
               '– опционально что-то еще из овощей\n' \
               '– опционально грибы\n' \
               '– соевый соус\n' \
               '– приправы и специи по желанию\n' \
               '\n' \
               'Пока варится рис, нарежте очень мелкими кусками овощи. Рис желательно пропаренный и варить до ' \
               '""Аль-данте". Когда рис готов, скидайте в него овощи и грибы (если вы их взяли), грибы сырыми. ' \
               'Обильно полейте малсом и добавьте соевый соус по вкусу. Можно предварительно влить масло в овощи, ' \
               'а соевый соус в рис, а затем смешивать.'
        fat_food = [shav, pasta, pelm, blin, salat, rise]
        res = random.choice(fat_food)
        bot.send_message(call.message.chat.id, f'Сделайте {res}')
        time.sleep(5)
        bot.send_message(call.message.chat.id, 'Не годится? Попробуй еще: /food')


    elif call.data == 'middle':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        fruit_salad = 'Сделайте фруктовый салат. Просто возьмите фруктов, какие имеются и подходят друг к другу, ' \
                      'порежьте все на "куски по 1 укусу" и ешьте.'
        grech = 'Сделайте гречу с молоком. Просто отварите гречу и налейте молока, как в хлопья.'
        kasha = 'Сварите кашу, например рисовую на молоке. Вы можете добавить в нее сухофруктов, орехов или\и ' \
                'свежих фруктов, например банан или яблоко.'
        soba = 'Гречневая лапша с овощами. Вам потребуется:\n' \
               '– соба\n' \
               '– морковь\n' \
               '– опционально другие овощи, например огурец и помидор\n' \
               '– кунжут\n' \
               '– соевый соус\n' \
               '– опционально другой соу\n' \
               '*учтите, что майонез резко превратит это блюдо в тяжелое!\n' \
               '\n' \
               'Сварите собу, обратите внимание, что она варится очень быстро (3 минуты), а также уже содержит соль. ' \
               '\n' \
               'Нарежте морковь длинными и мелкими ломтиками, аналогично поступите с другие овощи (если есть), ' \
               'положите на горячую сковороду, добавьте соевый соус и масло. Жарьте около 2 - 5 минут.' \
               '\n' \
               'Положите в тарелку собу, сверху сложите овощи, обильно посыпьте все кунжутом.'

        middle_food = [fruit_salad, grech, kasha, soba]
        res = random.choice(middle_food)
        bot.send_message(call.message.chat.id, res)
        time.sleep(5)
        bot.send_message(call.message.chat.id, 'Не годится? Попробуй еще: /food')


    elif call.data == 'sweet':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        banana_split = 'Банан с мороженным. Просто возьмите пломбир (здоровый) и покладите туда банан.'
        ice_cream_fruit = 'Возьмите персиков в банке или ананас в ней же и пломбир (большой).'
        blin = 'Возьмите готовых блинов и складывайте в них фрукты, сгушенку или шоколад.'
        creck_cake = 'Сделайте сметанный торт из крекеров с бананом. Вам потребуются:\n' \
                     '– крекер "нежный" (1 - 2 пачки)\n' \
                     '– бананы (3 - 5 штук)\n' \
                     '– сметана (0.5 литра)\n' \
                     '– сахар\n' \
                     '\n' \
                     'Смешивайте сметану с сахаром по вкусу (должно быть сладко). Режте банан на кружки. ' \
                     'В большую емкость кладите пищевую пленку (если есть), сверху слой бананов, затем слой крекеров, ' \
                     'затем сладкую сметану. Повторите, пока есть ингредиенты. Поставьте все в холодильник минимум на ' \
                     '5 часов, желательно на сутки. Чем дольше стоит, там мягче становится.\n' \
                     '\n' \
                     'Будте аккуратны, извлекая изделие из кострюли, особенно если не положили пленку.'
        sweet_food = [banana_split, ice_cream_fruit, blin, creck_cake]
        res = random.choice(sweet_food)
        bot.send_message(call.message.chat.id, res)
        time.sleep(5)
        bot.send_message(call.message.chat.id, 'Не годится? Попробуй еще: /food')


    elif call.data == 'outdoor':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        markup = telebot.types.InlineKeyboardMarkup()
        map_self = types.InlineKeyboardButton(text='Сам выберу', callback_data="map_self")
        sovet = types.InlineKeyboardButton(text='Посоветуйте', callback_data="sovet")
        markup.add(map_self, sovet)

        bot.send_message(call.message.chat.id, 'Куда хотите сходить?', reply_markup=markup)


    elif call.data == 'map_self':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'https://www.google.com/maps/search/%D0%B5%D0%B4%D0%B0')


    elif call.data == 'sovet':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        markup = telebot.types.InlineKeyboardMarkup()
        shit = types.InlineKeyboardButton(text='Фаст-фуд', callback_data="shit")
        street = types.InlineKeyboardButton(text='Стрит-фуд', callback_data="street")
        restorant = types.InlineKeyboardButton(text='Я = элита!', callback_data="restorant")
        markup.add(shit, street, restorant)

        bot.send_message(call.message.chat.id, 'Куда идем?', reply_markup=markup)


    elif call.data == 'shit':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'www.google.com/maps/search/фастфуд')


    elif call.data == 'street':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'https://www.google.com/maps/search/%D0%95%D0%B4%D0%B0+%D0%BD%D0%B0%D0%B2%D1%8B%D0%BD%D0%BE%D1%81')


    elif call.data == 'restorant':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'https://www.google.com/maps/search/%D0%A0%D0%B5%D1%81%D1%82%D0%BE%D1%80%D0%B0%D0%BD%D1%8B/data=!4m5!2m4!5m2!2e1!4e9!6e5')