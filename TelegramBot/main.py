import pymysql # pip
import telebot # pip
from telebot import types
from config import host, user, password, db_name
from bs4 import BeautifulSoup
import requests
from parsing import (napravlen_fizika, napravlen_prib, napravlen_prin, napravlen_ivt, proxodnie,clear_BD)

connection = pymysql.connect(
    host=host,
    port=3306,
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)

bot = telebot.TeleBot('5501105221:AAEkK71ojHlKzAKU1GzO-iG3u9hSH38aK4M')

# Команда прасинга
time = 1
@bot.message_handler(commands=['parse21'])
def parse_common(message):
   bot.send_message(message.chat.id, 'Идёт парсинг данных...')
   global time
   if time == 1:
       time = 0
       clear_BD()
       napravlen_fizika()
       napravlen_prib()
       napravlen_prin()
       napravlen_ivt()
       proxodnie()

       bot.send_message(message.chat.id, 'Данные обновлены')
       time = 1




@bot.message_handler(commands=['start'])
def start(message):
   bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}, я бот для абитуриента')
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
   fizika = types.KeyboardButton('Физика')
   ivt = types.KeyboardButton('Информатика и вычислительная техника')
   prog = types.KeyboardButton('Программная инженерия')
   prib = types.KeyboardButton('Приборостроение')
   markup.add(fizika, ivt, prog, prib)
   bot.send_message(message.chat.id, 'Я расскажу вам о направления ФЭВТ, а также покажу рейтинг дургих абитуриентов', reply_markup=markup)
   bot.send_message(message.chat.id, 'Выберите направление')


