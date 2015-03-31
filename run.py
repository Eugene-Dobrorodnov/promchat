import os.path

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.auth
import tornado.gen
from tornado.options import define, options

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from apps.common.handlers import MainHandler
from apps.registration.handlers import LoginHandler, LogoutHandler, RegistrationHandler


# Options
define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, type=bool)
define("db_path", default='postgresql+psycopg2:///prom_chat', type=str)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/signup', RegistrationHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
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
        engine = create_engine(options.db_path, convert_unicode=True, echo=options.debug)
        self.db = scoped_session(sessionmaker(bind=engine))


def main():
    port = int(os.environ.get("PORT", 5000))
    app = Application()
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
