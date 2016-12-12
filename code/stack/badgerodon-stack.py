import os
import redis
import uuid
from flask import Flask, redirect, request

# get config from the environment
redis_hostname = os.getenv("REDIS_HOSTNAME", "localhost")
port = int(os.getenv("PORT", "5000"))

# connect to redis
r = redis.StrictRedis(host=redis_hostname, port=6379, db=0)

# create our app
app = Flask(__name__)

# post to /links to create a link
@app.route("/links", methods=["POST"])
def put_link():
    if "url" in request.form:
        link_id = str(uuid.uuid4())
        r.set(link_id, request.form["url"])
        return link_id
    else:
        return "Expected URL", 400

# get /links/<link_id> to redirect to the saved url
@app.route("/links/<link_id>")
def links(link_id):
    url = r.get(link_id)
    if url:
        return redirect(url)
    else:
        return "Link Not Found", 404

# run the app
if __name__ == "__main__":
    app.debug = True
    app.run(port=port)
