from bs4 import BeautifulSoup #  pip
import requests
import pymysql # pip
from config import host, user, password, db_name


connection = pymysql.connect(
    host=host,
    port=3306,
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)

def napravlen_prib(): #Функуия парсинга кол-ва мест
    response = requests.get('https://welcome.vstu.ru/acceptance/reyting/3637/')
    # ТАК КАК ПОКА В ФИЗИКЕ НЕТ ЗАПИСЕЙ ВЗЯЛ ССЫЛКУ ИЗ ИВТ
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('b')
    stroka = str(items)

    mesta = [] # массив баллов
    for i in range(len(stroka)):
        if (stroka[i - 2].isdigit() and stroka[i - 1].isdigit()):
            mesta.append(stroka[i - 2] + stroka[i - 1])
    fizika_mesta = mesta[0].split('\'')[-1].split('\'')[0]

    response = requests.get('https://welcome.vstu.ru/acceptance/reyting/3637/')
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='wide')
    stroka = str(items)
    bal = []  # массив баллов
    for i in range(len(stroka)):
        if stroka[i - 4] == '>' and (stroka[i - 3] == '1' or stroka[i - 3] == '2') and stroka[i - 1] != '<' and \
                stroka[i - 2] != '<' and stroka[i] != '-':
            bal.append(stroka[i - 3] + stroka[i - 2] + stroka[i - 1])


    items = soup.findAll('div', class_='wide')
    stroka = str(items)
    origCopy = []  # массив баллов
    for i in range(len(stroka)):
        if (stroka[i - 8] == 'd' and stroka[i - 7] == '>' and stroka[i - 6].isalpha() and stroka[i - 5].isalpha() and stroka[i - 4].isalpha() and stroka[i - 3].isalpha() and stroka[i - 2].isalpha() and stroka[i - 1] == '<' and stroka[i] == '/')\
            or stroka[i - 10] == '"' and stroka[i - 9] == '>' and stroka[i - 8].isalpha() and stroka[i - 7].isalpha() and stroka[i - 6].isalpha() and stroka[i - 5].isalpha() and stroka[i - 4].isalpha() and stroka[i - 3].isalpha() and stroka[i - 2].isalpha() and stroka[i - 1].isalpha() and stroka[i] == '<':
            origCopy.append(stroka[i - 6] + stroka[i - 5] + stroka[i - 4] + stroka[i - 3] + stroka[i - 2])
    original = []
    for i in range(len(origCopy)):
        if origCopy[i] == 'копия':
            original.append('0')
        else:
            original.append('1')

    items = soup.findAll('div', class_='unit-75')
    stroka = str(items)
    name = stroka.split('- ')[0].split(' (')[0]
    name2 = name.split('— ')

    name3 = str(name2[1])


    for i in range(len(bal)):
        # заполняю бд данными с сайта
        with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
            update = 'insert into napravlen(kol_vo_mest, raitring, original,name) value (' + str(fizika_mesta) +', ' +bal[i] +', ' + original[i] + ', ' + '\'' + name3 + '\'' + ');'
            cursor.execute(update)
            connection.commit()

def napravlen_prin(): #Функуия парсинга кол-ва мест
    response = requests.get('https://welcome.vstu.ru/acceptance/reyting/3636/')
    # ТАК КАК ПОКА В ФИЗИКЕ НЕТ ЗАПИСЕЙ ВЗЯЛ ССЫЛКУ ИЗ ИВТ
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('b')
    stroka = str(items)

    mesta = [] # массив баллов
    for i in range(len(stroka)):
        if (stroka[i - 2].isdigit() and stroka[i - 1].isdigit()):
            mesta.append(stroka[i - 2] + stroka[i - 1])
    fizika_mesta = mesta[0].split('\'')[-1].split('\'')[0]

    response = requests.get('https://welcome.vstu.ru/acceptance/reyting/3636/')
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='wide')
    stroka = str(items)
    bal = []  # массив баллов
    for i in range(len(stroka)):
        if stroka[i - 4] == '>' and (stroka[i - 3] == '1' or stroka[i - 3] == '2') and stroka[i - 1] != '<' and \
                stroka[i - 2] != '<' and stroka[i] != '-':
            bal.append(stroka[i - 3] + stroka[i - 2] + stroka[i - 1])


    items = soup.findAll('div', class_='wide')
    stroka = str(items)
    origCopy = []  # массив баллов
    for i in range(len(stroka)):
        if (stroka[i - 8] == 'd' and stroka[i - 7] == '>' and stroka[i - 6].isalpha() and stroka[i - 5].isalpha() and stroka[i - 4].isalpha() and stroka[i - 3].isalpha() and stroka[i - 2].isalpha() and stroka[i - 1] == '<' and stroka[i] == '/')\
            or stroka[i - 10] == '"' and stroka[i - 9] == '>' and stroka[i - 8].isalpha() and stroka[i - 7].isalpha() and stroka[i - 6].isalpha() and stroka[i - 5].isalpha() and stroka[i - 4].isalpha() and stroka[i - 3].isalpha() and stroka[i - 2].isalpha() and stroka[i - 1].isalpha() and stroka[i] == '<':
            origCopy.append(stroka[i - 6] + stroka[i - 5] + stroka[i - 4] + stroka[i - 3] + stroka[i - 2])
    original = []
    for i in range(len(origCopy)):
        if origCopy[i] == 'копия':
            original.append('0')
        else:
            original.append('1')

    items = soup.findAll('div', class_='unit-75')
    stroka = str(items)
    name = stroka.split('- ')[0].split(' (')[0]
    name2 = name.split('— ')

    name3 = str(name2[1])


    for i in range(len(bal)):
        # заполняю бд данными с сайта
        with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
            update = 'insert into napravlen(kol_vo_mest, raitring, original,name) value (' + str(fizika_mesta) +', ' +bal[i] +', ' + original[i] + ', ' + '\'' + name3 + '\'' + ');'
            cursor.execute(update)
            connection.commit()

