import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
import webapp2

class Ghost(db.Model):
    name = db.StringProperty()
    description = db.StringProperty(multiline = True)

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
        #users = db.Query("SELECT * FROM User LIMIT 10")
        users = db.Query(User)
        for user in users:
            self.response.out.write("<b>%s</b><br/>" % user.email + " " + user.name) 
        self.response.out.write("</body></html>")
        
class Claim(webapp2.RequestHandler):
    def post(self):
        #self.response.out.write('<html><body>You wrote: <pre>')
        #self.response.out.write(cgi.escape(self.request.get('content')))
        #self.response.out.write('</body></html>')
        email = self.request.get('email_address')
        name = self.request.get('name')
        password = self.request.get('password')
        self.response.out.write('<html><body>You wrote: ' + email + ' ' + name + ' ' + password + '</body></html>')
        user = User(email = email, name = name, password = password)
        user.put()

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/claim', Claim)
], debug = True)

def main():
    application.RUN()

if __name__ == '__main__':
    main()
