from google.appengine.ext import db
from google.appengine.ext.webapp import template
from webapp2_extras import security
import random
import os
import models
from base import BaseHandler
from utils.path_setter import set_path

class CreateAccount(BaseHandler):
    def post(self):
        template_values = {}
        email = self.request.get('email_address')
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        password = self.request.get('password')
        assigned_ghost_name = self.request.get('assigned_ghost')
        assigned_ghost = db.Query(models.Ghost).filter('name =', assigned_ghost_name).get()
        if email_availability(email):
            user = models.User(
                email = email,
                first_name = first_name,
                last_name = last_name,
                password = security.generate_password_hash(password))
            if assigned_ghost:
                assigned_ghost.taken = True
                assigned_ghost.put()
                user.ghost = assigned_ghost
                user.put()
                template_values = {
                    'user': user,
                    'ghost': assigned_ghost,
                    'email_taken': False
                }
                self.session['current_user'] = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'ghost': user.ghost.name}
        else:
            template_values = {
                'email': email,
                'email_taken': True
            }
        path = set_path('create-account.html')
        self.response.out.write(template.render(path, template_values))

def email_availability(email):
    users = db.Query(models.User).filter("email =", email).get()
    if users:
        return False
    else:
        return True
