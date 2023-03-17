from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (
    LENGTH_OF_ORIGINAL_URL,
    LENGTH_OF_SHORT_URL,
    LONG_URL,
    REQUIRED_FIELD,
    RANDOM_SYMBOLS,
    SHORT_URL
)

BUTTON_TO_CREATE = 'Создать'


class YacutForm(FlaskForm):
    original_link = URLField(
        LONG_URL,
        validators=[DataRequired(message=REQUIRED_FIELD),
                    Length(max=LENGTH_OF_ORIGINAL_URL)]
    )
    custom_id = URLField(
        SHORT_URL,
        validators=[
            Length(max=LENGTH_OF_SHORT_URL),
            Optional(),
            Regexp(rf'^[{RANDOM_SYMBOLS}]+$')
        ]
    )
    submit = SubmitField(BUTTON_TO_CREATE)
