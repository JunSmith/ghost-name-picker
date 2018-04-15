# coding: utf-8
import cgi
import datetime
import urllib
import wsgiref.handlers
import random

from google.appengine.ext import db
from google.appengine.api import users
import ghosts
import webapp2
import sys
import logging

reload(sys)
sys.setdefaultencoding('utf8')

class Ghost(db.Model):
    name = db.StringProperty()
    description = db.StringProperty(multiline = True)
    taken = db.BooleanProperty(default = False)

class User(db.Model):
    email = db.EmailProperty(required=True)
    name = db.StringProperty()
    password = db.StringProperty()
    ghost = db.ReferenceProperty(Ghost)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("""
            <html><body>
                <form action="/claim" method="post">
                    <div><input type="email" name="email_address" ></input></div>
                    <div><input type="text" name="name"></input></div>
                    <div><input type="password" name="password"></input></div>
                    <div><input type="submit" value="Enter Your Name"></input></div>
                </form>
        """)
        users = db.Query(User)
        for user in users:
            user_ghost_name = user.ghost.name if user.ghost is not None else ""
            self.response.out.write("<b>%s</b><br/>" % user.email + " " + user.name + " " + user_ghost_name)
        self.response.out.write("</body></html>")

class Claim(webapp2.RequestHandler):
    def post(self):
        email = self.request.get('email_address')
        name = self.request.get('name')
        password = self.request.get('password')
        assigned_ghost = get_unused_ghost()
        self.response.out.write('<html><body>You wrote: ' + email + ' ' + name + ' ' + password)
        self.response.out.write('<br/>Your ghost is: ' + assigned_ghost.name)
        self.response.out.write('</body></html>')
        user = User(email = email, name = name, password = password)
        # user.put()
        assign_ghost(assigned_ghost, user)

def assign_ghost(ghost, user):
    ghost.taken = True
    ghost.put()
    user.ghost = ghost
    user.put()

class List(webapp2.RequestHandler):
    def get(self):
        ghost_entities = get_ghosts()
        self.response.out.write("<html><body><table>")
        for ghost in ghost_entities:
            self.response.out.write("<tr><td>%s</td><td>s</td>" % ghost.name )
        self.response.out.write("</table></body></html>")

def get_unused_ghost():
    ghost_entities = get_ghosts().filter('taken = ', False).fetch(None)
    return ghost_entities[random.randint(0, len(ghost_entities))]

def get_ghosts():
    ghosts_result = db.Query(Ghost)
    if(ghosts_result.get() == None):
    # Add ghosts to the db
        store_ghosts()
        # get_ghosts()
    else:
        return ghosts_result

def store_ghosts():
    for ghost in ghosts.get_ghosts():
        ghost_entity = Ghost(name =  ghost.keys()[0], description = ghost.values()[0])
        ghost_entity.put()

def init_ghosts():
    ghosts_result = db.Query(Ghost)
    if(ghosts_result.get() == None):
        store_ghosts()

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/claim', Claim),
    ('/list', List)
], debug = True)

init_ghosts()

def main():
    application.RUN()

if __name__ == '__main__':
    main()
