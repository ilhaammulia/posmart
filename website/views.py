from flask import Blueprint, render_template, redirect, url_for, session, request, flash, jsonify
from werkzeug.utils import secure_filename
from .models import User, Product, Order, ProductSold
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
        if method == 'put':
            product_id = int(request.form.get('product_id'))
            product = Product(product_id=product_id)
            data = (name, category, price, stocks, product_id)
            is_updated = product.update_product(data)
            if is_updated:
                flash('Product has been updated successfully.', category='success')
            else:
                flash('Product failed to update.', category='error')
        else:
            img = request.files['img']
            secured_name = secure_filename(f'{int(time())}_{img.filename}')
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
    order = Order()
    today_orders = order.get_today_order()
    total_sales = sum([item[3] for item in today_orders])
    ps = ProductSold()
    products_sold = ps.get_today_by_reference_id()[0]
    top_products = ps.get_top_product()
    print(top_products)
    return render_template('report.html', user=user, total_sales=total_sales, today_orders=today_orders, products_sold=products_sold, top_products=top_products)


@views.route('/users', methods=['GET', 'POST'])
@must_login
def users():
    if request.method == 'POST':
        method = request.form.get('_method')
        if method == 'delete':
            user_id = int(request.form.get('user_id'))
            user = User(user_id=user_id)
            is_deleted = user.delete_user()
            if is_deleted:
                flash("User has been successfully deleted.", category="success")
            else:
                flash("User failed to delete.", category="error")
            return redirect(url_for('views.users'))
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        role = request.form.get('role')
        if method == 'put':
            user_id = int(request.form.get('user_id'))
            myuser = User(user_id=user_id)
            user_data = myuser.get_user_by_id()
            if user_data:
                data = []
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
        else:
            myuser = User(name=name, username=username,
                          password=password, role=role)
            is_created = myuser.create_user()
            if is_created:
                flash('User has been successfully created.', category='success')
            else:
                flash('User failed to create.', category='error')
            return redirect(url_for('views.users'))
    user = session['current_user']
    if user['role'] != 'admin':
        return redirect(url_for('views.home'))
    all_users = User().get_all_user()
    total_admin = len([
        worker[0]
        for worker in all_users if worker[4] == 'admin'
    ])
    total_staff = len([
        worker[0]
        for worker in all_users if worker[4] == 'staff'
    ])
    return render_template('users.html', user=user, users=all_users, total_admin=total_admin, total_staff=total_staff)


@views.route('/order', methods=['GET', 'POST'])
@must_login
def order():
    if request.method == 'POST':
        product_ids = request.form.getlist('productIds[]')
        product_quantities = request.form.getlist('productQtys[]')
        product_prices = request.form.getlist('productPrices[]')
        products_zip = zip(product_ids, product_quantities, product_prices)
        products = list(products_zip)

        reference_id = int(time())
        total_bill = request.form.get('total-bill')
        total_paid = request.form.get('total-paid')
        total_change = request.form.get('total-change')
        payment_method = request.form.get('pay-with')

        order = Order(reference_id=reference_id, total_bill=total_bill,
                      total_paid=total_paid, total_change=total_change, payment_method=payment_method)
        is_order_created = order.create_order()
        if is_order_created:
            product_sold = ProductSold(
                reference_id=reference_id, items=products)
            is_product_created = product_sold.create_sold()
            if is_product_created:
                for item in products:
                    product = Product(product_id=item[0])
                    stock = product.get_product_by_id()[4]

                    product.update_stock(stock - int(item[1]))
                flash('Thanks for your purchasing.', category='success')
        else:
            flash('Purchase failed to create.', category='error')
    return redirect(url_for('views.home'))


@views.route('/json/<path>')
@must_login
def json(path):
    if path == 'products':
        product_id = request.args.get('product_id')
        category = request.args.get('category')
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
        elif category:
            products = Product().get_product_by_category(category=category)
            return jsonify([
                {
                    'product_id': product[0],
                    'name': product[1],
                    'category': product[2],
                    'price': product[3],
                    'stocks': product[4],
                    'img': product[5]
                }
                for product in products
            ])
        else:
            pass
    elif path == 'users':
        user_id = request.args.get('user_id')
        if user_id:
            user = User(user_id=user_id).get_user_by_id()
            return jsonify({
                'user_id': user[0],
                'name': user[1],
                'username': user[2],
                'role': user[4]
            })
    elif path == 'report':
        orders = Order()
        month = request.args.get('month')
        chart = orders.get_month_sales(month=month)
        total_sales = []
        total_order = []
        total_sold = []
        for item in chart:
            total_sales.append(item[0] / 1000)
            total_order.append(item[1])
            total_sold.append(item[2])
        return jsonify({
            'weeks': list(range(1, len(chart) + 1)),
            'total_sales': total_sales,
            'total_order': total_order,
            'total_sold': total_sold
        })
    else:
        pass
    return jsonify({})
