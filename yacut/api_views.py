from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import ID_NO_FOUND
from .error_handlers import InvalidAPIUsage, ShortValueError
from .models import URLMap

ERROR_NAME = 'Указано недопустимое имя для короткой ссылки'
NO_DATA = 'Отсутствует тело запроса'
NO_URL = '\"url\" является обязательным полем!'


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL)
    try:
        url_map = URLMap.create(
            data['url'],
            data.get('custom_id'),
            to_validate=True
        )
    except ValueError:
        raise InvalidAPIUsage(ERROR_NAME)
    except ShortValueError as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.get_url_map(short_id)
    if url_map is None:
        raise InvalidAPIUsage(ID_NO_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
