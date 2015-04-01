from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from tornado.web import authenticated
from tornado.websocket import WebSocketHandler

from apps.common.mixins import BaseHandler
from apps.registration.models import User
from apps.chat.forms import RoomForm
from apps.chat.models import Room, Message


class RoomListHandler(BaseHandler):

    @authenticated
    def get(self):
        form = RoomForm()
        rooms = self.db.query(Room).all()
        data = {
            'user': self.current_user,
            'rooms': rooms,
            'form': form,
            'room': None
        }
        self.render('rooms_list.html', **data)

    @authenticated
    def post(self, *args, **kwargs):
        form = RoomForm(self.request.arguments, db_session=self.db)
        if form.validate():
            obj = form.save()
            print obj
        else:
            rooms = self.db.query(Room).all()
            self.render('rooms_list.html', form=form, rooms=rooms)


class RoomDetailHandler(BaseHandler):

    @authenticated
    def get(self, room_id):
        try:
            room = self.db.query(Room).filter_by(id=room_id).one()
        except NoResultFound:
            self.raise_404()

        rooms = self.db.query(Room).all()
        form = RoomForm()
        self.render('room_detail.html', room=room, rooms=rooms, form=form)


class WebSocketHandler(BaseHandler, WebSocketHandler):
    connections = set()

    def open(self, room):

        if not room or not self.db.query(Room).filter_by(id=room).scalar():
            self.write_message({'error': 1, 'textStatus': 'Error: No room specified'})
            self.close()
            return

        self.room = room
        WebSocketHandler.connections.add(self)

        # Load all messages in this room
        messages = self.db.query(Message).filter_by(room_id=self.room).order_by(desc('created_at'))
        result_html = self.render_string('msg.html', messages=messages)
        self.write_message({'html': result_html})

    def on_close(self):
        WebSocketHandler.connections.remove(self)

    def on_message(self, msg):

        try:
            user = self.db.query(User).filter_by(username=self.current_user).one()
            message = Message(user_id=user.id, room_id=self.room, messages=msg)
            self.db.add(message)
            self.db.commit()
        except NoResultFound:
            self.write_message({'error': 1, 'textStatus': 'Error: No such user'})
            self.close()
            return

        result_html = self.render_string('msg.html', messages=[message])
        self.send_messages(result_html)

    def send_messages(self, msg):
        for conn in WebSocketHandler.connections:
            if conn.room == self.room:
                conn.write_message({'html': msg})
