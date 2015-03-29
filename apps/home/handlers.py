from tornado.web import RequestHandler


class MainHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render('base.html')
