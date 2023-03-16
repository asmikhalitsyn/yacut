import random
import string

from yacut.models import URLMap


def get_unique_short_id(length):
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for i in range(length)
    )


def check_url(arg):
    return URLMap.query.filter_by(short=arg).first()
