#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template,util

import urllib2,urllib

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/login.html',dict()))

class BrowserIDHandler(webapp.RequestHandler):
    def post(self):
        data = {
            "assertion" : self.request.get('assertion'),
            "audience" : "localhost"
        }
        req = urllib2.Request('https://browserid.org/verify',urllib.urlencode(data))        
        html = urllib2.urlopen(req).read()
        self.response.out.write(html)

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/login', BrowserIDHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
