import random
from datetime import datetime
from re import sub

from . import db
from .constants import (
    ERROR_NAME,
    LENGTH_OF_ORIGINAL_URL,
    LENGTH_OF_SHORT_URL,
    LENGTH_OF_RANDOM_URL,
    RANDOM_SYMBOLS,

)
from .error_handlers import InvalidAPIUsage

USED_NAME = 'Имя "{custom_id}" уже занято.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LENGTH_OF_ORIGINAL_URL), nullable=False)
    short = db.Column(db.String(LENGTH_OF_SHORT_URL), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_unique_short_id(
            symbols=RANDOM_SYMBOLS,
            short_length=LENGTH_OF_RANDOM_URL
    ):
        return ''.join(random.choices(symbols, k=short_length))

    @staticmethod
    def check_url(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_short_url(original, short=None):
        if not short:
            short = URLMap.get_unique_short_id()
        if len(short) > LENGTH_OF_SHORT_URL:
            raise InvalidAPIUsage(ERROR_NAME)
        incorrect_symbols = sub(rf'[{RANDOM_SYMBOLS}]', '', short)
        if incorrect_symbols:
            raise InvalidAPIUsage(ERROR_NAME)
        if URLMap.check_url(short):
            raise InvalidAPIUsage(USED_NAME.format(custom_id=short))
        url = URLMap(original=original, short=short)
        db.session.add(url)
        db.session.commit()
        return url

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=f'http://localhost/{self.short}',
        )

    def from_dict(self, data):
        api_dict = {
            'original': 'url',
            'short': 'custom_id'
        }
        for field in api_dict.keys():
            if api_dict[field] in data:
                setattr(self, field, data[api_dict[field]])
