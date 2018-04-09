import time
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def db_healthcheck(retries=10):
    from app.wsgi import DATABASE_URI
    try:
        conn = psycopg2.connect(DATABASE_URI)
    except psycopg2.OperationalError as exc:
        if retries > 0:
            retries -= 1
            time.sleep(1)
            db_healthcheck(retries=retries)
        else:
            raise exc


db = SQLAlchemy()
migrate = Migrate()
