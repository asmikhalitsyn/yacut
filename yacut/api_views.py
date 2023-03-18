from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import ID_NO_FOUND
from .error_handlers import InvalidAPIUsage
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
        url_map = URLMap.create_short_url(data['url'], data.get('custom_id'))
    except ValueError:
        raise InvalidAPIUsage(ERROR_NAME)
    except NameError as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    link = URLMap.get_short_link(short_id)
    if link is None:
        raise InvalidAPIUsage(ID_NO_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.original}), HTTPStatus.OK
