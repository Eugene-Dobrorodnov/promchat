from wtforms.validators import DataRequired, Length
from wtforms_tornado import Form
from wtforms import StringField, ValidationError

from apps.chat.models import Room


class RoomForm(Form):

    def __init__(self, *arg, **kwargs):
        self.db = kwargs.get('db_session', None)
        super(RoomForm, self).__init__(*arg, **kwargs)

    title = StringField('Title', validators=[DataRequired(), Length(max=30)])

    def validate_title(self, field):
        print self.db.query(Room).filter_by(title=field.data).scalar()
        if self.db.query(Room).filter_by(title=field.data).scalar():
            raise ValidationError('Room with that title already exists')

    def save(self):
        room = Room(title=self.title.data)
        self.db.add(room)
        self.db.commit()
        return room

