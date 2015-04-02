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
        data = {}
        form = RoomForm()
        q = self.request.arguments.get('q', None)

        if q and q[0]:
            rooms = self.db.query(Room).filter(Room.title.ilike('%' + q[0] + '%'))
            data.update({'q': q[0]})
        else:
            rooms = self.db.query(Room).all()
            data.update({'q': None})

        data.update({
            'user': self.current_user,
            'rooms': rooms,
            'form': form,
            'room': None
        })
        self.render('rooms_list.html', **data)

    @authenticated
    def post(self, *args, **kwargs):
        form = RoomForm(self.request.arguments, db_session=self.db)
        if form.validate():
            obj = form.save()
            redirect_url = '/room/{0}'.format(obj.id)
            self.redirect(redirect_url)
        else:
            rooms = self.db.query(Room).all()
            self.render('rooms_list.html', form=form, rooms=rooms, room=None, q=None)


class RoomDetailHandler(BaseHandler):

    @authenticated
    def get(self, room_id):
        try:
            room = self.db.query(Room).filter_by(id=room_id).one()
        except NoResultFound:
            self.raise_404()

        rooms = self.db.query(Room).all()

        data = {
            'room': room,
            'rooms': rooms
        }
        self.render('room_detail.html', **data)


class WebSocketHandler(BaseHandler, WebSocketHandler):
    connections = set()

    @authenticated
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

    @authenticated
    def on_close(self):
        WebSocketHandler.connections.remove(self)

    @authenticated
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

    @authenticated
    def send_messages(self, msg):
        for conn in WebSocketHandler.connections:
            if conn.room == self.room:
                conn.write_message({'html': msg})
