from datetime import datetime
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.wsgi import login
from flask_login import UserMixin

@login.user_loader
def load_user(userid):
    return User.query.get(int(userid))


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(16), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    keys = db.relationship('Key', backref='creator', lazy='dynamic')

    def __repr__(self):
        return '<User {userid}: {username}>'.format(
            userid=self.user_id,
            username=self.user_name)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_id(self):
        return self.user_id
