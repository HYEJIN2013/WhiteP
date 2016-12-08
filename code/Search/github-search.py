#!/usr/bin/env python

import requests
import sys 

from termcolor import colored


if len(sys.argv) != 2:
    print "Usage {0} KEYWORD"
    sys.exit(1)

url = 'https://api.github.com/search/repositories?q={0}'.format(sys.argv[1])

r = requests.get(url)
if r.status_code == 200:
    result = r.json()
    if result['total_count'] != 0:
        for record in result['items']:
            print colored("----- {0} -----".format(record['name']), 'red') 
            if record['description']:
                print record['description']
            print colored(record['url'], 'blue')
            print colored(record['clone_url'], 'blue')
            print
