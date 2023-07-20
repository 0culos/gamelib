import os
from gamelib import app


def return_image(id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}.jpg' == file_name:
            return file_name

    return 'standard_cover.jpg'
