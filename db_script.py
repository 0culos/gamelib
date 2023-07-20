import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Connecting...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='oculos'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Wrong username or password.')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `gamelib`;")

cursor.execute("CREATE DATABASE `gamelib`;")

cursor.execute("USE `gamelib`;")

# criando tabelas
TABLES = {}
TABLES['Games'] = ('''
      CREATE TABLE `games` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL,
      `category` varchar(40) NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Users'] = ('''
      CREATE TABLE `users` (
      `name` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `password` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for name_table in TABLES:
    sql_table = TABLES[name_table]
    try:
        print('Creating table {}:'.format(name_table), end=' ')
        cursor.execute(sql_table)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Already exits')
        else:
            print(err.msg)
    else:
        print('OK')

# inserindo usuarios
sql_user = 'INSERT INTO users (name, nickname, password) VALUES (%s, %s, %s)'
users = [
    ("Bruno Divino", "BD", generate_password_hash("alohomora").decode('utf8')),
    ("Camila Ferreira", "Mila", generate_password_hash("paozinho").decode('utf8')),
    ("Guilherme Louro", "Cake", generate_password_hash("python_eh_vida").decode('utf8'))
]
cursor.executemany(sql_user, users)

cursor.execute('select * from gamelib.users')
print(' -------------  Users:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
sql_games = 'INSERT INTO games (name, category, console) VALUES (%s, %s, %s)'
games = [
    ('Tetris', 'Puzzle', 'Atari'),
    ('God of War', 'Hack n Slash', 'PS2'),
    ('Mortal Kombat', 'Luta', 'PS2'),
    ('Valorant', 'FPS', 'PC'),
    ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
    ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(sql_games, games)

cursor.execute('select * from gamelib.games')
print(' -------------  Games:  -------------')
for game in cursor.fetchall():
    print(game[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
