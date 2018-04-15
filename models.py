
from google.appengine.ext import db

class Ghost(db.Model):
    name = db.StringProperty()
    description = db.StringProperty(multiline = True)
    taken = db.BooleanProperty(default = False)

class User(db.Model):
    email = db.EmailProperty(required=True)
    name = db.StringProperty()
    password = db.StringProperty()
    ghost = db.ReferenceProperty(Ghost)
