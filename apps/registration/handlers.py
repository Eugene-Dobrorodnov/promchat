from tornado.web import RequestHandler


class LoginHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render('registration/login.html')


class LogoutHandler(RequestHandler):

    def post(self):
        self.clear_all_cookies()
        self.redirect("/")