def napravlen_ivt(): #Функуия парсинга кол-ва мест
    response = requests.get('https://welcome.vstu.ru/acceptance/reyting/3635/')
    # ТАК КАК ПОКА В ФИЗИКЕ НЕТ ЗАПИСЕЙ ВЗЯЛ ССЫЛКУ ИЗ ИВТ
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('b')
    stroka = str(items)

    mesta = [] # массив баллов
    for i in range(len(stroka)):
        if (stroka[i - 2].isdigit() and stroka[i - 1].isdigit()):
            mesta.append(stroka[i - 2] + stroka[i - 1])
    fizika_mesta = mesta[0].split('\'')[-1].split('\'')[0]

    response = requests.get('https://welcome.vstu.ru/acceptance/reyting/3635/')
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='wide')
    stroka = str(items)
    bal = []  # массив баллов
    for i in range(len(stroka)):
        if stroka[i - 4] == '>' and (stroka[i - 3] == '1' or stroka[i - 3] == '2') and stroka[i - 1] != '<' and \
                stroka[i - 2] != '<' and stroka[i] != '-':
            bal.append(stroka[i - 3] + stroka[i - 2] + stroka[i - 1])


    items = soup.findAll('div', class_='wide')
    stroka = str(items)
    origCopy = []  # массив баллов
    for i in range(len(stroka)):
        if (stroka[i - 8] == 'd' and stroka[i - 7] == '>' and stroka[i - 6].isalpha() and stroka[i - 5].isalpha() and stroka[i - 4].isalpha() and stroka[i - 3].isalpha() and stroka[i - 2].isalpha() and stroka[i - 1] == '<' and stroka[i] == '/')\
            or stroka[i - 10] == '"' and stroka[i - 9] == '>' and stroka[i - 8].isalpha() and stroka[i - 7].isalpha() and stroka[i - 6].isalpha() and stroka[i - 5].isalpha() and stroka[i - 4].isalpha() and stroka[i - 3].isalpha() and stroka[i - 2].isalpha() and stroka[i - 1].isalpha() and stroka[i] == '<':
            origCopy.append(stroka[i - 6] + stroka[i - 5] + stroka[i - 4] + stroka[i - 3] + stroka[i - 2])
    original = []
    for i in range(len(origCopy)):
        if origCopy[i] == 'копия':
            original.append('0')
        else:
            original.append('1')

    items = soup.findAll('div', class_='unit-75')
    stroka = str(items)
    name = stroka.split('- ')[0].split(' (')[0]
    name2 = name.split('— ')

    name3 = str(name2[1])


    for i in range(len(bal)):
        # заполняю бд данными с сайта
        with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
            update = 'insert into napravlen(kol_vo_mest, raitring, original,name) value (' + str(fizika_mesta) +', ' +bal[i] +', ' + original[i] + ', ' + '\'' + name3 + '\'' + ');'
            cursor.execute(update)
            connection.commit()

