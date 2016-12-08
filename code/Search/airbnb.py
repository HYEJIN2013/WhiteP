"""
Sample specific search query to airbnb returning list of new flats (compared to last run) as stdout (meant to be used as crontab).
Copyright 2011 Domen Kozar. All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:
   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.
THIS SOFTWARE IS PROVIDED BY DOMEN KOZAR ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL DOMEN KOZAR OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of DOMEN KOZAR.
"""
import json
import pickle
import requests
from pprint import pprint


query = {
    'new_search': 'true',
    'search_view': '1',
    'min_bedrooms': '2',
    'min_bathrooms': '0',
    'min_beds': '2',
    'page': '1',
    'location': 'Barcelona, Spain',
    'checkin': '02/24/2012',
    'checkout': '07/01/2012',
    'quests': '2',
    'room_types[]': 'Entire home/apt',
    'sort': '4',
    'per_page': '21',
}

data = json.loads(resp.content)['properties']

flats = set()
for apartment in data:
    flats.add(apartment['id'])

try:
    p = pickle.load(open('airbnb_flats', 'r'))
except IOError:
    pass
else:
    for id_ in flats.difference(p):
        print 'http://www.airbnb.com/rooms/%s' % id_

pickle.dump(flats, open('airbnb_flats', 'w'))
