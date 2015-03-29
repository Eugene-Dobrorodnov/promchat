import os.path

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.auth
import tornado.gen

from apps.home.handlers import MainHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
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


def main():
    port = int(os.environ.get("PORT", 5000))
    app = Application()
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
