from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app
from .forms import YacutForm
from .models import URLMap

NAME_IS_BUSY = 'Имя {custom_id} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short_url = form.custom_id.data
    if URLMap.get_short_id(short_url) is not None:
        flash(NAME_IS_BUSY.format(custom_id=short_url))
        return render_template('index.html', form=form)
    url = URLMap.create_short_url(
        form.original_link.data,
        form.data.get('custom_id'),
        validated_form=True
    )
    return render_template(
        'index.html',
        form=form,
        result_url=url_for('index_view', _external=True) + url.short
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_for_short_url(short):
    link = URLMap.get_short_id(short)
    if not link:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(link.original), HTTPStatus.FOUND
