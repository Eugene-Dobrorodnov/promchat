from tornado.web import RequestHandler
from apps.common.mixins import BaseHandler

from apps.registration.forms import SignupForm, LoginFrom


class RegistrationHandler(BaseHandler):

    def get(self):
        form = SignupForm()
        self.render('signup.html', form=form)

    def post(self, *args, **kwargs):
        form = SignupForm(self.request.arguments, db_session=self.db)

        if form.validate():
            obj = form.save()
            self.set_secure_cookie('username', str(obj.username))
            self.redirect('/')
        else:
            self.render('signup.html', form=form)


class LoginHandler(BaseHandler):

    def get(self, *args, **kwargs):
        form = LoginFrom()
        self.render('login.html', form=form)

    def post(self, *args, **kwargs):
        form = LoginFrom(self.request.arguments, db_session=self.db)

        if form.validate():
            self.set_secure_cookie('username', str(form.username.data))
            self.redirect('/')
        else:
            self.render('login.html', form=form)


class LogoutHandler(RequestHandler):

    def get(self):
        self.clear_all_cookies()
        self.redirect("/login")
