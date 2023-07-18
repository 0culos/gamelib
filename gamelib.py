from flask import Flask, render_template


class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console

    def __str__(self):
        return f"{self.name}, {self.category}, {self.console}"


app = Flask(__name__)


@app.route('/start')
def hello():
    game1 = Game('Tetris', 'Puzzle', 'Atari')
    game2 = Game('God of War', 'Rack and Slash', 'PS2')
    game3 = Game('Crash', 'Adventure', 'PS1')
    game_list = [game1, game2, game3]
    return render_template('list.html', title='Games', games=game_list)


@app.route('/new_game')
def new_game():
    return render_template('new_game.html', title='New Game')
app.run()
