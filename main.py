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
import ghosts
import webapp2
import sys
import logging

reload(sys)
sys.setdefaultencoding('utf8')
class MainPage(webapp2.RequestHandler):
    def get(self):
        users = db.Query(models.User)
        ghosts = db.Query(models.Ghost)
        path = os.path.join(os.path.dirname(__file__), 'mainpage.html')
        template_values = {
            'users': users,
            'ghosts': ghosts
            }
        self.response.out.write(template.render(path, template_values))


class Claim(webapp2.RequestHandler):
    def post(self):
        template_values = {}
        email = self.request.get('email_address')
        name = self.request.get('name')
        password = self.request.get('password')
        assigned_ghost = get_unused_ghost()
        user = models.User(email = email, name = name, password = password)
        # user.put()
        if assigned_ghost:
            assign_ghost(assigned_ghost, user)
            template_values = {
                'user': user,
                'ghost': assigned_ghost
            }
        # else:
            # route for error / ghost unavailable
        path = os.path.join(os.path.dirname(__file__), 'claim.html')
        self.response.out.write(template.render(path, template_values))

def assign_ghost(ghost, user):
    ghost.taken = True
    ghost.put()
    user.ghost = ghost
    user.put()

class GhostList(webapp2.RequestHandler): # return a table of ghosts
    def get(self):
        ghost_entities = get_ghosts()
        path = os.path.join(os.path.dirname(__file__), 'ghost-list.html')
        template_values = {
            'ghosts': ghost_entities
        }
        return template.render(path, template_values)
        # self.response.out.write(template.render(path, template_values))
        # self.response.out.write("<html><body><table>")
        # for ghost in ghost_entities:
        #     self.response.out.write("<tr><td>%s</td><td>s</td>" % ghost.name )
        # self.response.out.write("</table></body></html>")

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
    for ghost in ghosts.get_ghosts():
        ghost_entity = models.Ghost(name =  ghost.keys()[0], description = ghost.values()[0])
        ghost_entity.put()

def init_ghosts():
    ghosts_result = db.Query(models.Ghost)
    if(ghosts_result.get() == None):
        store_ghosts()

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/claim', Claim),
    ('/ghost-list', GhostList)
], debug = True)

init_ghosts()

def main():
    application.RUN()

if __name__ == '__main__':
    main()
