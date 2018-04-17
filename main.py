# coding: utf-8
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import cgi
import urllib
import wsgiref.handlers
import random
import os
import models
import webapp2
import sys
import utils.ghost_catcher

from handlers.home import HomePage
from handlers.create_account import CreateAccount
from handlers.login import Login
from handlers.logout import Logout

reload(sys)
sys.setdefaultencoding('utf8')

config = {'webapp2_extras.sessions': {'secret_key': 'thisisas00p3rsp00pysecritkeyydontl0se1t'}}

application = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/create-account', CreateAccount),
    ('/login', Login),
    ('/logout', Logout)
],
config = config,
debug = True)

utils.ghost_catcher.catch()

def main():
    application.RUN()

if __name__ == '__main__':
    main()
