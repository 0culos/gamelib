import os
from gamelib import app


def return_image(id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}' in file_name:
            return file_name

    return 'standard_cover.jpg'


def delete_image(id):
    image = return_image(id)
    if image != 'standard_cover.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], image))
