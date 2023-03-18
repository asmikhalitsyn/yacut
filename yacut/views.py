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
    url = URLMap.create_short_url(
        form.original_link.data,
        form.data.get('custom_id'),
        validator=True
    )
    return render_template(
        'index.html',
        form=form,
        result_url=url_for('index_view', _external=True) + url.short
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_for_short_url(short):
    link = URLMap.get_short_link(short)
    if not link:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(link.original), HTTPStatus.FOUND
