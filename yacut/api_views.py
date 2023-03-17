from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (
    ID_NO_FOUND,
    NO_DATA,
    NO_URL,
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL)
    url = URLMap.create_short_url(data['url'], data.get('custom_id'))
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.check_url(short_id)
    if url is None:
        raise InvalidAPIUsage(ID_NO_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
