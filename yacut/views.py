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
    url_map = URLMap.create_url_map(
        form.original_link.data,
        form.data.get('custom_id')
    )
    return render_template(
        'index.html',
        form=form,
        result_url=url_for('index_view', _external=True) + url_map.short
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_for_short_url(short):
    link_object = URLMap.get_short_object(short)
    if not link_object:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(link_object.original), HTTPStatus.FOUND
