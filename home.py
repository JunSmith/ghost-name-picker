from google.appengine.ext import db
from google.appengine.ext.webapp import template
from webapp2_extras import security, sessions
import cgi
import urllib
import wsgiref.handlers
import random
import os
import models
import ghost_vault
import webapp2
import sys
import main

class MainPage(main.BaseHandler):
    def get(self):
        users = db.Query(models.User)
        ghosts = db.Query(models.Ghost)
        user_ghosts = get_unused_ghosts()
        template_values = {
            'ghosts': ghosts,
            'available_ghosts': user_ghosts
            }
        if len(users.fetch(None)) > 0:
            template_values['users'] = users
        current_user = self.session.get('current_user', None)
        if current_user:
            template_values['current_user'] = current_user
        path = set_path('main-page.html')
        self.response.out.write(template.render(path, template_values))
