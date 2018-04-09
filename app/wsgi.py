import os
from flask import Flask
from dotenv import load_dotenv
from app.db import db, migrate, db_healthcheck
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

load_dotenv(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..', '.env'
        )
    )
)
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URI = os.environ.get('DATABASE_URI')

if not SECRET_KEY:
    raise RuntimeError('Error starting the Flask-App server:'
                       'Please run `export SECRET_KEY=<some_secret_key>`'
                       'before starting the server.')

if not DATABASE_URI:
    raise RuntimeError('Error starting the Flask-App server:'
                       'Please specify the database connection string '
                       'for the app to connect to:  '
                       '`export DATABASE_URI=<some_db_uri>`'
                       'before starting the server.')

login = LoginManager()
bootstrap = Bootstrap()

def create_app(**config):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    app.config.update(**config)
    db_healthcheck()
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'
    bootstrap.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.keys import bp as keys_bp
    app.register_blueprint(keys_bp, url_prefix='/keys')

    return app


from app import models
