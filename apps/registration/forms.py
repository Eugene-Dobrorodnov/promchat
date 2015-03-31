import hashlib

from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length
from wtforms_tornado import Form

from apps.registration.models import User


class SignupForm(Form):

    def __init__(self, *arg, **kwargs):
        self.db = kwargs.get('db_session', None)
        super(SignupForm, self).__init__(*arg, **kwargs)

    username = StringField('Username', validators=[DataRequired(), Length(max=30)])
    password = StringField('Password', validators=[DataRequired(), Length(max=30)])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), Length(max=30)])

    def validate_username(self, field):
        if self.db.query(User).filter_by(username=field.data).scalar():
            raise ValidationError('A user already exists')

    def validate_password(self, field):
        if self.confirm_password.data != field.data:
            raise ValidationError('Passwords do not match')

    def save(self):
        password = hashlib.sha1(repr(self.data['password'])).hexdigest()
        username = self.data['username']
        user = User(username=username, password=password)
        self.db.add(user)
        self.db.commit()
        return user


class LoginFrom(Form):

    def __init__(self, *arg, **kwargs):
        self.db = kwargs.get('db_session', None)
        super(LoginFrom, self).__init__(*arg, **kwargs)

    username = StringField('Username', validators=[DataRequired(), Length(max=30)])
    password = StringField('Password', validators=[DataRequired(), Length(max=30)])

    def validate_username(self, field):
        password = hashlib.sha1(repr(self.password.data)).hexdigest()

        if not self.db.query(User).filter_by(username=field.data, password=password).scalar():
            raise ValidationError('A user already exists')
