# coding: utf-8
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
import home

reload(sys)
sys.setdefaultencoding('utf8')

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class MainPage(BaseHandler):
    def get(self):
        users = db.Query(models.User)
        ghosts = db.Query(models.Ghost)
        user_ghosts = get_unused_ghosts()
        template_values = {
            # 'users': users,
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

class Create_Account(BaseHandler):
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
                self.session['current_user'] = {'first_name': matching_user.first_name, 'ghost': matching_user.ghost.name}
        path = set_path('login.html')
        self.response.out.write(template.render(path, template_values))

class Logout(BaseHandler):
    def post(self):
        self.session['current_user'] = {}
        template_values = {}
        path = os.path.join(*[os.path.dirname(__file__), 'templates', 'logout.html'])
        self.response.out.write(template.render(path, template_values))

def set_path(file_name):
    return os.path.join(*[os.path.dirname(__file__), 'templates', file_name])

def get_unused_ghosts():
    ghost_entities = get_ghosts().filter('taken = ', False).fetch(None)
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

def get_ghosts():
    ghosts_result = db.Query(models.Ghost)
    if(ghosts_result.get() == None):
        store_ghosts()
    else:
        return ghosts_result

def store_ghosts():
    for ghost in ghost_vault.get():
        ghost_entity = models.Ghost(name =  ghost.keys()[0], description = ghost.values()[0])
        ghost_entity.put()

def init_ghosts():
    ghosts_result = db.Query(models.Ghost)
    if(ghosts_result.get() == None):
        store_ghosts()

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

application = webapp2.WSGIApplication([
    ('/', home.MainPage),
    ('/create-account', Create_Account),
    ('/login', Login),
    ('/logout', Logout)
],
config = config,
debug = True)

init_ghosts()

def main():
    application.RUN()

if __name__ == '__main__':
    main()
