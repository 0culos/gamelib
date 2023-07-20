import time

from flask import render_template, request, redirect, url_for, flash, session, send_from_directory

from gamelib import app, db
from models import Games, Users
from helpers import return_image, delete_image, GameForm


@app.route('/')
def index():
    game_list = Games.query.order_by(Games.id)
    return render_template('list.html', title='Games', games=game_list)


@app.route('/new_game')
def new_game():
    if 'logged_in' not in session or session['logged_in'] is None:
        return redirect(url_for('login', next_page=url_for('new_game')))
    form = GameForm()
    return render_template('new_game.html', title='New Game', form=form)


@app.route('/create', methods=('GET', 'POST'))
def create():
    form = GameForm(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('new_game'))

    name = form.name.data
    category = form.category.data
    console = form.console.data
    game = Games.query.filter_by(name=name).first()

    if game:
        flash('Game already exists.')
        return redirect(url_for('index'))

    new = Games(name=name, category=category, console=console)

    db.session.add(new)
    db.session.commit()

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    file.save(f'{upload_path}/cover{new.id}-{timestamp}.jpg')

    flash("Successfully game added")

    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit(id):
    if 'logged_in' not in session or session['logged_in'] is None:
        return redirect(url_for('login', next_page=url_for('edit', id=id)))

    game = Games.query.filter_by(id=id).first()
    form = GameForm()
    form.name.data = game.name
    form.category.data = game.category
    form.console.data = game.console
    game_cover = return_image(id)
    return render_template('edit.html', title='Editing Game', id=id, game_cover=game_cover, form=form)


@app.route('/update', methods=('GET', 'POST'))
def update():
    form = GameForm(request.form)

    if form.validate_on_submit():
        game = Games.query.filter_by(id=request.form['id']).first()

        game.name = form.name.data
        game.category = form.category.data
        game.console = form.console.data

        db.session.add(game)
        db.session.commit()

        file = request.files['file']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        delete_image(game.id)
        file.save(f'{upload_path}/cover{game.id}-{timestamp}.jpg')

        flash("Game updated successfully")

    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_in' not in session or session['logged_in'] is None:
        return redirect(url_for('login'))

    Games.query.filter_by(id=id).delete()
    db.session.commit()

    flash("Successfully deleted game")

    return redirect(url_for('index'))


@app.route('/login', methods=('GET', 'POST'))
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


@app.route('/uploads/<file_name>')
def image(file_name):
    return send_from_directory('uploads', file_name)
