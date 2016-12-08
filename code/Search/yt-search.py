#!/usr/bin/python3

import urllib.request
import urllib.parse
import re
import sys

inargs = sys.argv
inargs.remove(inargs[0])
inargs = ' '.join(inargs)

query_string = urllib.parse.urlencode({"search_query" : inargs})
html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
print("http://www.youtube.com/watch?v=" + search_results[0])
