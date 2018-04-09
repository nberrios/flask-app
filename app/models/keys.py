from datetime import datetime
from app.db import db


class Key(db.Model):
    key_id = db.Column(db.Integer, primary_key=True)
    key_name = db.Column(db.String(32), index=True)
    key_value = db.Column(db.String(32), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Key: {key_name}, value: {key_value}, user_id: {user_id}>'.format(
            key_name=self.key_name,
            key_value=self.key_value,
            user_id=self.user_id)

    def get_id(self):
        return self.key_id
