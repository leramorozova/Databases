import sqlite3


def dataset_creator():
    conn = sqlite3.connect('food_database.db')
    c = conn.cursor()
    c.executescript("""DROP TABLE IF EXISTS kkal_energy;

                 CREATE TABLE kkal_energy
                 (name TEXT, 
                 proteins FLOAT,
                 fat FLOAT, 
                 carbs FLOAT,
                 kkal FLOAT);
                       """)
    c.executescript("""DROP TABLE IF EXISTS kJ_energy;

                     CREATE TABLE kJ_energy
                     (name TEXT, 
                     proteins FLOAT,
                     fat FLOAT, 
                     carbs FLOAT,
                     kJ FLOAT);
                           """)
    conn.close()


def insert_info(name, proteins, fat, carbs):
    conn = sqlite3.connect('food_database.db')
    c = conn.cursor()
    kkal_energy = float(proteins) * 4 + float(fat) * 9 + float(carbs) * 4
    kJ_energy = float(proteins) * 17 + float(fat) * 38 + float(carbs) * 17
    c.execute('''
                    INSERT INTO kkal_energy (name, kkal, proteins, fat, carbs)
                    VALUES (?, ?, ?, ?, ?)
                        ''', [name, kkal_energy, proteins, fat, carbs])
    c.execute('''
                    INSERT INTO kJ_energy (name, kJ, proteins, fat, carbs)
                    VALUES (?, ?, ?, ?, ?)
                        ''', [name, kJ_energy, proteins, fat, carbs])
    conn.commit()
    conn.close()


def search(dish, measure):
    conn = sqlite3.connect('food_database.db')
    c = conn.cursor()
    dish = '%' + dish.lower() + '%'
    if measure == 'kkal':
        c.execute('''
                    SELECT * FROM kkal_energy WHERE name LIKE ?
                  ''', (dish,))
    if measure == 'kJ':
        c.execute('''
                    SELECT * FROM kJ_energy WHERE name LIKE ?
                  ''', [dish])
    response = c.fetchall()
    conn.close()
    return response


def viewer(measure):
    conn = sqlite3.connect('food_database.db')
    c = conn.cursor()
    if measure == 'kkal':
        c.execute('''SELECT * FROM kkal_energy''')
    if measure == 'kJ':
        c.execute('''SELECT * FROM kJ_energy''')
    response = c.fetchall()
    conn.close()
    return response