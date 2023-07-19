from flask import Flask, render_template, request, redirect, url_for, flash, session


class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console

    def __str__(self):
        return f"{self.name}, {self.category}, {self.console}"


game1 = Game('Tetris', 'Puzzle', 'Atari')
game2 = Game('God of War', 'Rack and Slash', 'PS2')
game3 = Game('Crash', 'Adventure', 'PS1')
game_list = [game1, game2, game3]


class User:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nikname = nickname
        self.password = password


user1 = User('Danilo Pereira', 'Zóio', 'alohomora')
user2 = User('Camila Ferreira', 'Mila', 'paozinho')
user3 = User('Guilherme Louro', 'Cake', 'python_eh_vida')

users = {user1.nikname: user1,
         user2.nikname: user2,
         user3.nikname: user3
         }

app = Flask(__name__)
app.secret_key = 'dev'


@app.route('/')
def index():
    return render_template('list.html', title='Games', games=game_list)


@app.route('/new_game')
def new_game():
    if 'logged_in' not in session or session['logged_in'] is None:
        return redirect(url_for('login', next_page=url_for('new_game')))
    return render_template('new_game.html', title='New Game')


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        console = request.form['console']

        game = Game(name, category, console)
        game_list.append(game)

        return redirect(url_for('index'))

    return render_template('list.html', title='Games', games=game_list)


@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    return render_template('login.html', next_page=next_page)


@app.route('/authenticate', methods=('GET', 'POST'))
def authenticate():
    if request.form['user'] in users:
        user = users[request.form['user']]
        if request.form['password'] == user.password:
            session['logged_in'] = user.nikname
            flash(user.nikname + ' logged in successfully.')
            next_page = request.form['next_page']
            return redirect(next_page)
    else:
        flash('Login failed.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['logged_in'] = None
    flash('User logged out successfully')
    return redirect(url_for('index'))


app.run()
