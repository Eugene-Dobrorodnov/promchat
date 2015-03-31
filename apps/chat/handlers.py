from sqlalchemy.orm.exc import NoResultFound
from tornado.web import authenticated
from tornado.websocket import WebSocketHandler

from apps.common.mixins import BaseHandler
from apps.chat.forms import RoomForm
from apps.chat.models import Room


class RoomListHandler(BaseHandler):

    @authenticated
    def get(self):
        form = RoomForm()
        rooms = self.db.query(Room).all()
        self.render('rooms_list.html', user=self.current_user, rooms=rooms, form=form)

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
        self.render('room_detail.html', room=room, rooms=rooms)


class WebSocketHandler(BaseHandler, WebSocketHandler):
    connections = set()

    def open(self):
        WebSocketHandler.connections.add(self)

    def on_close(self):
        WebSocketHandler.connections.remove(self)

    def on_message(self, msg):
        self.send_messages(msg)

    def send_messages(self, msg):
        for conn in self.connections:
            conn.write_message({'name': self.current_user, 'msg': msg})
