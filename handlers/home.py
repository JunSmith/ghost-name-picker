from google.appengine.ext import db
from google.appengine.ext.webapp import template
from webapp2_extras import security, sessions
import cgi
import urllib
import wsgiref.handlers
import random
import os
import models
import webapp2
import sys
from base import BaseHandler
from utils.path_setter import set_path

class HomePage(BaseHandler):
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

def get_unused_ghosts():
    ghost_entities = db.Query(models.Ghost).filter('taken = ', False).fetch(None)
    ghost_count = len(ghost_entities)
    if ghost_count > 0:
        selected_ghosts = []
        i = 0
        limit = 3 if ghost_count >= 3 else ghost_count
        while i < limit:
            selected_ghost = ghost_entities[random.randint(0, ghost_count - 1)]
            if selected_ghost not in selected_ghosts:
                i = i + 1
                selected_ghosts.append(selected_ghost)
        return selected_ghosts

    else:
        return undefined
