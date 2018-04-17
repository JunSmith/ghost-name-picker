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
