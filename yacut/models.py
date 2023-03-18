import random
import re
from datetime import datetime

from flask import url_for

from . import db
from .constants import (
    ATTEMPTS,
    REGEXP_SYMBOLS,
    LENGTH_OF_ORIGINAL_URL,
    LENGTH_OF_SHORT_URL,
    LENGTH_OF_RANDOM_URL,
    RANDOM_SYMBOLS
)
from .error_handlers import ShortValueError

NOT_FIND_SHORT_URL = 'Не удалось подобрать короткий url!'
USED_NAME = 'Имя "{custom_id}" уже занято.'
INCORRECT_SYMBOLS = 'Присутствуют некорректные символы'
INCORRECT_ORIGINAL_LENGTH = (
    'Длина оригинальной ссылки {original_length} '
    'превышает 1024'
)
INCORRECT_SHORT_LENGTH = (
    'Длина короткой ссылки {short_length} '
    'превышает 16'
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LENGTH_OF_ORIGINAL_URL), nullable=False)
    short = db.Column(db.String(LENGTH_OF_SHORT_URL), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_url_map(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id(
            symbols=RANDOM_SYMBOLS,
            short_length=LENGTH_OF_RANDOM_URL
    ):
        for _ in range(ATTEMPTS):
            random_short = ''.join(random.choices(symbols, k=short_length))
            if not URLMap.get_url_map(random_short):
                return random_short
        raise ValueError(NOT_FIND_SHORT_URL)

    @staticmethod
    def create(original, short=None, to_validate=False):
        if not short:
            short = URLMap.get_unique_short_id()
        elif to_validate:
            length_original = len(original)
            length_short = len(short)
            if length_original > LENGTH_OF_ORIGINAL_URL:
                raise ValueError(
                    INCORRECT_ORIGINAL_LENGTH.format(
                        original_length=length_original
                    ))
            if length_short > LENGTH_OF_SHORT_URL:
                raise ValueError(INCORRECT_SHORT_LENGTH.format(short_length=length_short))
            if not re.match(REGEXP_SYMBOLS, short):
                raise ValueError(INCORRECT_SYMBOLS)
            if URLMap.get_url_map(short):
                raise ShortValueError(USED_NAME.format(custom_id=short))
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_for_short_url',
                short=self.short,
                _external=True))
