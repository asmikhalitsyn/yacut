from http import HTTPStatus

from flask import abort, redirect, render_template, url_for

from . import app
from .forms import YacutForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(
            form.original_link.data,
            form.data.get('custom_id')
        )
    except ValueError:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)
    return render_template(
        'index.html',
        form=form,
        result_url=url_for('index_view', _external=True) + url_map.short
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_for_short_url(short):
    url_map = URLMap.get_url_map(short)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original), HTTPStatus.FOUND
