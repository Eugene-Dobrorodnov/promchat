from apps.common.mixins import BaseHandler


class MainHandler(BaseHandler):

    def get(self, *args, **kwargs):
        if self.current_user:
            self.redirect('/chat')
        self.render('base.html')
