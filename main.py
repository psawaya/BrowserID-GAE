#!/usr/bin/env python

import gaesessions

from google.appengine.ext import db,webapp
from google.appengine.ext.webapp import template,util

try:
    import json
except ImportError:
    from django.utils import simplejson as json

import logging

import urllib2,urllib

from uuid import uuid4

class UserObj(db.Model):
    email = db.StringProperty()
    hampshireStudent = db.BooleanProperty()

class MainHandler(webapp.RequestHandler):
    def get(self):
        if gaesessions.get_current_session().is_active():
            # User is already logged in, don't bother showing login page.
            return self.redirect('/home')
        self.response.out.write(template.render('templates/login.html',dict()))

class BrowserIDHandler(webapp.RequestHandler):
    def post(self):
        session = gaesessions.get_current_session()
        if session.is_active():
            return self.response.out.write(json.dumps({
                'error' : 'Already logged in!'
            }))
        data = {
            "assertion" : self.request.get('assertion'),
            "audience" : urllib2.Request(self.request.url).get_host()
        }
        req = urllib2.Request('https://browserid.org/verify',urllib.urlencode(data))        
        json_result = urllib2.urlopen(req).read()
        
        # Parse the JSON to extract the e-mail
        result = json.loads(json_result)
        userEmail = result.get('email')
        UserObj.get_or_insert(userEmail, email = userEmail, hampshireStudent = userEmail.endswith('hampshire.edu'))
        session['email'] = userEmail
        
        self.response.out.write(json_result)

class HomeHandler(webapp.RequestHandler):
    def get(self):
        session = gaesessions.get_current_session()
        if session.is_active():
            sessionEmail = session.get('email')
            if sessionEmail:
                thisUser = UserObj.get_by_key_name(sessionEmail)
            if thisUser is None or sessionEmail is None:
                # If the user's session doesn't correspond to an e-mail in the database,
                # it's bad and needs to be terminated.
                session.terminate()
                return self.response.out.write("Invalid cookie!")
            else:
                return self.response.out.write(template.render('templates/home.html',{ 'user' : thisUser}))
        else:
            # User doesn't have a session/is expired, have them sign in again
            self.redirect('/')
 
class LogoutHandler(webapp.RequestHandler):
    def get(self):
        session = gaesessions.get_current_session()
        if session.is_active():
            session.terminate()
        self.redirect('/')

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/login', BrowserIDHandler),
                                        ('/home', HomeHandler),
                                        ('/logout', LogoutHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
