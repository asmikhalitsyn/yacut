import os
from re import escape

from yacut.constants import RANDOM_SYMBOLS

REGEXP = rf'^[{escape(RANDOM_SYMBOLS)}]+$'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
