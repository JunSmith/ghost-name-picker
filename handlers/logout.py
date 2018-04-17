from google.appengine.ext.webapp import template
from webapp2_extras import sessions
from base import BaseHandler
from utils.path_setter import set_path

class Logout(BaseHandler):
    def post(self):
        self.session['current_user'] = {}
        template_values = {}
        path = set_path('logout.html')
        self.response.out.write(template.render(path, template_values))
