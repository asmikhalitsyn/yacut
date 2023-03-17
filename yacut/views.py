from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app
from .forms import YacutForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short_url = form.custom_id.data
    if URLMap.check_url(short_url) is not None:
        flash(f'Имя {short_url} уже занято!')
        return render_template('index.html', form=form)
    url = URLMap.create_short_url(
        form.original_link.data,
        form.data.get('custom_id'),
    )
    return render_template(
        'index.html',
        form=form,
        result_url=url_for('index_view', _external=True) + url.short
    )


@app.route('/<string:short_url>', methods=['GET'])
def redirect_for_short_url(short_url):
    url = URLMap.check_url(short_url)
    if not url:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url.original), HTTPStatus.FOUND
