from http import HTTPStatus
from re import fullmatch

from flask import jsonify, request

from . import app, db
from .constants import (
    ID_NO_FOUND,
    ERROR_NAME,
    MAX_LENGTH,
    NO_DATA,
    NO_URL,
    REGEXP_SHORT_URL
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import check_url, get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA)
    custom_id = data.get('custom_id')
    if not custom_id:
        custom_id = get_unique_short_id(MAX_LENGTH)
        data['custom_id'] = custom_id
    re_match = fullmatch(REGEXP_SHORT_URL, custom_id)
    if not re_match or len(custom_id) > 16:
        raise InvalidAPIUsage(ERROR_NAME)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL)
    if check_url(custom_id) is not None:
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = check_url(short_id)
    if url is None:
        raise InvalidAPIUsage(ID_NO_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
