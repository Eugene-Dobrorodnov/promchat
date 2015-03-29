from apps.common.mixins import BaseHandler


class MainHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render('base.html')
