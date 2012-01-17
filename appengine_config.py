from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
    # Generate your own cookie_key!
    # You can do so by running this (in the terminal, not in your code here):
    #   from uuid import uuid4
    #   print str(uuid4().hex+uuid4().hex)
    app = SessionMiddleware(app, cookie_key="c184345987404d23b8cc796b890cb3b7e2d527758ccd4f658c6162350fbb8473", cookie_only_threshold = 0)
    return app