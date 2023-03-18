import random
import re
from datetime import datetime

from flask import url_for

from . import db
from .constants import (
    ATTEMPT_NUMBER,
    CORRECT_SYMBOLS,
    LENGTH_OF_ORIGINAL_URL,
    LENGTH_OF_SHORT_URL,
    LENGTH_OF_RANDOM_URL,
    RANDOM_SYMBOLS
)
from .error_handlers import ShortValueError

NOT_FIND_SHORT = 'короткий url не удалось подобрать'
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
    def get_short_object(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_url_map(original, short=None, to_validate=False):
        if not short:
            for _ in range(ATTEMPT_NUMBER):
                if not URLMap.get_short_object(
                        ''.join(random.choices(
                            RANDOM_SYMBOLS, k=LENGTH_OF_RANDOM_URL
                        ))):
                    short = ''.join(random.choices(
                        RANDOM_SYMBOLS, k=LENGTH_OF_RANDOM_URL
                    ))
        elif to_validate:
            length_original = len(original)
            length_short = len(short)
            if length_original > LENGTH_OF_ORIGINAL_URL:
                raise ValueError(INCORRECT_ORIGINAL_LENGTH.format(original_length=length_original))
            if length_short > LENGTH_OF_SHORT_URL:
                raise ValueError(INCORRECT_SHORT_LENGTH.format(short_length=length_short))
            if not re.match(CORRECT_SYMBOLS, short):
                raise ValueError(INCORRECT_SYMBOLS)
            if URLMap.get_short_object(short):
                raise ShortValueError(USED_NAME.format(custom_id=short))
        url = URLMap(original=original, short=short)
        db.session.add(url)
        db.session.commit()
        return url

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_for_short_url',
                short=self.short,
                _external=True))
