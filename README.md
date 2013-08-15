BrowserID on App Engine 
-----------------------

This is a very simple example of how to get up and running with [BrowserID](http://persona.org) on [Google App Engine](http://code.google.com/appengine/).

It stores a user's login in a session, via [gaesessions](https://github.com/dound/gae-sessions).

This was developed as part of [CS206](http://hampshire.edu/~pedcs/classes/cs206January12/) at Hampshire College, which is why the example provided verifies whether or not you're a Hampshire student.

__Make sure to modify the secret cookie_key in appengine_config.py before deploying!__