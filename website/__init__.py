from flask import Flask


def create_app():
    global app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'posmartkey123'
    app.config['UPLOAD_FOLDER'] = 'static'
    app.config['MAX_CONTENT_PATH'] = 10 * 1024 * 1024

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .models import DBModel
    DBModel().create_db()

    return app