def main(message):  # Главное меню
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
   fizika = types.KeyboardButton('Физика')
   ivt = types.KeyboardButton('Информатика и вычислительная техника')
   prog = types.KeyboardButton('Программная инженерия')
   prib = types.KeyboardButton('Приборостроение')
   markup.add(fizika, ivt, prog, prib)
   bot.send_message(message.chat.id, 'Главное меню', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text(message):
   if message.text != 'В главное меню' and message.text != 'Физика' and message.text != 'Информатика и вычислительная техника'\
           and message.text != 'Программная инженерия' and message.text != 'Приборостроение'\
           and message.text != 'Записаться на напрвление Физика'  \
           and message.text != 'Профильный предмет - Физика' and message.text != 'Профильный предмет - Информатика'\
           and message.text != 'Профильный предмет - Информатика' and message.text != 'Профильный предмет - Английский язык'\
           and message.text != 'Наличие красного аттестата(+10 балов)' and message.text != 'Наличие знака отличия ГТО (+3 балла)' and message.text != 'Нет'\
           and message.text != 'Записаться на направление Информатика и вычислительная техника' and message.text != 'Записаться на направление Программная инженерия' and message.text != 'Записаться на направление Физика' and message.text != 'Записаться на направление Приборостроение':
           bot.send_message(message.chat.id, 'Я вас не понимаю, воспользуйтесь кнопками')

# Тут дописать с другими направлениями


   if message.text == 'В главное меню':
       main(message)
       bot.send_message(message.chat.id, 'Выберите направление')

   # Функиця вывода (после нет или после вычисления в да)
   def noo(message):
       if message.text != 'Узнать результаты' and message.text != 'В главное меню':
           msg = bot.send_message(message.chat.id, 'Я вас не понимаю, воспользуйтесь кнопками')
           bot.register_next_step_handler(msg, noo)

       if message.text == 'В главное меню':
           main(message)
           bot.send_message(message.chat.id, 'Выберите направление')

       if napr == 1 and message.text == 'Узнать результаты':
           markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
           back = types.KeyboardButton('В главное меню')
           markup.add(back)

           if message.text == '/start':
               start(message)
               return

           if message.text == '/parse21':
               parse_common(message)
               main(message)
               return

           if message.text == 'В главное меню':  # Выход в главное меню
               main(message)
               bot.send_message(message.chat.id, 'Выберите направление')
               return

           if message.text == 'Узнать результаты':
               with connection.cursor() as cursor:
                   select = 'select first_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   first = cursor.fetchall()
                   first1 = str(first).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select second_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   second = cursor.fetchall()
                   second2 = str(second).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select third_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   thrid = cursor.fetchall()
                   thrid2 = str(thrid).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select ind_doc from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   ind = cursor.fetchall()
                   ind2 = str(ind).split(' ')[-1].split('}')[0]
                   if ind2 == 'None':
                       ind2 = 0

               try:
                   rez = int(first1) + int(second2) + int(thrid2) + int(ind2)
               except:
                   pass


           bot.send_message(message.chat.id, 'Ваши баллы : ' + str(rez), reply_markup=markup)

           with connection.cursor() as cursor:
               proxodnie_fizika = 'select rait from proxodnie where `name` = \' Физика\';'
               cursor.execute(proxodnie_fizika)
               prox_fizika = cursor.fetchall()

           prox = str(prox_fizika).split(' ')[-1].split('}')[0]
           bot.send_message(message.chat.id, 'В прошлом году на это направление проходной балл был ' + str(prox),
                            reply_markup=markup)

           try:
               with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
                   update = 'insert into napravlen(uid, raitring,`name`) value(' + str(message.from_user.id) + ',' + str(
                       int(first1) + int(second2) + int(thrid2) + int(ind2)) + ' , \'Физика\');'
                   cursor.execute(update)
                   connection.commit()
           except:
               pass
           # Вывод
           with connection.cursor() as cursor:
               select = 'select uid, original, raitring from napravlen where `name` = \'Физика\' order by raitring desc;'

               cursor.execute(select)
               rows = cursor.fetchall()  # вывожу список

           id = ''
           rait = ''
           orig = ''
           vivod = ''
           vivod2 = ''
           vivod3 = ''
           vivod4 = ''
           vivod5 = ''
           vivod6 = ''
           vivod7 = ''
           vivod8 = ''
           vivod9 = ''

           mesto = 0
           for row in rows:
               id = str(row).split(',')[0].split(' ')[1]
               id2 = str(id).replace('.0', '')

               rait = str(row).split('},')[-1].split(' ')[-1]
               rait2 = rait.replace('}', '')

               orig = str(row).split('l\':')[1].split(', \'rai')[0]

               if orig == ' 0':
                   cop = 'Копия'
               else:
                   cop = 'Оригинал'

               if id2 != str(message.from_user.id):
                   if mesto < 50:
                       vivod = vivod + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(cop) + '\n'
                   if mesto > 50 and mesto <= 100:
                       vivod2 = vivod2 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 100 and mesto <= 150:
                       vivod3 = vivod3 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 150 and mesto <= 200:
                       vivod4 = vivod4 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 200 and mesto <= 250:
                       vivod5 = vivod5 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 250 and mesto <= 300:
                       vivod6 = vivod6 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 300 and mesto <= 350:
                       vivod7 = vivod7 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 350 and mesto <= 400:
                       vivod8 = vivod8 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 400 and mesto <= 450:
                       vivod9 = vivod9 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   mesto = mesto + 1

                   print(vivod)
                   print(vivod2)
                   print(vivod3)
                   print(vivod4)

               if id2 == str(message.from_user.id):
                   if mesto <= 50:
                       vivod = vivod + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 50 and mesto <= 100:
                       vivod2 = vivod2 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 100 and mesto <= 150:
                       vivod3 = vivod3 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 150 and mesto <= 200:
                       vivod4 = vivod4 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 200 and mesto <= 250:
                       vivod5 = vivod5 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 250 and mesto <= 300:
                       vivod6 = vivod6 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 300 and mesto <= 350:
                       vivod7 = vivod7 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 350 and mesto <= 400:
                       vivod8 = vivod8 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 400 and mesto <= 450:
                       vivod9 = vivod9 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   global mesto_user2
                   mesto_user2 = mesto + 1
                   print(mesto_user2)

           bot.send_message(message.chat.id, str(vivod), reply_markup=markup)
           if mesto > 51:
               bot.send_message(message.chat.id, str(vivod2), reply_markup=markup)
           if mesto > 101:
               bot.send_message(message.chat.id, str(vivod3), reply_markup=markup)
           if mesto > 151:
               bot.send_message(message.chat.id, str(vivod4), reply_markup=markup)
           if mesto > 201:
               bot.send_message(message.chat.id, str(vivod5), reply_markup=markup)
           if mesto > 251:
               bot.send_message(message.chat.id, str(vivod6), reply_markup=markup)
           if mesto > 301:
               bot.send_message(message.chat.id, str(vivod7), reply_markup=markup)
           if mesto > 351:
               bot.send_message(message.chat.id, str(vivod8), reply_markup=markup)
           if mesto > 401:
               bot.send_message(message.chat.id, str(vivod9), reply_markup=markup)

           bot.send_message(message.chat.id, 'Вы занимаете ' + str(mesto_user2) + ' место', reply_markup=markup)

           with connection.cursor() as cursor:
               select = 'select sum(original) from napravlen where `name` = \'Физика\' and raitring >=' + str(
                   rez) + ';'
               cursor.execute(select)
               count_orig = cursor.fetchall()

           count_orig1 = str(count_orig).replace('[{\'sum(original)\': Decimal(\'', '')
           count_orig2 = str(count_orig1).replace('\')}]', '')

           bot.send_message(message.chat.id,
                            'Выше вас в рейтинге ' + str(count_orig2) + ' человек(а) подал(и) оригинал документов',
                            reply_markup=markup)

           with connection.cursor() as cursor:
               proxodnie_fizika = 'select kol_vo_mest from napravlen where `name` = \'Физика\' limit 1;'
               cursor.execute(proxodnie_fizika)
               mesta_fizika = cursor.fetchall()

           mesta = str(mesta_fizika).split(' ')[-1].split('}')[0]
           bot.send_message(message.chat.id, 'Всего бюджетных мест на это направление ' + str(mesta),
                            reply_markup=markup)


           # Шансы
           try:
               if int(count_orig2) < int(mesta) and int(mesto_user2) < int(mesta):
                   bot.send_message(message.chat.id, 'У вас отличные шансы поступить на выбранное направление',
                                    reply_markup=markup)
               if int(count_orig2) < int(mesta) and int(mesto_user2) > int(mesta):
                   bot.send_message(message.chat.id, 'У вас средние шансы поступить на выбранное направление',
                                    reply_markup=markup)
               if int(count_orig2) >= int(mesta):
                   bot.send_message(message.chat.id, 'У вас маленькие шансы поступить на выбранное направление',
                                    reply_markup=markup)
           except:
               pass





           # Очистка после вывода
           with connection.cursor() as cursor:
               clear = 'delete from `user` where id = ' + str(message.from_user.id) + ';'
               cursor.execute(clear)
               connection.commit()

           with connection.cursor() as cursor:
               clear = 'delete from napravlen where uid = ' + str(message.from_user.id) + ';'
               cursor.execute(clear)
               connection.commit()




























       if napr == 2 and message.text == 'Узнать результаты':
           markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
           back = types.KeyboardButton('В главное меню')
           markup.add(back)

           if message.text == '/start':
               start(message)
               return

           if message.text == '/parse21':
               parse_common(message)
               main(message)
               return

           if message.text == 'В главное меню':  # Выход в главное меню
               main(message)
               bot.send_message(message.chat.id, 'Выберите направление')
               return

           if message.text == 'Узнать результаты':
               with connection.cursor() as cursor:
                   select = 'select first_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   first = cursor.fetchall()
                   first1 = str(first).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select second_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   second = cursor.fetchall()
                   second2 = str(second).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select third_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   thrid = cursor.fetchall()
                   thrid2 = str(thrid).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select ind_doc from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   ind = cursor.fetchall()
                   ind2 = str(ind).split(' ')[-1].split('}')[0]
                   if ind2 == 'None':
                       ind2 = 0
               try:
                   rez = int(first1) + int(second2) + int(thrid2) + int(ind2)
               except:
                   pass
           bot.send_message(message.chat.id, 'Ваши баллы : ' + str(rez), reply_markup=markup)

           with connection.cursor() as cursor:
               proxodnie_fizika = 'select rait from proxodnie where `name` = \'Информатика и вычислительная техника\';'
               cursor.execute(proxodnie_fizika)
               prox_fizika = cursor.fetchall()

           prox = str(prox_fizika).split(' ')[-1].split('}')[0]
           bot.send_message(message.chat.id, 'В прошлом году на это направление проходной балл был ' + str(prox),
                            reply_markup=markup)

           try:
               with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
                   update = 'insert into napravlen(uid, raitring,`name`) value(' + str(message.from_user.id) + ',' + str(
                       int(first1) + int(second2) + int(thrid2) + int(
                           ind2)) + ' , \'Информатика и вычислительная техника\');'
                   cursor.execute(update)
                   connection.commit()
           except:
               pass
           # Вывод
           with connection.cursor() as cursor:
               select = 'select uid, original, raitring from napravlen where `name` = \'Информатика и вычислительная техника\' order by raitring desc;'

               cursor.execute(select)
               rows = cursor.fetchall()  # вывожу список

           id = ''
           rait = ''
           orig = ''
           vivod = ''
           vivod2 = ''
           vivod3 = ''
           vivod4 = ''
           vivod5 = ''
           vivod6 = ''
           vivod7 = ''
           vivod8 = ''
           vivod9 = ''

           mesto = 0
           for row in rows:
               id = str(row).split(',')[0].split(' ')[1]
               id2 = str(id).replace('.0', '')

               rait = str(row).split('},')[-1].split(' ')[-1]
               rait2 = rait.replace('}', '')

               orig = str(row).split('l\':')[1].split(', \'rai')[0]

               if orig == ' 0':
                   cop = 'Копия'
               else:
                   cop = 'Оригинал'

               if id2 != str(message.from_user.id):
                   if mesto < 50:
                       vivod = vivod + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(cop) + '\n'
                   if mesto > 50 and mesto <= 100:
                       vivod2 = vivod2 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 100 and mesto <= 150:
                       vivod3 = vivod3 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 150 and mesto <= 200:
                       vivod4 = vivod4 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 200 and mesto <= 250:
                       vivod5 = vivod5 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 250 and mesto <= 300:
                       vivod6 = vivod6 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 300 and mesto <= 350:
                       vivod7 = vivod7 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 350 and mesto <= 400:
                       vivod8 = vivod8 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 400 and mesto <= 450:
                       vivod9 = vivod9 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   mesto = mesto + 1

                   print(vivod)
                   print(vivod2)
                   print(vivod3)
                   print(vivod4)

               if id2 == str(message.from_user.id):
                   if mesto <= 50:
                       vivod = vivod + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 50 and mesto <= 100:
                       vivod2 = vivod2 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 100 and mesto <= 150:
                       vivod3 = vivod3 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 150 and mesto <= 200:
                       vivod4 = vivod4 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 200 and mesto <= 250:
                       vivod5 = vivod5 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 250 and mesto <= 300:
                       vivod6 = vivod6 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 300 and mesto <= 350:
                       vivod7 = vivod7 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 350 and mesto <= 400:
                       vivod8 = vivod8 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 400 and mesto <= 450:
                       vivod9 = vivod9 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   global mesto_user1
                   mesto_user1 = mesto + 1
                   print(mesto_user1)

           bot.send_message(message.chat.id, str(vivod), reply_markup=markup)
           if mesto > 51:
               bot.send_message(message.chat.id, str(vivod2), reply_markup=markup)
           if mesto > 101:
               bot.send_message(message.chat.id, str(vivod3), reply_markup=markup)
           if mesto > 151:
               bot.send_message(message.chat.id, str(vivod4), reply_markup=markup)
           if mesto > 201:
               bot.send_message(message.chat.id, str(vivod5), reply_markup=markup)
           if mesto > 251:
               bot.send_message(message.chat.id, str(vivod6), reply_markup=markup)
           if mesto > 301:
               bot.send_message(message.chat.id, str(vivod7), reply_markup=markup)
           if mesto > 351:
               bot.send_message(message.chat.id, str(vivod8), reply_markup=markup)
           if mesto > 401:
               bot.send_message(message.chat.id, str(vivod9), reply_markup=markup)

           bot.send_message(message.chat.id, 'Вы занимаете ' + str(mesto_user1) + ' место', reply_markup=markup)

           with connection.cursor() as cursor:
               select = 'select sum(original) from napravlen where `name` = \'Информатика и вычислительная техника\' and raitring >=' + str(
                   rez) + ';'
               cursor.execute(select)
               count_orig = cursor.fetchall()

           count_orig1 = str(count_orig).replace('[{\'sum(original)\': Decimal(\'', '')
           count_orig2 = str(count_orig1).replace('\')}]', '')

           bot.send_message(message.chat.id,
                            'Выше вас в рейтинге ' + str(count_orig2) + ' человек(а) подал(и) оригинал документов',
                            reply_markup=markup)

           with connection.cursor() as cursor:
               proxodnie_fizika = 'select kol_vo_mest from napravlen where `name` = \'Информатика и вычислительная техника\' limit 1;'
               cursor.execute(proxodnie_fizika)
               mesta_fizika = cursor.fetchall()

           mesta = str(mesta_fizika).split(' ')[-1].split('}')[0]
           bot.send_message(message.chat.id, 'Всего бюджетных мест на это направление ' + str(mesta),
                            reply_markup=markup)

           # Шансы
           try:
               if int(count_orig2) < int(mesta) and int(mesto_user1) < int(mesta):
                   bot.send_message(message.chat.id, 'У вас отличные шансы поступить на выбранное направление',
                                    reply_markup=markup)
               if int(count_orig2) < int(mesta) and int(mesto_user1) > int(mesta):
                   bot.send_message(message.chat.id, 'У вас средние шансы поступить на выбранное направление',
                                    reply_markup=markup)
               if int(count_orig2) >= int(mesta):
                   bot.send_message(message.chat.id, 'У вас маленькие шансы поступить на выбранное направление',
                                    reply_markup=markup)
           except:
               pass
           # Очистка после вывода
           with connection.cursor() as cursor:
               clear = 'delete from `user` where id = ' + str(message.from_user.id) + ';'
               cursor.execute(clear)
               connection.commit()

           with connection.cursor() as cursor:
               clear = 'delete from napravlen where uid = ' + str(message.from_user.id) + ';'
               cursor.execute(clear)
               connection.commit()



































       if napr == 3 and message.text == 'Узнать результаты':
           markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
           back = types.KeyboardButton('В главное меню')
           markup.add(back)

           if message.text == '/start':
               start(message)
               return

           if message.text == '/parse21':
               parse_common(message)
               main(message)
               return

           if message.text == 'В главное меню':  # Выход в главное меню
               main(message)
               bot.send_message(message.chat.id, 'Выберите направление')
               return

           if message.text == 'Узнать результаты':
               with connection.cursor() as cursor:
                   select = 'select first_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   first = cursor.fetchall()
                   first1 = str(first).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select second_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   second = cursor.fetchall()
                   second2 = str(second).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select third_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   thrid = cursor.fetchall()
                   thrid2 = str(thrid).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select ind_doc from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   ind = cursor.fetchall()
                   ind2 = str(ind).split(' ')[-1].split('}')[0]
                   if ind2 == 'None':
                       ind2 = 0
               try:
                   rez = int(first1) + int(second2) + int(thrid2) + int(ind2)
               except:
                   pass
           bot.send_message(message.chat.id, 'Ваши баллы : ' + str(rez), reply_markup=markup)

           with connection.cursor() as cursor:
               proxodnie_fizika = 'select rait from proxodnie where `name` = \'Программная инженерия\';'
               cursor.execute(proxodnie_fizika)
               prox_fizika = cursor.fetchall()

           prox = str(prox_fizika).split(' ')[-1].split('}')[0]
           bot.send_message(message.chat.id, 'В прошлом году на это направление проходной балл был ' + str(prox),
                            reply_markup=markup)

           try:
               with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
                   update = 'insert into napravlen(uid, raitring,`name`) value(' + str(message.from_user.id) + ',' + str(
                       int(first1) + int(second2) + int(thrid2) + int(
                           ind2)) + ' , \'Программная инженерия\');'
                   cursor.execute(update)
                   connection.commit()
           except:
               pass
           # Вывод
           with connection.cursor() as cursor:
               select = 'select uid, original, raitring from napravlen where `name` = \'Программная инженерия\' order by raitring desc;'

               cursor.execute(select)
               rows = cursor.fetchall()  # вывожу список

           id = ''
           rait = ''
           orig = ''
           vivod = ''
           vivod2 = ''
           vivod3 = ''
           vivod4 = ''
           vivod5 = ''
           vivod6 = ''
           vivod7 = ''
           vivod8 = ''
           vivod9 = ''

           mesto = 0
           for row in rows:
               id = str(row).split(',')[0].split(' ')[1]
               id2 = str(id).replace('.0', '')

               rait = str(row).split('},')[-1].split(' ')[-1]
               rait2 = rait.replace('}', '')

               orig = str(row).split('l\':')[1].split(', \'rai')[0]

               if orig == ' 0':
                   cop = 'Копия'
               else:
                   cop = 'Оригинал'

               if id2 != str(message.from_user.id):
                   if mesto < 50:
                       vivod = vivod + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(cop) + '\n'
                   if mesto > 50 and mesto <= 100:
                       vivod2 = vivod2 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 100 and mesto <= 150:
                       vivod3 = vivod3 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 150 and mesto <= 200:
                       vivod4 = vivod4 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 200 and mesto <= 250:
                       vivod5 = vivod5 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 250 and mesto <= 300:
                       vivod6 = vivod6 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 300 and mesto <= 350:
                       vivod7 = vivod7 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 350 and mesto <= 400:
                       vivod8 = vivod8 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 400 and mesto <= 450:
                       vivod9 = vivod9 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   mesto = mesto + 1

                   print(vivod)
                   print(vivod2)
                   print(vivod3)
                   print(vivod4)

               if id2 == str(message.from_user.id):
                   if mesto <= 50:
                       vivod = vivod + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 50 and mesto <= 100:
                       vivod2 = vivod2 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 100 and mesto <= 150:
                       vivod3 = vivod3 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 150 and mesto <= 200:
                       vivod4 = vivod4 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 200 and mesto <= 250:
                       vivod5 = vivod5 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 250 and mesto <= 300:
                       vivod6 = vivod6 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 300 and mesto <= 350:
                       vivod7 = vivod7 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 350 and mesto <= 400:
                       vivod8 = vivod8 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 400 and mesto <= 450:
                       vivod9 = vivod9 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   global mesto_user3
                   mesto_user3 = mesto + 1
                   print(mesto_user3)

           bot.send_message(message.chat.id, str(vivod), reply_markup=markup)
           if mesto > 51:
               bot.send_message(message.chat.id, str(vivod2), reply_markup=markup)
           if mesto > 101:
               bot.send_message(message.chat.id, str(vivod3), reply_markup=markup)
           if mesto > 151:
               bot.send_message(message.chat.id, str(vivod4), reply_markup=markup)
           if mesto > 201:
               bot.send_message(message.chat.id, str(vivod5), reply_markup=markup)
           if mesto > 251:
               bot.send_message(message.chat.id, str(vivod6), reply_markup=markup)
           if mesto > 301:
               bot.send_message(message.chat.id, str(vivod7), reply_markup=markup)
           if mesto > 351:
               bot.send_message(message.chat.id, str(vivod8), reply_markup=markup)
           if mesto > 401:
               bot.send_message(message.chat.id, str(vivod9), reply_markup=markup)

           bot.send_message(message.chat.id, 'Вы занимаете ' + str(mesto_user3) + ' место', reply_markup=markup)

           with connection.cursor() as cursor:
               select = 'select sum(original) from napravlen where `name` = \'Программная инженерия\' and raitring >=' + str(
                   rez) + ';'
               cursor.execute(select)
               count_orig = cursor.fetchall()

           count_orig1 = str(count_orig).replace('[{\'sum(original)\': Decimal(\'', '')
           count_orig2 = str(count_orig1).replace('\')}]', '')

           bot.send_message(message.chat.id,
                            'Выше вас в рейтинге ' + str(count_orig2) + ' человек(а) подал(и) оригинал документов',
                            reply_markup=markup)

           with connection.cursor() as cursor:
               proxodnie_fizika = 'select kol_vo_mest from napravlen where `name` = \'Программная инженерия\' limit 1;'
               cursor.execute(proxodnie_fizika)
               mesta_fizika = cursor.fetchall()

           mesta = str(mesta_fizika).split(' ')[-1].split('}')[0]
           bot.send_message(message.chat.id, 'Всего бюджетных мест на это направление ' + str(mesta),
                            reply_markup=markup)

           # Шансы
           try:
               if int(count_orig2) < int(mesta) and int(mesto_user3) < int(mesta):
                   bot.send_message(message.chat.id, 'У вас отличные шансы поступить на выбранное направление',
                                    reply_markup=markup)
               if int(count_orig2) < int(mesta) and int(mesto_user3) > int(mesta):
                   bot.send_message(message.chat.id, 'У вас средние шансы поступить на выбранное направление',
                                    reply_markup=markup)
               if int(count_orig2) >= int(mesta):
                   bot.send_message(message.chat.id, 'У вас маленькие шансы поступить на выбранное направление',
                                    reply_markup=markup)
           except:
               pass

           # Очистка после вывода
           with connection.cursor() as cursor:
               clear = 'delete from `user` where id = ' + str(message.from_user.id) + ';'
               cursor.execute(clear)
               connection.commit()

           with connection.cursor() as cursor:
               clear = 'delete from napravlen where uid = ' + str(message.from_user.id) + ';'
               cursor.execute(clear)
               connection.commit()



























       if napr == 4 and message.text == 'Узнать результаты':
           markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
           back = types.KeyboardButton('В главное меню')
           markup.add(back)

           if message.text == '/start':
               start(message)
               return

           if message.text == '/parse21':
               parse_common(message)
               main(message)
               return

           if message.text == 'В главное меню':  # Выход в главное меню
               main(message)
               bot.send_message(message.chat.id, 'Выберите направление')
               return

           if message.text == 'Узнать результаты':
               with connection.cursor() as cursor:
                   select = 'select first_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   first = cursor.fetchall()
                   first1 = str(first).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select second_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   second = cursor.fetchall()
                   second2 = str(second).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select third_egz from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   thrid = cursor.fetchall()
                   thrid2 = str(thrid).split(' ')[-1].split('}')[0]
               with connection.cursor() as cursor:
                   select = 'select ind_doc from `user` where id = ' + str(message.from_user.id) + ';'
                   cursor.execute(select)
                   ind = cursor.fetchall()
                   ind2 = str(ind).split(' ')[-1].split('}')[0]
                   if ind2 == 'None':
                       ind2 = 0
               try:
                  rez = int(first1) + int(second2) + int(thrid2) + int(ind2)
               except:
                   pass
           bot.send_message(message.chat.id, 'Ваши баллы : ' + str(rez), reply_markup=markup)

           with connection.cursor() as cursor:
               proxodnie_fizika = 'select rait from proxodnie where `name` = \'Приборостроение\';'
               cursor.execute(proxodnie_fizika)
               prox_fizika = cursor.fetchall()

           prox = str(prox_fizika).split(' ')[-1].split('}')[0]

           bot.send_message(message.chat.id, 'В прошлом году на это направление проходной балл был ' + str(prox),
                            reply_markup=markup)
           try:
               with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
                   update = 'insert into napravlen(uid, raitring,`name`) value(' + str(message.from_user.id) + ',' + str(
                       int(first1) + int(second2) + int(thrid2) + int(
                           ind2)) + ' , \'Приборостроение\');'
                   cursor.execute(update)
                   connection.commit()
           except:
               pass
           # Вывод
           with connection.cursor() as cursor:
               select = 'select uid, original, raitring from napravlen where `name` = \'Приборостроение\' order by raitring desc;'

               cursor.execute(select)
               rows = cursor.fetchall()  # вывожу список

           id = ''
           rait = ''
           orig = ''
           vivod = ''
           vivod2 = ''
           vivod3 = ''
           vivod4 = ''
           vivod5 = ''
           vivod6 = ''
           vivod7 = ''
           vivod8 = ''
           vivod9 = ''

           mesto = 0
           for row in rows:
               id = str(row).split(',')[0].split(' ')[1]
               id2 = str(id).replace('.0', '')

               rait = str(row).split('},')[-1].split(' ')[-1]
               rait2 = rait.replace('}', '')

               orig = str(row).split('l\':')[1].split(', \'rai')[0]

               if orig == ' 0':
                   cop = 'Копия'
               else:
                   cop = 'Оригинал'

               if id2 != str(message.from_user.id):
                   if mesto < 50:
                       vivod = vivod + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(cop) + '\n'
                   if mesto > 50 and mesto <= 100:
                       vivod2 = vivod2 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 100 and mesto <= 150:
                       vivod3 = vivod3 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 150 and mesto <= 200:
                       vivod4 = vivod4 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 200 and mesto <= 250:
                       vivod5 = vivod5 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 250 and mesto <= 300:
                       vivod6 = vivod6 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 300 and mesto <= 350:
                       vivod7 = vivod7 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 350 and mesto <= 400:
                       vivod8 = vivod8 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   if mesto > 400 and mesto <= 450:
                       vivod9 = vivod9 + 'id: ' + str(id2) + ' рейтинг: ' + str(rait2) + ' Документы : ' + str(
                           cop) + '\n'
                   mesto = mesto + 1

                   print(vivod)
                   print(vivod2)
                   print(vivod3)
                   print(vivod4)

               if id2 == str(message.from_user.id):
                   if mesto <= 50:
                       vivod = vivod + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 50 and mesto <= 100:
                       vivod2 = vivod2 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 100 and mesto <= 150:
                       vivod3 = vivod3 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 150 and mesto <= 200:
                       vivod4 = vivod4 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 200 and mesto <= 250:
                       vivod5 = vivod5 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 250 and mesto <= 300:
                       vivod6 = vivod6 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   if mesto > 300 and mesto <= 350:
                       vivod7 = vivod7 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 350 and mesto <= 400:
                       vivod8 = vivod8 + 'Вы:  рейтинг: ' + str(rait2) + '\n'
                   if mesto > 400 and mesto <= 450:
                       vivod9 = vivod9 + 'Вы:  рейтинг: ' + str(rait2) + '\n'

                   global mesto_user4
                   mesto_user4 = mesto + 1
                   print(mesto_user4)

           bot.send_message(message.chat.id, str(vivod), reply_markup=markup)
           if mesto > 51:
               bot.send_message(message.chat.id, str(vivod2), reply_markup=markup)
           if mesto > 101:
               bot.send_message(message.chat.id, str(vivod3), reply_markup=markup)
           if mesto > 151:
               bot.send_message(message.chat.id, str(vivod4), reply_markup=markup)
           if mesto > 201:
               bot.send_message(message.chat.id, str(vivod5), reply_markup=markup)
           if mesto > 251:
               bot.send_message(message.chat.id, str(vivod6), reply_markup=markup)
           if mesto > 301:
               bot.send_message(message.chat.id, str(vivod7), reply_markup=markup)
           if mesto > 351:
               bot.send_message(message.chat.id, str(vivod8), reply_markup=markup)
           if mesto > 401:
               bot.send_message(message.chat.id, str(vivod9), reply_markup=markup)

           bot.send_message(message.chat.id, 'Вы занимаете ' + str(mesto_user4) + ' место', reply_markup=markup)

           with connection.cursor() as cursor:
               select = 'select sum(original) from napravlen where `name` = \'Приборостроение\' and raitring >=' + str(
                   rez) + ';'
               cursor.execute(select)
               count_orig = cursor.fetchall()

           count_orig1 = str(count_orig).replace('[{\'sum(original)\': Decimal(\'', '')
           count_orig2 = str(count_orig1).replace('\')}]', '')

           bot.send_message(message.chat.id,
                            'Выше вас в рейтинге ' + str(count_orig2) + ' человек(а) подал(и) оригинал документов',
                            reply_markup=markup)

           with connection.cursor() as cursor:
               proxodnie_fizika = 'select kol_vo_mest from napravlen where `name` = \'Приборостроение\' limit 1;'
               cursor.execute(proxodnie_fizika)
               mesta_fizika = cursor.fetchall()

           mesta = str(mesta_fizika).split(' ')[-1].split('}')[0]
           bot.send_message(message.chat.id, 'Всего бюджетных мест на это направление ' + str(mesta),
                            reply_markup=markup)

           # Шансы
           try:
               if int(count_orig2) < int(mesta) and int(mesto_user4) < int(mesta):
                   bot.send_message(message.chat.id, 'У вас отличные шансы поступить на выбранное направление',
                                    reply_markup=markup)
               if int(count_orig2) < int(mesta) and int(mesto_user4) > int(mesta):
                   bot.send_message(message.chat.id, 'У вас средние шансы поступить на выбранное направление',
                                    reply_markup=markup)
               if int(count_orig2) >= int(mesta):
                   bot.send_message(message.chat.id, 'У вас маленькие шансы поступить на выбранное направление',
                                    reply_markup=markup)
           except:
               pass

           # Очистка после вывода
           with connection.cursor() as cursor:
               clear = 'delete from `user` where id = ' + str(message.from_user.id) + ';'
               cursor.execute(clear)
               connection.commit()

           with connection.cursor() as cursor:
               clear = 'delete from napravlen where uid = ' + str(message.from_user.id) + ';'
               cursor.execute(clear)
               connection.commit()








   def yes(message):

       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       back = types.KeyboardButton('В главное меню')
       rez = types.KeyboardButton('Узнать результаты')
       markup.add(back, rez)

       if message.text == '/start':
           start(message)
           return

       if message.text == '/parse21':
           parse_common(message)
           main(message)
           return

       if message.text == 'В главное меню': # Выход в главное меню
           main(message)
           bot.send_message(message.chat.id, 'Выберите направление')
           return

       if message.text == 'Узнать результаты': # Выход в главное меню
           noo(message)
           return



       doc = message.text

       for i in range(len(doc)):
           if doc[i] != ',' and doc[i] != '1' and doc[i] != '2' and doc[i] != '3' and doc[i] != '4' and doc[i] != '5' and doc[i] != '6' and doc[i] != '7'  :
               msg = bot.send_message(message.chat.id, 'Вы написали номер или номера достижений в неверном формате, попробуйте еще раз')
               bot.register_next_step_handler(msg, yes)
               return

       if len(doc) > 1:
           for i in range(len(doc)):
               if ( doc[i-1]==','and doc[i]==',' ) :
                   msg = bot.send_message(message.chat.id,'Вы написали номер или номера достижений в неверном формате, попробуйте еще раз')
                   bot.register_next_step_handler(msg, yes)
                   return

       if len(doc) > 1:
           for i in range(1,len(doc)):
               if str(doc[i - 1]).isdigit() and doc[i] != ',':
                   msg = bot.send_message(message.chat.id, 'Вы написали номер или номера достижений в неверном формате, попробуйте еще раз')
                   bot.register_next_step_handler(msg, yes)
                   return

       if doc[0] == ',' or doc[len(doc)-1] == ',':
           msg = bot.send_message(message.chat.id, 'Вы написали номер или номера достижений в неверном формате, попробуйте еще раз')
           bot.register_next_step_handler(msg, yes)
           return


       gto_bal = 0
       gto_bal2 = 0
       gto_bal3 = 0
       for i in range(len(doc)):
           if doc[i] == '1':
               gto_bal = 1
           if doc[i] == '2':
               gto_bal = 2
               gto_bal2 = 1
           if doc[i] == '3':
               gto_bal = 3
               gto_bal3 = 1

       if gto_bal2 == 1:
           gto_bal = 2

       if gto_bal3 == 1:
           gto_bal = 3


       olimp_bal = 0
       olimp6 = 0
       olimp8 = 0

       for i in range(len(doc)):
           if doc[i] == '4':
               olimp_bal = 3
           if doc[i] == '5':
               olimp_bal = 6
               olimp6 = 1
           if doc[i] == '6':
               olimp_bal = 8
               olimp8 = 1

       if olimp6 == 1:
           olimp_bal = 6

       if olimp8 == 1:
           olimp_bal = 8



       red = 0
       for i in range(len(doc)):
           if doc[i] == '7':
              red = 10

       itog = gto_bal + olimp_bal + red

       if itog > 10:
           itog = 10
           bot.send_message(message.chat.id, 'Обратите внимание что в сумме индивидуальные достижения могут принести максимум 10 баллов к основному рейтингу')


       # Передаем баллы за инд. дос. в бд
       with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
           update = 'update `user` set ind_doc = ' + str(itog) + ' where id = ' + str(message.from_user.id) + ';'
           cursor.execute(update)
           connection.commit()



       if itog == 1:
           msg = bot.send_message(message.chat.id, 'За индвивидуальные достижения вы получаете '+str(itog)+ ' балл')
           bot.register_next_step_handler(msg, noo)
       if itog == 2 or itog == 3 or itog == 4:
           msg = bot.send_message(message.chat.id, 'За индвивидуальные достижения вы получаете ' + str(itog) +' балла')
           bot.register_next_step_handler(msg, noo)
       if itog == 5 or itog == 6 or itog == 7 or itog == 8 or itog == 9 or itog == 10:
           msg = bot.send_message(message.chat.id, 'За индвивидуальные достижения вы получаете ' + str(itog) + ' баллов')
           bot.register_next_step_handler(msg, noo)






   def exit(message):


       if message.text == '/start':
           start(message)
           return

       if message.text == '/parse21':
           parse_common(message)
           main(message)
           return
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       back = types.KeyboardButton('В главное меню')
       rez = types.KeyboardButton('Узнать результаты')
       markup.add(back, rez)

       if message.text == 'В главное меню':  # Выход в главное меню
           main(message)
           bot.send_message(message.chat.id, 'Выберите направление')
           return



       rait3 = message.text
       # print(rus1)

       if rait3.isdigit():
           if(int(rait3)>=1 and int(rait3) <= 100):
               if int(rait3) >= 40:
                   with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
                       update = 'update `user` set third_egz = ' + str(rait3) + ' where id = ' + str(message.from_user.id) + ';'
                       cursor.execute(update)
                       connection.commit()

                   bot.send_message(message.chat.id, 'Отлично, вы перешли порог по русскому языку, который состовляет 40 баллов.', reply_markup=markup)
                   markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                   No = types.KeyboardButton('Нет')
                   back = types.KeyboardButton('В главное меню')
                   markup.add(No,back)
                   msg = bot.send_message(message.chat.id,
                                                 '\nУ вас есть какие-нибудь индивидуальные достижения ?'
                                                 '\nИндивидуальными достижениями считаются:'
                                                 '\n1 Бронзовая награда ГТО - 1 балл'
                                                 '\n2 Серебрянная награда ГТО - 2 балла'
                                                 '\n3 Золотая награда ГТО - 3 балла'
                                                 '\n4 Сертификат участия во Всероссийской олимпиаде - 3 балла'
                                                 '\n5 Диплом призера во Всероссийской олимпиаде - 6 баллов'
                                                 '\n6 Диплом победителя во Всероссийской олимпиаде - 8 баллов'
                                                 '\n7 Наличие красного аттестата - 10 баллов'
                                                 '\nНапишите через запятую номер или номера ваших индивидуальных достижений(из этого сообщения), без пробелов (например: 1,4,7) отправьте, и нажмите кнопку Узнать результаты'
                                                 '\nЕсли нет индвивидуальных достижений просто нажмите кнопку Узнать результаты')
                   bot.register_next_step_handler(msg, yes)




               if int(rait3) < 40:
                   markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                   back = types.KeyboardButton('В главное меню')
                   markup.add(back)
                   bot.send_message(message.chat.id, 'К сожалению вы не перешли порог по русскому языку, который состовляет 40 баллов. Вы не можете записаться на данное направление',reply_markup=markup)
       # вывод
           else:
               if message.text != 'В главное меню':
                   msg = bot.send_message(message.chat.id, 'Введите число от 1 до 100', reply_markup=markup)
                   bot.register_next_step_handler(msg, exit)

       else:
           if message.text != 'В главное меню':
               msg = bot.send_message(message.chat.id, 'Введите число от 1 до 100', reply_markup=markup)
               bot.register_next_step_handler(msg, exit)




   def rus(message):
       if message.text == '/start':
           start(message)
           return

       if message.text == '/parse21':
           parse_common(message)
           main(message)
           return

       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       back = types.KeyboardButton('В главное меню')
       markup.add(back)

       if message.text == 'В главное меню':  # Выход в главное меню
           main(message)
           bot.send_message(message.chat.id, 'Выберите направление')
           return
       # вывод

       rait2 = message.text  # баллы по математике
       if rait2.isdigit():
           if(int(rait2)>=1 and int(rait2) <= 100):
               if int(rait2) >= 39:
                    msg = bot.send_message(message.chat.id,  'Отлично, вы перешли порог по математике, который состовляет 39 баллов. Сколько у вас баллов за ЕГЭ по русскому языку?', reply_markup=markup)
                    bot.register_next_step_handler(msg, exit)  # перехожу к русскому

                    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
                        update = 'update `user` set second_egz = ' + str(rait2) +' where id = ' + str(message.from_user.id) + ';'
                        cursor.execute(update)
                        connection.commit()


               if int(rait2) < 39:

                   bot.send_message(message.chat.id,'К сожалению вы не перешли порог по математике, который состовляет 39 баллов. Вы не можете записаться на данное направление', reply_markup=markup)
       # print(matem1)
           else:
               if message.text != 'В главное меню':
                   msg = bot.send_message(message.chat.id, 'Введите число от 1 до 100')
                   bot.register_next_step_handler(msg, rus)

       else:
           if message.text != 'В главное меню':
               msg = bot.send_message(message.chat.id, 'Введите число от 1 до 100')
               bot.register_next_step_handler(msg, rus)














   def matem(message):
       # вывод
       if message.text == '/start':
           start(message)
           return

       if message.text == '/parse21':
           parse_common(message)
           main(message)
           return
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       back = types.KeyboardButton('В главное меню')
       markup.add(back)

       rait1 = message.text  # баллы
       if message.text == 'В главное меню':  # Выход в главное меню
           main(message)
           bot.send_message(message.chat.id, 'Выберите направление')
           return

       print(message.from_user.id)
       if rait1.isdigit() and choose == 1:
           if(int(rait1)>=1 and int(rait1) <= 100 ):
               if int(rait1) >= 30:
                   msg = bot.send_message(message.chat.id,   'Отлично, вы перешли порог по английскому языку, который состовляет 30 баллов. Сколько у вас баллов за ЕГЭ по математике?', reply_markup=markup)
                   bot.register_next_step_handler(msg, rus)  # перехожу к русскому
                   # Передаем в бд по айди пользователя данные
                   with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
                       update = 'insert into `user`(id, first_egz) value('+ str(message.from_user.id) +','+ str(rait1) +');'
                       cursor.execute(update)
                       connection.commit()



               if int(rait1) < 30:
                   bot.send_message(message.chat.id,'К сожалению вы не перешли порог по английскому языку, который состовляет 30 баллов. Вы не можете записаться на данное направление', reply_markup=markup)
           else:
               msg = bot.send_message(message.chat.id, 'Введите число от 1 до 100')
               bot.register_next_step_handler(msg, matem)


       elif rait1.isdigit() and choose == 2: # Информатика
           if (int(rait1) >= 1 and int(rait1) <= 100):
               if int(rait1) >= 44:
                   msg = bot.send_message(message.chat.id, 'Отлично, вы перешли порог по информатике, который состовляет 44 баллов. Сколько у вас баллов за ЕГЭ по математике?', reply_markup=markup)
                   bot.register_next_step_handler(msg, rus)  # перехожу к русскому

                   with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
                       update = 'insert into `user`(id, first_egz) value('+ str(message.from_user.id) +','+ str(rait1) +');'
                       cursor.execute(update)
                       connection.commit()

               if int(rait1) < 44:
                   bot.send_message(message.chat.id,  'К сожалению вы не перешли порог по информатике, который состовляет 44 баллов. Вы не можете записаться на данное направление',reply_markup=markup)
           else:
               msg = bot.send_message(message.chat.id, 'Введите число от 1 до 100')
               bot.register_next_step_handler(msg, matem)

       elif rait1.isdigit() and choose == 3: #физика
           if (int(rait1) >= 1 and int(rait1) <= 100):
               if int(rait1) >= 39:
                    msg = bot.send_message(message.chat.id,   'Отлично, вы перешли порог по физике, который состовляет 39 баллов. Сколько у вас баллов за ЕГЭ по математике?', reply_markup=markup)
                    bot.register_next_step_handler(msg, rus)  # перехожу к русскому

                    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
                        update = 'insert into `user`(id, first_egz) value(' + str(message.from_user.id) + ',' + str(rait1) + ');'
                        cursor.execute(update)
                        connection.commit()


               if int(rait1) < 39:
                   bot.send_message(message.chat.id,  'К сожалению вы не перешли порог по физике, который состовляет 39 баллов. Вы не можете записаться на данное направление',reply_markup=markup)
           else:
               if message.text != 'В главное меню':
                   msg = bot.send_message(message.chat.id, 'Введите число от 1 до 100')
                   bot.register_next_step_handler(msg, matem)

       else:
           if message.text != 'В главное меню':
               msg = bot.send_message(message.chat.id, 'Введите число от 1 до 100')
               bot.register_next_step_handler(msg, matem)

   # Выбор профильного предмета (направление физика

   if message.text == 'Профильный предмет - Английский язык':
       def angl(message):
           if message.text == '/start':
               start(message)
               return

           if message.text == '/parse21':
               parse_common(message)
               main(message)
               return
       # вывод
           markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
           back = types.KeyboardButton('В главное меню')
           markup.add(back)
           msg = bot.send_message(message.chat.id, 'Сколько у вас баллов за ЕГЭ по английскому языку?', reply_markup=markup)
           bot.register_next_step_handler(msg, matem)  # перехожу к математике
       angl(message)
       choose = 1

   if message.text == 'Профильный предмет - Информатика':
       def inf(message):
           if message.text == '/start':
               start(message)
               return

           if message.text == '/parse21':
               parse_common(message)
               main(message)
               return

           if message.text == 'В главное меню':  # Выход в главное меню
               main(message)
               bot.send_message(message.chat.id, 'Выберите направление')
               return
       # вывод
           markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
           back = types.KeyboardButton('В главное меню')
           markup.add(back)
           msg = bot.send_message(message.chat.id, 'Сколько у вас баллов за ЕГЭ по информатике?', reply_markup=markup)
           bot.register_next_step_handler(msg, matem)  # перехожу к математике
       inf(message)
       choose = 2

   if message.text == 'Профильный предмет - Физика':
       def fiz(message):
           if message.text == 'В главное меню':  # Выход в главное меню
               main(message)
               bot.send_message(message.chat.id, 'Выберите направление')
               return

           if message.text == '/start':
               start(message)
               return

           if message.text == '/parse21':
               parse_common(message)
               main(message)
               return
           markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
           back = types.KeyboardButton('В главное меню')
           markup.add(back)
       # вывод

           msg = bot.send_message(message.chat.id, 'Сколько у вас баллов за ЕГЭ по физике?', reply_markup=markup)
           bot.register_next_step_handler(msg, matem)  # перехожу к математике
       fiz(message)
       choose = 3

   global napr # Переменная для выбора направления

   if message.text == 'Физика':
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       back = types.KeyboardButton('В главное меню')
       write = types.KeyboardButton('Записаться на направление Физика')
       markup.add(back, write)

       #Вывод кол-ва бюджетных мест по заданному направлению из бд
       with connection.cursor() as cursor:
           proxodnie_fizika = 'select kol_vo_mest from napravlen where `name` = \'Физика\' limit 1;'
           cursor.execute(proxodnie_fizika)
           mesta_fizika = cursor.fetchall()

       mesta = str(mesta_fizika).split(' ')[-1].split('}')[0]
       bot.send_message(message.chat.id, 'План набора на бюджет, обшие основания = ' + str(mesta), reply_markup=markup)

   if message.text == 'Записаться на направление Физика' :
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       Fiz = types.KeyboardButton('Профильный предмет - Физика')
       Inf = types.KeyboardButton('Профильный предмет - Информатика')
       Ang = types.KeyboardButton('Профильный предмет - Английский язык')
       Back = types.KeyboardButton('В главное меню')
       markup.add(Fiz, Inf, Ang,Back)
       bot.send_message(message.chat.id, 'Выберите профильный предмет', reply_markup=markup)
       # Очистка данных текущего пользователя
       with connection.cursor() as cursor:
           clear = 'delete from `user` where id = ' + str(message.from_user.id) + ';'
           cursor.execute(clear)
           connection.commit()

       with connection.cursor() as cursor:
           clear = 'delete from napravlen where uid = ' + str(message.from_user.id) + ';'
           cursor.execute(clear)
           connection.commit()
       napr = 1













   if message.text == 'Информатика и вычислительная техника':
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       back = types.KeyboardButton('В главное меню')
       write = types.KeyboardButton('Записаться на направление Информатика и вычислительная техника')
       markup.add(back, write)
       #Вывод кол-ва бюджетных мест по заданному направлению из бд
       with connection.cursor() as cursor:
           proxodnie_fizika = 'select kol_vo_mest from napravlen where `name` = \'Информатика и вычислительная техника\' limit 1;'
           cursor.execute(proxodnie_fizika)
           mesta_fizika = cursor.fetchall()

       mesta = str(mesta_fizika).split(' ')[-1].split('}')[0]
       bot.send_message(message.chat.id, 'План набора на бюджет, обшие основания = ' + str(mesta), reply_markup=markup)

   if message.text == 'Записаться на направление Информатика и вычислительная техника' :
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       Fiz = types.KeyboardButton('Профильный предмет - Физика')
       Inf = types.KeyboardButton('Профильный предмет - Информатика')
       Ang = types.KeyboardButton('Профильный предмет - Английский язык')
       Back = types.KeyboardButton('В главное меню')
       markup.add(Fiz, Inf, Ang,Back)
       bot.send_message(message.chat.id, 'Выберите профильный предмет', reply_markup=markup)

       # Очистка данных текущего пользователя
       with connection.cursor() as cursor:
           clear = 'delete from `user` where id = ' + str(message.from_user.id) + ';'
           cursor.execute(clear)
           connection.commit()

       with connection.cursor() as cursor:
           clear = 'delete from napravlen where uid = ' + str(message.from_user.id) + ';'
           cursor.execute(clear)
           connection.commit()
       napr = 2














   if message.text == 'Программная инженерия':
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       back = types.KeyboardButton('В главное меню')
       write = types.KeyboardButton('Записаться на направление Программная инженерия')
       markup.add(back, write)
       #Вывод кол-ва бюджетных мест по заданному направлению из бд
       with connection.cursor() as cursor:
           proxodnie_fizika = 'select kol_vo_mest from napravlen where `name` = \'Программная инженерия\' limit 1;'
           cursor.execute(proxodnie_fizika)
           mesta_fizika = cursor.fetchall()
           print(mesta_fizika)

       mesta = str(mesta_fizika).split(' ')[-1].split('}')[0]
       bot.send_message(message.chat.id, 'План набора на бюджет, обшие основания = ' + str(mesta), reply_markup=markup)

   if message.text == 'Записаться на направление Программная инженерия' :
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       Fiz = types.KeyboardButton('Профильный предмет - Физика')
       Inf = types.KeyboardButton('Профильный предмет - Информатика')
       Ang = types.KeyboardButton('Профильный предмет - Английский язык')
       Back = types.KeyboardButton('В главное меню')
       markup.add(Fiz, Inf, Ang,Back)
       bot.send_message(message.chat.id, 'Выберите профильный предмет', reply_markup=markup)

       # Очистка данных текущего пользователя
       with connection.cursor() as cursor:
           clear = 'delete from `user` where id = ' + str(message.from_user.id) + ';'
           cursor.execute(clear)
           connection.commit()

       with connection.cursor() as cursor:
           clear = 'delete from napravlen where uid = ' + str(message.from_user.id) + ';'
           cursor.execute(clear)
           connection.commit()
       napr = 3
































   if message.text == 'Приборостроение':
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       back = types.KeyboardButton('В главное меню')
       write = types.KeyboardButton('Записаться на направление Приборостроение')
       markup.add(back, write)
       #Вывод кол-ва бюджетных мест по заданному направлению из бд
       with connection.cursor() as cursor:
           proxodnie_fizika = 'select kol_vo_mest from napravlen where `name` = \'Приборостроение\' limit 1;'
           cursor.execute(proxodnie_fizika)
           mesta_fizika = cursor.fetchall()
           print(mesta_fizika)

       mesta = str(mesta_fizika).split(' ')[-1].split('}')[0]
       bot.send_message(message.chat.id, 'План набора на бюджет, обшие основания = ' + str(mesta), reply_markup=markup)

   if message.text == 'Записаться на направление Приборостроение' :
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
       Fiz = types.KeyboardButton('Профильный предмет - Физика')
       Inf = types.KeyboardButton('Профильный предмет - Информатика')
       Ang = types.KeyboardButton('Профильный предмет - Английский язык')
       Back = types.KeyboardButton('В главное меню')
       markup.add(Fiz, Inf, Ang,Back)
       bot.send_message(message.chat.id, 'Выберите профильный предмет', reply_markup=markup)

       # Очистка данных текущего пользователя
       with connection.cursor() as cursor:
           clear = 'delete from `user` where id = ' + str(message.from_user.id) + ';'
           cursor.execute(clear)
           connection.commit()

       with connection.cursor() as cursor:
           clear = 'delete from napravlen where uid = ' + str(message.from_user.id) + ';'
           cursor.execute(clear)
           connection.commit()
       napr = 4








bot.polling(none_stop=True)