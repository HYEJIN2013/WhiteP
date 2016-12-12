def hello(environ, start_response):
    start_response('200 OK', [('Content-type','text/plain')])
    return ["Hello World!"]

# The Web Server Gateway Interface is a Python standard created in 2003 by Philip J. Eby
class Middleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

app = Middleware(hello)

from wsgiref import simple_server

httpd = simple_server.WSGIServer(
    ('0.0.0.0', 8000),
    simple_server.WSGIRequestHandler,
)
httpd.set_app(app)
httpd.serve_forever()
