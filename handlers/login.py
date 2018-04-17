from google.appengine.ext import db
from google.appengine.ext.webapp import template
from webapp2_extras import security, sessions
import models
from base import BaseHandler
from utils.path_setter import set_path

class Login(BaseHandler):
    def post(self):
        template_values = {}
        email = self.request.get('email_address')
        password = self.request.get('password')
        users = db.Query(models.User).fetch(None)
        if(len(users)):
            matching_users = filter(lambda x: security.check_password_hash(password, x.password) and email == x.email, users)
            matching_user = matching_users[0] if len(matching_users) > 0 else None
            if matching_user:
                template_values = {'user': matching_user}
                self.session['current_user'] = {
                    'first_name': matching_user.first_name,
                    'last_name': matching_user.last_name,
                    'email': matching_user.email,
                    'ghost': matching_user.ghost.name}
        path = set_path('login.html')
        self.response.out.write(template.render(path, template_values))
