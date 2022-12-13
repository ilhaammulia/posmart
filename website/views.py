from flask import Blueprint, render_template, redirect, url_for, session, request, flash, jsonify
from werkzeug.utils import secure_filename
from .models import User, Product
from functools import wraps
from os import path
from time import time
from . import app

views = Blueprint('views', __name__)


def must_login(func):
    @wraps(func)
    def is_login(*args, **kwargs):
        if 'current_user' not in session:
            return redirect(url_for('views.login'))
        return func(*args, **kwargs)
    return is_login


def admin_only():
    if session['current_user']['role'] != 'admin':
        return redirect(url_for('views.home'))


@views.route('/')
@must_login
def home():
    user = session['current_user']
    return render_template('home.html', user=user)


@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username=username, password=password)
        user.login()
        if user.is_logged_in:
            session['current_user'] = {
                'user_id': user.user_id,
                'name': user.name,
                'username': user.username,
                'role': user.role
            }
            return redirect(url_for('views.home'))
        flash('Username or Password invalid.', category='error')
    return render_template('login.html')


@views.route('/logout')
@must_login
def logout():
    session.pop('current_user')
    return redirect(url_for('views.login'))


@views.route('/products', methods=['GET', 'POST'])
@must_login
def products():
    if request.method == 'POST':
        method = request.form.get('_method')
        if method == 'delete':
            product_id = int(request.form.get('product_id'))
            product = Product(product_id=product_id)
            is_deleted = product.delete_product()
            if is_deleted:
                flash('Product has been deleted successfully.', category='success')
            else:
                flash('Product failed to delete.', category='error')
            return redirect(url_for('views.products'))
        name = request.form.get('name')
        category = request.form.get('category')
        price = int(request.form.get('price'))
        stocks = int(request.form.get('stocks'))
        img = request.files['img']
        secured_name = secure_filename(f'{int(time())}_{img.filename}')
        if method == 'put':
            product_id = int(request.form.get('product_id'))
            product = Product(product_id=product_id)
            data = (name, category, price, stocks, secured_name, product_id)
            is_updated = product.update_product(data)
            if is_updated:
                filename = path.join(path.dirname(
                    __file__), app.config['UPLOAD_FOLDER'], 'img', 'products', secured_name)
                try:
                    flash('Product has been updated successfully.',
                          category='success')
                    img.save(filename)
                except:
                    flash('Product image failed to update.', category='error')
        else:
            product = Product(name=name, category=category,
                              price=price, stocks=stocks, img=secured_name)
            created = product.create_product()
            if created:
                filename = path.join(path.dirname(
                    __file__), app.config['UPLOAD_FOLDER'], 'img', 'products', secured_name)
                try:
                    flash('Product has been created successfully.',
                          category='success')
                    img.save(filename)
                except:
                    flash('Product image failed to create.', category='error')
        return redirect(url_for('views.products'))

    user = session['current_user']
    products = Product().get_all_products()
    total_products = len(products)
    total_stocks = 0
    total_product_out_of_stock = 0
    for product_id, name, category, price, stocks, img in products:
        total_stocks += stocks
        if stocks == 0:
            total_product_out_of_stock += 1
    return render_template('products.html', user=user, products=enumerate(products), total_products=total_products, total_stocks=total_stocks, total_product_out_of_stock=total_product_out_of_stock)


@views.route('/report')
@must_login
def report():
    user = session['current_user']
    return render_template('report.html', user=user)


@views.route('/users', methods=['GET', 'POST'])
@must_login
def users():
    if request.method == 'POST':
        method = request.form.get('_method')
        username = request.form.get('username')
        name = request.form.get('name')
        role = request.form.get('role')
        if method == 'put':
            user_id = int(request.form.get('user_id'))
            myuser = User(user_id=user_id)
            user_data = myuser.get_user_by_id()
            if user_data:
                data = []
                password = request.form.get('password')
                confirmpass = request.form.get('confirmpass')
                if password != confirmpass:
                    flash(
                        'Your password not match with the confirmed password.', category='error')
                    return redirect(url_for('views.home'))
                data.append(name)
                data.append(username)
                if password:
                    data.append(password)
                if role:
                    data.append(role)
                else:
                    data.append(user_data[4])
                data.append(user_id)
                is_updated = myuser.update_user(tuple(data))
                if is_updated:
                    session['current_user'] = {
                        'user_id': user_id,
                        'name': name,
                        'username': username,
                        'role': role
                    }
                    flash('Your data has been updated.', category='success')
                else:
                    flash('Your data failed to update.', category='error')
                return redirect(url_for('views.home'))
    admin_only()
    user = session['current_user']
    return render_template('users.html', user=user)


@views.route('/json/<path>')
@must_login
def json(path):
    if path == 'products':
        product_id = request.args.get('product_id')
        if product_id:
            product = Product(product_id=product_id).get_product_by_id()
            return jsonify({
                'product_id': product[0],
                'name': product[1],
                'category': product[2],
                'price': product[3],
                'stocks': product[4],
                'img': product[5]
            })
    return jsonify({})