def napravlen_fizika(): #Функуия парсинга кол-ва мест
    response = requests.get('https://welcome.vstu.ru/acceptance/reyting/3716/')
    # ТАК КАК ПОКА В ФИЗИКЕ НЕТ ЗАПИСЕЙ ВЗЯЛ ССЫЛКУ ИЗ ИВТ
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('b')
    stroka = str(items)

    mesta = [] # массив баллов
    for i in range(len(stroka)):
        if (stroka[i - 2].isdigit() and stroka[i - 1].isdigit()):
            mesta.append(stroka[i - 2] + stroka[i - 1])
    fizika_mesta = mesta[0].split('\'')[-1].split('\'')[0]

    response = requests.get('https://welcome.vstu.ru/acceptance/reyting/3716/')
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='wide')
    stroka = str(items)
    bal = []  # массив баллов
    for i in range(len(stroka)):
        if stroka[i - 4] == '>' and (stroka[i - 3] == '1' or stroka[i - 3] == '2') and stroka[i - 1] != '<' and \
                stroka[i - 2] != '<' and stroka[i] != '-':
            bal.append(stroka[i - 3] + stroka[i - 2] + stroka[i - 1])


    items = soup.findAll('div', class_='wide')
    stroka = str(items)
    origCopy = []  # массив баллов
    for i in range(len(stroka)):
        if (stroka[i - 8] == 'd' and stroka[i - 7] == '>' and stroka[i - 6].isalpha() and stroka[i - 5].isalpha() and stroka[i - 4].isalpha() and stroka[i - 3].isalpha() and stroka[i - 2].isalpha() and stroka[i - 1] == '<' and stroka[i] == '/')\
            or stroka[i - 10] == '"' and stroka[i - 9] == '>' and stroka[i - 8].isalpha() and stroka[i - 7].isalpha() and stroka[i - 6].isalpha() and stroka[i - 5].isalpha() and stroka[i - 4].isalpha() and stroka[i - 3].isalpha() and stroka[i - 2].isalpha() and stroka[i - 1].isalpha() and stroka[i] == '<':
            origCopy.append(stroka[i - 6] + stroka[i - 5] + stroka[i - 4] + stroka[i - 3] + stroka[i - 2])
    original = []
    for i in range(len(origCopy)):
        if origCopy[i] == 'копия':
            original.append('0')
        else:
            original.append('1')

    items = soup.findAll('div', class_='unit-75')
    stroka = str(items)
    name = stroka.split('- ')[0].split(' (')[0]
    name2 = name.split('— ')

    name3 = str(name2[1])


    for i in range(len(bal)):
        # заполняю бд данными с сайта
        with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
            update = 'insert into napravlen(kol_vo_mest, raitring, original,name) value (' + str(fizika_mesta) +', ' +bal[i] +', ' + original[i] + ', ' + '\'' + name3 + '\'' + ');'
            cursor.execute(update)
            connection.commit()

def proxodnie():  # Функуия парсинга проходных баллов
    response = requests.get('https://tabiturient.ru/vuzu/vstu/proxodnoi/')
    # ТАК КАК ПОКА В ФИЗИКЕ НЕТ ЗАПИСЕЙ ВЗЯЛ ССЫЛКУ ИЗ ИВТ
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('span', class_='font3')
    stroka = str(items)
    name = [' ']

    for i in range(len(stroka)):
        if i != 0:
            name.append(stroka[i])

    name1 = ''.join(name)
    name2 = name1.split(' <span class="font3"><b style="text-transform:uppercase;">')
    name3 = ' '.join(name2)
    name4 = name3.split('</b></span>, ', 21)
    name4.pop(21)

    items = soup.findAll('span', class_='font11')
    stroka = str(items)
    ball = []  # массив баллов
    for i in range(len(stroka)):
        if (stroka[i - 3] == '1' or stroka[i - 3] == '2') and stroka[i - 2].isdigit() and stroka[i - 1].isdigit() and \
                stroka[i - 4] != '-':
            ball.append(stroka[i - 3] + stroka[i - 2] + stroka[i - 1])


    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[0]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[0].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[2]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[1].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[4]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[2].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[6]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[3].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[8]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[4].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[12]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[5].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[18]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[6].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[22]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[7].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[24]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[8].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[26]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[9].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[28]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[10].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[30]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[11].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[32]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[12].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[34]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[13].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[38]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[14].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[44]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[15].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[50]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[16].split('\'')[-1].split('\'')[0] + '\',' + str(2022) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[54]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[17].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[60]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[18].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[64]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[19].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()

    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        update = 'insert into proxodnie (rait,`name`,`year`) values (' + str(ball[66]).split('\'')[-1].split('\'')[
            0] + ', \'' + name4[20].split('\'')[-1].split('\'')[0] + '\',' + str(2021) + ');'
        cursor.execute(update)
        connection.commit()




def clear_BD():
    with connection.cursor() as cursor:  # Передаю сумму баллов пользователя
        clear1 = 'truncate proxodnie;'
        cursor.execute(clear1)
        clear2 = 'truncate napravlen;'
        cursor.execute(clear2)
        connection.commit()
