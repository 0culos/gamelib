from flask import render_template, request, redirect, url_for, flash, session
from gamelib import app
from helpers import UserForm
from models import Users
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    form = UserForm()
    return render_template('login.html', next_page=next_page, form=form)


@app.route('/authenticate', methods=['POST', ])
def authenticate():
    form = UserForm(request.form)
    user = Users.query.filter_by(nickname=form.nickname.data).first()
    password = check_password_hash(user.password, form.password.data)

    if user and password:
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