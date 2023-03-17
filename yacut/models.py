import random
import re
from datetime import datetime

from flask import url_for

from . import db
from .constants import (
    LENGTH_OF_ORIGINAL_URL,
    LENGTH_OF_SHORT_URL,
    LENGTH_OF_RANDOM_URL,
    RANDOM_SYMBOLS,

)
from settings import REGEXP

USED_NAME = 'Имя "{custom_id}" уже занято.'
INCORRECT_SYMBOLS = 'Присутствуют некорректные символы'
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
    def generate_short_id(
            symbols=RANDOM_SYMBOLS,
            short_length=LENGTH_OF_RANDOM_URL
    ):
        return ''.join(random.choices(symbols, k=short_length))

    @staticmethod
    def get_short_id(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_short_url(original, short=None, validated_form=False):
        if not short:
            short = URLMap.generate_short_id()
        if not validated_form:
            length_short = len(short)
            if length_short > LENGTH_OF_SHORT_URL:
                raise ValueError(INCORRECT_SHORT_LENGTH.format(short_length=length_short))
            if not re.match(REGEXP, short):
                raise ValueError(INCORRECT_SYMBOLS)
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
