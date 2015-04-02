import os.path

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.auth
import tornado.gen
from tornado.options import define, options

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from apps.settings import Settings
from apps.common.handlers import MainHandler
from apps.registration.handlers import LoginHandler, LogoutHandler, RegistrationHandler
from apps.chat.handlers import RoomListHandler, WebSocketHandler, RoomDetailHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/signup', RegistrationHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/rooms', RoomListHandler),
            (r'^/room/(\d+)/?$', RoomDetailHandler),
            #(r'/ws', WebSocketHandler),
            (r"/ws/(\d+)/?$", WebSocketHandler),
        ]
        settings = dict(
            cookie_secret="your_cookie_secret",
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            static_url_prefix='/static/',
            login_url='/',
            xsrf_cookies=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        engine = create_engine(Settings.DB_PATCH, convert_unicode=True)
        self.db = scoped_session(sessionmaker(bind=engine))


def main():
    port = int(os.environ.get("PORT", 5000))
    app = Application()
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
