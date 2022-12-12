from flask import Blueprint, render_template, redirect, url_for, session, make_response, abort, request
from functools import wraps

views = Blueprint('views', __name__)


def must_login(func):
    @wraps(func)
    def is_login(*args, **kwargs):
        if 'user_id' not in request.cookies:
            return redirect(url_for('views.login'))
        user_id = request.cookies.get('user_id')
        if user_id not in session['current_session']:
            return redirect(url_for('views.login'))
        return func(*args, **kwargs)
    return is_login


@views.route('/')
# @must_login
def home():
    return render_template('home.html')


@views.route('/products')
# @must_login
def products():
    return render_template('products.html')


@views.route('/report')
# @must_login
def report():
    return render_template('report.html')


@views.route('/users')
# @must_login
def users():
    return render_template('users.html')
