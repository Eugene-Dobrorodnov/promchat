from tornado.web import authenticated
from tornado.websocket import WebSocketHandler
from apps.common.mixins import BaseHandler


class ChatHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render('chat.html', user=self.current_user)


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
