"""

База содержит:

1) таблицу user_info со столбиками

user_name - имя пользователя VARCHAR(45)
user_surname - фамилия пользователя VARCHAR(45)
user_city - город, в котором пользователь живет VARCHAR(45)
user_age - возраст пользователя INT


2) таблицу friendship со столбиками

friend_1 - id пользователя из таблицы user_info, с которым дружит упомянутый пользователь INT
f_surname - фамилия пользователя VARCHAR(45)
f_city - город, в котором пользователь живет VARCHAR(45)
f_age - возраст пользователя INT

"""

from db_utils import Database


def insert_user_info(name, surname, city, user_age):
    db = Database()
    db.execute('''
    INSERT INTO user_info 
    (user_name, user_surname, user_city, user_age) 
    VALUES (%s, %s, %s, %s)
    ''', (name, surname, city, user_age))
    db.commit()


def insert_friend_info(user_name, user_surname, user_city, user_age, name, surname, city, age):
    db = Database()
    res = db.execute('''
    SELECT id FROM user_info
    WHERE user_name = %s AND user_surname = %s AND user_city = %s AND user_age = %s
    ''', (user_name, user_surname, user_city, user_age))
    print(res)
    try:
        user_id = res[0][0]
        db.execute('''
            INSERT INTO friendship
            (friend_1, friend_name, friend_surname, friend_city, friend_age)
            VALUES (%s, %s, %s, %s, %s)
            ''', (user_id, name, surname, city, age))
    except IndexError:
        db.execute('''
            INSERT INTO friendship
            (friend_name, friend_surname, friend_city, friend_age)
            VALUES (%s, %s, %s, %s)
            ''', (name, surname, city, age))
    db.commit()


def view_registered():
    db = Database()
    res = db.execute('''SELECT * FROM user_info''', 0)
    return res


def search(parameter, value):
    db = Database()
    out = []
    res = 0
    if parameter == 'name':
        res = db.execute('''SELECT * 
                        FROM user_info JOIN friendship 
                        ON (user_name = %s OR f_name = %s)''', (value, value))
    elif parameter == 'surname':
        res = db.execute('''SELECT * 
                        FROM user_info JOIN friendship 
                        ON (user_surname = %s OR f_surname = %s)''', (value, value))
    elif parameter == 'city':
        res = db.execute('''SELECT * 
                        FROM user_info JOIN friendship 
                        ON (user_city = %s OR f_city = %s)''', (value, value))
    elif parameter == 'age':
        res = db.execute('''SELECT * 
                        FROM user_info JOIN friendship 
                        ON (user_age = %s OR f_age = %s)''', (value, value))
    for el in res:
        out.append([el[1], el[2], el[3], el[4]])
        out.append([el[7], el[8], el[9], el[10]])
    if parameter == 'age':
        out = [el for el in out if int(value) in el]
    else:
        out = [el for el in out if value in el]
    unique = []
    for el in out:
        if el not in unique:
            unique.append(el)
    return unique


def view_all():
    out = []
    db = Database()
    res = db.execute('SELECT * FROM user_info JOIN friendship', 0)
    for el in res:
        out.append([el[1], el[2], el[3], el[4]])
        out.append([el[7], el[8], el[9], el[10]])
    unique = []
    for el in out:
        if el not in unique:
            unique.append(el)
    return unique


# to do
# не добавлять пользователя в friendship во второй раз, если он уже есть (например, если я добавляю того, кто уже там,
#   добавлять второго участника связи
# показать всех пользователей, которые из москвы, старше 18 и дружат с джоном
# join списка друзей и списка пользователей
