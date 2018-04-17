
from google.appengine.ext import db

class Ghost(db.Model):
    name = db.StringProperty(required=True)
    description = db.StringProperty(multiline = True)
    taken = db.BooleanProperty(default = False)

class User(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    password = db.StringProperty(required=True)
    ghost = db.ReferenceProperty(Ghost)
