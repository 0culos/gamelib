import os

SECRET_KEY = 'dev'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:oculos@localhost/gamelib'

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
