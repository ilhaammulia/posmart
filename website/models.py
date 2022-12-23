from .database import *
import pymysql


class DBModel:
    db = None
    cursor = None

    def open_db(self):
        self.db = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.db.cursor()

    def close_db(self):
        self.db.close()

    def __create_table__(self, query):
        try:
            self.cursor.execute(query)
        except:
            pass

    def create_db(self):
        try:
            self.open_db()
            self.__create_table__(
                'CREATE TABLE user(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100), username VARCHAR(20), password VARCHAR(32), role VARCHAR(5))')
            self.__create_table__(
                'CREATE TABLE product(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), category VARCHAR(50), price INT(30), stocks INT(50), img VARCHAR(255))')
            self.__create_table__(
                'CREATE TABLE orders(id INT PRIMARY KEY AUTO_INCREMENT, reference_id INT(30), date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, total_bill INT(30), total_paid INT(30), total_change INT(30), payment_method VARCHAR(20))')
            self.__create_table__(
                'CREATE TABLE product_sold(id INT PRIMARY KEY AUTO_INCREMENT, reference_id INT(30), product_id INT, product_qty INT(30), product_price INT(30), FOREIGN KEY (product_id) REFERENCES product(id))')
            self.db.commit()
            self.check_admin()
            self.close_db()
        except:
            pass

    def check_admin(self):
        try:
            self.cursor.execute('SELECT * FROM user')
            users = self.cursor.fetchall()
            if not len(users):
                self.cursor.execute(
                    'INSERT INTO user(name, username, password, role) VALUES ("Administrator", "admin", MD5("password"), "admin")')
                self.db.commit()
        except:
            pass


class User(DBModel):
    def __init__(self, user_id=None, name=None, username=None, password=None, role=None):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password
        self.role = role
        self.is_logged_in = False

    def login(self):
        try:
            self.open_db()
            self.cursor.execute(
                "SELECT * FROM user WHERE username='%s' AND password=MD5('%s')" % (self.username, self.password))
            user = self.cursor.fetchone()
            if user:
                self.user_id = user[0]
                self.name = user[1]
                self.username = user[2]
                self.role = user[4]
                self.is_logged_in = True
            self.close_db()
        except:
            pass

    def create_user(self):
        try:
            self.open_db()
            self.cursor.execute("INSERT INTO user(name, username, password, role) VALUES ('%s', '%s', MD5('%s'), '%s')" % (
                self.name, self.username, self.password, self.role))
            self.db.commit()
            self.close_db()
            return True
        except:
            return False

    def get_all_user(self):
        try:
            self.open_db()
            self.cursor.execute('SELECT * FROM user')
            users = self.cursor.fetchall()
            self.close_db()
            return users
        except:
            return ()

    def get_user_by_id(self):
        try:
            self.open_db()
            self.cursor.execute(
                "SELECT * FROM user WHERE id='%s'" % (self.user_id))
            user = self.cursor.fetchone()
            return user
        except:
            return None

    def update_user(self, data):
        try:
            self.open_db()
            if len(data) == 5:
                query = "UPDATE user SET name='%s', username='%s', password=MD5('%s'), role='%s' WHERE id='%s'"
            else:
                query = "UPDATE user SET name='%s', username='%s', role='%s' WHERE id='%s'"
            self.cursor.execute(query % data)
            self.db.commit()
            self.close_db()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_user(self):
        try:
            self.open_db()
            self.cursor.execute(
                "DELETE FROM user WHERE id='%s'" % (self.user_id))
            self.db.commit()
            return True
        except:
            return False


