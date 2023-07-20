import os
from gamelib import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


class GameForm(FlaskForm):
    name = StringField('Game Title', [validators.DataRequired(), validators.Length(min=1, max=50)])
    category = StringField('Category', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    save = SubmitField('Save')


def return_image(id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}' in file_name:
            return file_name

    return 'standard_cover.jpg'


def delete_image(id):
    image = return_image(id)
    if image != 'standard_cover.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], image))
