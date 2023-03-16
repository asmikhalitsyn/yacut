from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (BUTTON_TO_CREATE,
                        LONG_URL,
                        REQUIRED_FIELD,
                        REGEXP_SHORT_URL,
                        SHORT_URL)


class YacutForm(FlaskForm):
    original_link = URLField(
        LONG_URL,
        validators=[DataRequired(message=REQUIRED_FIELD),
                    Length(1, 256)]
    )
    custom_id = URLField(
        SHORT_URL,
        validators=[
            Length(1, 128),
            Optional(),
            Regexp(REGEXP_SHORT_URL)
        ]
    )
    submit = SubmitField(BUTTON_TO_CREATE)
