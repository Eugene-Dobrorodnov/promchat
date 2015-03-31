from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user = self.get_secure_cookie('username')
        if user:
            user = user.decode('utf-8')
        return user

    def raise_404(self):
        self.clear()
        self.set_status(404)
        self.render("404.html")
