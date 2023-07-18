from flask import Flask, render_template, request, redirect, url_for, flash


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

app = Flask(__name__)


@app.route('/')
def index():

    return render_template('list.html', title='Games', games=game_list)


@app.route('/new_game')
def new_game():
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
    return render_template('login.html')


@app.route('/authenticate', methods=('GET', 'POST'))
def authenticate():
    if 'alohomora' == request.form['password']:
        return redirect('/')
    else:
        return redirect('/login')


app.run()