class Product(DBModel):
    def __init__(self, product_id=None, name=None, category=None, price=0, stocks=0, img=None):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stocks = stocks
        self.img = img

    def create_product(self):
        try:
            self.open_db()
            self.cursor.execute(
                "INSERT INTO product(name, category, price, stocks, img) VALUES ('%s', '%s', '%s', '%s', '%s')" % (self.name, self.category, self.price, self.stocks, self.img))
            self.db.commit()
            self.close_db()
            return True
        except:
            return False

    def get_all_products(self):
        try:
            self.open_db()
            self.cursor.execute("SELECT * FROM product")
            products = self.cursor.fetchall()
            self.close_db()
            return products
        except:
            return ()

    def get_product_by_id(self):
        try:
            self.open_db()
            self.cursor.execute(
                "SELECT * FROM product WHERE id='%s'" % (self.product_id))
            product = self.cursor.fetchone()
            self.close_db()
            return product
        except:
            return ()

    def get_product_by_category(self, category):
        try:
            self.open_db()
            self.cursor.execute(
                "SELECT * FROM product WHERE category='%s'" % (category))
            products = self.cursor.fetchall()
            self.close_db()
            return products
        except:
            return ()

    def update_product(self, data):
        try:
            self.open_db()
            self.cursor.execute(
                "UPDATE product SET name='%s', category='%s', price='%s', stocks='%s' WHERE id='%s'" % data)
            self.db.commit()
            self.db.close()
            return True
        except:
            return False

    def update_stock(self, new_stock):
        try:
            self.open_db()
            self.cursor.execute(
                "UPDATE product SET stocks='%s' WHERE id='%s'" % (new_stock, self.product_id))
            self.db.commit()
            self.db.close()
            return True
        except:
            return False

    def delete_product(self):
        try:
            self.open_db()
            self.cursor.execute(
                "DELETE FROM product WHERE id='%s'" % (self.product_id))
            self.db.commit()
            return True
        except:
            return False


class Order(DBModel):
    def __init__(self, reference_id=None, total_bill=0, total_paid=0, total_change=0, payment_method=None):
        self.reference_id = reference_id
        self.total_bill = total_bill
        self.total_paid = total_paid
        self.total_change = total_change
        self.payment_method = payment_method

    def create_order(self):
        try:
            self.open_db()
            self.cursor.execute(
                "INSERT INTO orders(reference_id, total_bill, total_paid, total_change, payment_method) VALUES ('%s', '%s', '%s', '%s', '%s')" % (self.reference_id, self.total_bill, self.total_paid, self.total_change, self.payment_method))
            self.db.commit()
            self.close_db()
            return True
        except:
            return False

    def get_all_order(self):
        try:
            self.open_db()
            self.cursor.execute("SELECT * FROM orders")
            orders = self.cursor.fetchall()
            self.close_db()
            return orders
        except:
            return ()

    def get_today_order(self):
        try:
            self.open_db()
            self.cursor.execute(
                "SELECT * FROM orders WHERE DATE(date) = DATE(NOW())")
            orders = self.cursor.fetchall()
            self.close_db()
            return orders
        except:
            return ()

    def get_month_sales(self, month=None):
        try:
            self.open_db()
            if month:
                self.cursor.execute(
                    "SELECT CAST(SUM(O.total_bill) AS SIGNED) total_bills, COUNT(O.id), CAST(SUM(PS.product_qty) AS SIGNED) product_qty FROM orders O, product_sold PS WHERE PS.reference_id = O.reference_id AND  MONTH(date) = '%s' GROUP BY WEEK(date)" % (month))
            else:
                self.cursor.execute(
                    "SELECT CAST(SUM(O.total_bill) AS SIGNED) total_bills, COUNT(O.id), CAST(SUM(PS.product_qty) AS SIGNED) product_qty FROM orders O, product_sold PS WHERE PS.reference_id = O.reference_id AND  MONTH(date) = MONTH(NOW()) GROUP BY WEEK(date)")
            data = self.cursor.fetchall()
            self.close_db()
            return data
        except:
            return ()


class ProductSold(DBModel):
    def __init__(self, reference_id=None, items=[]):
        self.reference_id = reference_id
        self.items = items

    def create_sold(self):
        try:
            self.open_db()
            for item in self.items:
                self.cursor.execute(
                    "INSERT INTO product_sold(reference_id, product_id, product_qty, product_price) VALUES ('%s', '%s', '%s', '%s')" % (self.reference_id, item[0], item[1], item[2]))
            self.db.commit()
            self.close_db()
            return True
        except Exception as e:
            print(e)
            return False

    def get_today_by_reference_id(self):
        try:
            self.open_db()
            self.cursor.execute(
                "SELECT SUM(product_qty) FROM product_sold WHERE reference_id IN (SELECT reference_id FROM orders WHERE DATE(date) = DATE(NOW()))")
            products = self.cursor.fetchone()
            self.close_db()
            return products
        except:
            return ()

    def get_top_product(self):
        try:
            self.open_db()
            self.cursor.execute("SELECT P.name, SUM(PS.product_qty) AS sum_product FROM product P, product_sold PS, orders O WHERE O.reference_id = PS.reference_id AND PS.product_id = P.id AND MONTH(O.date) = MONTH(NOW()) GROUP BY PS.product_id ORDER BY sum_product DESC LIMIT 3")
            top_product = self.cursor.fetchall()
            self.close_db()
            return top_product
        except:
            return ()
