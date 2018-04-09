from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from app.models.keys import Key
from flask_login import current_user


class KeyForm(FlaskForm):
    keyname = StringField('Key name', validators=[DataRequired()])
    keyvalue = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_keyname(self, keyname):
        key = Key.query.filter_by(key_name=keyname.data,
                                  user_id=current_user.user_id).first()
        if key is not None:
            raise ValidationError('A key with that name already exists in your keys.')
