from flask import Flask, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <html><head><title>HDMI switcher</title><style>
    .btn {
font-size: 20px;
  padding: 10px 20px 10px 20px;
margin: 40px;
     }
    </style></head>
    <body>
    <div>
	<form action="/click" method="POST">
		<input type="submit" value="Switch Port" class="btn"/>
	</form>
    </div>
    </body></html>
    """

@app.route('/click', methods=['POST'])
def click():
    os.system('sudo python click.py')
    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run('0.0.0.0')
