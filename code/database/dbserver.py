#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import with_statement
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler

from urlparse import parse_qs
from urllib import unquote
import re

import json


# Base class for our server's responses.
class Response(object):
    status_code = 200
    body = '200 - OK'
    content_type = 'text/plain'

    def __init__(self, **kwargs):
        if 'body' in kwargs:
            self.body = kwargs.pop('body')

        if 'status_code' in kwargs:
            self.status_code = kwargs.pop('status_code')

        if 'content_type' in kwargs:
            self.content_type = kwargs.pop('content_type')


class ResponseBadRequest(Response):
    # Returned when the request could not be understood due to 
    # unexpected syntax.
    status_code = 400
    body = '400 - Bad Request'

class ResponseNotFound(Response):
    # Returned when the given key was not found on the database.
    status_code = 404
    body = '404 - Not Found'



# This class is just a simple wrapper of a dict object
class DatabaseServer(object):

    data = {}

    def __init__(self, file_name='data_json'):
        self.file_name = file_name

        with open(self.file_name, "r") as f:
            try:
                self.data = json.load(f)
            except ValueError:
                self.data = {}

    def set(self, key, value):
        self.data[key] = value

        with open(self.file_name, "w+") as f:
            json.dump(self.data, f)

    def get(self, key):
        return self.data.get(key)


# This class will handle the HTTP requests received by this server.
class DatabaseServerHTTPRequestHandler(BaseHTTPRequestHandler):

    database = DatabaseServer()

    # Handles the HTTP GET Method.
    def do_GET(self):
        
        # The path (querystring) must match the regular expression:
        qs_regex = r'^/(set|get)\?\w+=[%\w]+$'
        matches = re.search(qs_regex, self.path)

        if matches:
            # Gets the name of the action.
            action_name = matches.groups()[0]
            
            # Now, we parse the query string, removing from it the action's
            # name, the forward slash, and the question sign. 
            qs_dict = parse_qs(self.path[len(action_name) + 2:])

            # Dynamically call the method by name, passing it the querystring dict.
            try:
                response = getattr(self, 'do_' + action_name)(qs_dict)
            except KeyError:
                # If the call raises a KeyError, an expected attribute in the 
                # query string was not found.
                response = ResponseBadRequest()
        else:
            # If the path does not match, return a bad request.
            response = ResponseBadRequest()

        self.respond(response)


    def do_set(self, qs_dict):
        # In this case, the arguments dictionary contains a single key and a value
        # associated with it. Due to the way parse_qs returns its result, the value 
        # is stored in the value of this key as a list object.

        # Get the first key
        key = qs_dict.keys()[0]

        # The first value associated with that key
        value = qs_dict[key][0]

        # The value is URL-encoded, so we must decode it.
        value = unquote(value)

        # Set it in the database server.
        self.database.set(key, value)

        return Response()

    def do_get(self, qs_dict):
        # In this case, the arguments dictionary has a single key 'key'
        # with a value of the actual key that we want to retrieve.
        key = qs_dict['key'][0]
        value = self.database.get(key)

        if not value:
            # Value not found? Send a 404 response.
            return ResponseNotFound()
        else:
            return Response(body=value)

    def respond(self, response):
        # Send the response headers: Status code and content-type.
        self.send_response(response.status_code)
        self.send_header('Content-type', response.content_type)
        self.end_headers()
        # Send the actual response's body.
        self.wfile.write(response.body)
        self.wfile.close()

if __name__ == '__main__':
    port = 4000
    request_handler = DatabaseServerHTTPRequestHandler
    httpd = SocketServer.TCPServer(('', port), request_handler)
    print 'database serving at port', port
    httpd.serve_forever()
