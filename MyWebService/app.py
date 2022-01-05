import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# подключение к баззе данных
conn = psycopg2.connect(database='postgres', 
                        user='postgres', 
                        password='root', 
                        host='localhost',
                        port='5432')
cursor = conn.cursor()
@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                            (str(username), str(password)))
            records = list(cursor.fetchall())
            match (username, password):
                case ('', ''):
                    return "Вы ничего не ввели"
                case (username, ''):
                    return "Введите пароль"
                case ('', password):
                    return "Введите логин"
                case (username, password):
                    if not records:
                        return ('Неверное имя пользователя или пароль')
                    else:
                        return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name.replace(' ', '').isalpha():
            return 'В имени можно использовать только буквы'
        login = request.form.get('login')
        password = request.form.get('password')

        cursor.execute("SELECT * FROM service.users WHERE login=%s",
                        (str(login),))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO service.users (name, login, password) VALUES (%s, %s, %s);',
                        (str(name), str(login), str(password)))
            conn.commit()
        else:
            return "Вы уже зарегестрированы"

        return redirect('/login/')

    return render_template('registration.html')

# CREATE TABLE users (
#     id SERIAL,
#     login varchar(255),
#     password varchar(255),
#     name varchar(255)
# );

# INSERT INTO service.users(login, password, name) VALUES ('лол', 'лол', 'лол');


# SELECT * FROM service.users;