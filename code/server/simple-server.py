#!/usr/bin/env python2
import BaseHTTPServer
import SocketServer
from StringIO import StringIO
import random
import urllib2 as urllib
import shutil


class Main(BaseHTTPServer.BaseHTTPRequestHandler):

    def version_string(self):
        return '!@#$!@#$'

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if not self.path[:5] == '/http':
            print self.path[:5]
            return
        url = self.path[1:]
        self.download(url)

    def download(self, url):
        req = urllib.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT'
                       ' 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR'
                       ' 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0')
        r = urllib.urlopen(req)
        self.wfile.write(r.read())

# rand = lambda max: int(100000 * random.random() % max)
PORT = 3045


httpd = SocketServer.TCPServer(("", PORT), Main)
httpd.serve_forever()
