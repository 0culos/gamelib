from flask import render_template, request, redirect, url_for, flash, session

from gamelib import app, db
from models import Games, Users


@app.route('/')
def index():
    game_list = Games.query.order_by(Games.id)
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
        game = Games.query.filter_by(name=name).first()

        if game:
            flash('Game already exists.')
            return redirect(url_for('index'))

        new = Games(name=name, category=category, console=console)

        db.session.add(new)
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/edit')
def edit():
    if 'logged_in' not in session or session['logged_in'] is None:
        return redirect(url_for('login', next_page=url_for('edit')))
    return render_template('edit.html', title='Editing Game')


@app.route('/update', methods=('GET', 'POST'))
def update():
    pass


@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    return render_template('login.html', next_page=next_page)


@app.route('/authenticate', methods=('GET', 'POST'))
def authenticate():
    user = Users.query.filter_by(nickname=request.form['user']).first()
    if user:
        if request.form['password'] == user.password:
            session['logged_in'] = user.nickname
            flash(user.nickname + ' logged in successfully.')
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
