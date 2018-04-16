# coding: utf-8
import cgi
import datetime
import urllib
import wsgiref.handlers
import random
import os

from google.appengine.ext import db
import models
# from google.appengine.api import users
from google.appengine.ext.webapp import template
import ghost_vault
import webapp2
import sys
from webapp2_extras import security
from webapp2_extras import sessions

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
        # self.session['currentuser'] = 'testing'
        users = db.Query(models.User)
        ghosts = db.Query(models.Ghost)
        path = os.path.join(os.path.dirname(__file__), 'mainpage.html')
        template_values = {
            'users': users,
            'ghosts': ghosts
            }
        current_user = self.session.get('current_user', None)
        if current_user:
            template_values['current_user'] = current_user
        self.response.out.write(template.render(path, template_values))

class Create_Account(webapp2.RequestHandler):
    def post(self):
        template_values = {}
        email = self.request.get('email_address')
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        password = self.request.get('password')
        assigned_ghost = get_unused_ghost()
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
                    'ghost': assigned_ghost
                }
            path = os.path.join(os.path.dirname(__file__), 'create-account.html')
            self.response.out.write(template.render(path, template_values))

def email_availability(email):
    users = db.Query(models.User).filter("email ==", email)
    if users:
        return False
    else:
        return True

class GhostList(webapp2.RequestHandler): # return a table of ghosts
    def get(self):
        ghost_entities = get_ghosts()
        path = os.path.join(os.path.dirname(__file__), 'ghost-list.html')
        template_values = {
            'ghosts': ghost_entities
        }
        return template.render(path, template_values)

class Login(BaseHandler): # log in page - will replace
    def post(self):
        template_values = {}
        email = self.request.get('email_address')
        password = self.request.get('password')
        # password_hash = generate_password_hash(password)
        users = db.Query(models.User).fetch(None)
        # matching_users = users.filter(lambda x: security.check_password_hash(password, x.password))
        if(len(users)):
            matching_user = filter(lambda x: security.check_password_hash(password, x.password) and email == x.email, users)[0]
            template_values = {'user': matching_user}
            self.session['current_user'] = {'email': matching_user.email, 'ghost': matching_user.ghost.name}
        path = os.path.join(os.path.dirname(__file__), 'login.html')
        self.response.out.write(template.render(path, template_values))
        # self.MainPage.get()

class Logout(BaseHandler):
    def post(self):
        self.session['current_user'] = {}
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'logout.html')
        self.response.out.write(template.render(path, template_values))


def get_unused_ghost():
    ghost_entities = get_ghosts().filter('taken = ', False).fetch(None)
    if len(ghost_entities) > 0:
        return ghost_entities[random.randint(0, len(ghost_entities))]
    else:
        return undefined

def get_ghosts():
    ghosts_result = db.Query(models.Ghost)
    if(ghosts_result.get() == None):
    # Add ghosts to the db
        store_ghosts()
        # get_ghosts()
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
    ('/', MainPage),
    ('/create-account', Create_Account),
    ('/ghost-list', GhostList),
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
