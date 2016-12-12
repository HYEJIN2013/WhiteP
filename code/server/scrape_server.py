import urllib
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/scrape')
def scrape():
  sport = request.args['sport']

  html = urllib.urlopen("http://www.espn.com/" + sport).read()
  headlines = [headline.get_text() for headline in BeautifulSoup(html).find(class_="headlines").find_all('li')]

  return jsonify(results = headlines)

if __name__ == '__main__':
    app.run()
