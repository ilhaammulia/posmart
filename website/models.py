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
            self.open_db()
            self.cursor.execute(query)
            self.db.commit()
        except:
            pass
        finally:
            self.close_db()

    def create_db(self):
        try:
            self.open_db()
            self.__create_table__(
                'CREATE TABLE user(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100), username VARCHAR(20), password VARCHAR(32), role VARCHAR(5))')
            self.__create_table__(
                'CREATE TABLE product(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), category VARCHAR(50), price INT(30), stocks INT(50), img VARCHAR(255))')
            self.db.commit()
            self.check_admin()
            self.close_db()
        except:
            pass

    def check_admin(self):
        try:
            self.cursor.execute('SELECT * FROM user')
            users = self.cursor.fetchall()
            if not users:
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
            self.cursor.execute("INSERT INTO user(name, username, password, role) VALUES ('%s', MD5('%s'), '%s')" % (
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
            return None

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

    def update_product(self, data):
        try:
            self.open_db()
            self.cursor.execute(
                "UPDATE product SET name='%s', category='%s', price='%s', stocks='%s', img='%s' WHERE id='%s'" % data)
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
