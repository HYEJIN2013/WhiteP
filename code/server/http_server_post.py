from sys import version as python_version
from cgi import parse_header, parse_multipart

if python_version.startswith('3'):
    from urllib.parse import parse_qs
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from urlparse import parse_qs
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def do_POST(self):
        postvars = self.parse_POST()
        body = 'OK'
        print postvars
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

server = HTTPServer(('', 8081), RequestHandler)
server.serve_forever()

# test with:
# curl -d "param1=value1&param2=value2" http://localhost:8081
