from flask import Flask
from flask import request as req
from manager import MapPlayerManager, GameMaster

app = Flask(__name__)
manager = MapPlayerManager()
gm = GameMaster()

@app.route('/')
def index():
    return 'SABAEval GAME!'

@app.route('/admin')
def admin():
    return app.send_static_file('admin.html')

@app.route('/add')
def add():
    args = req.args
    name, pid = args.get('name'), args.get('pid')
    if manager.add(name, pid):
        return 'OK'
    else:
        return 'NG'

@app.route('/list')
def list():
    return str(manager.get_list())

@app.route('/kill')
def kill():
    args = req.args
    if manager.kill(args.get('killer_pid'), args.get('killed_pid')):
        return 'OK'
    else:
        return 'NG'

@app.route('/resurrect')
def resurrect():
    args = req.args
    if manager.resurrect(args.get('pid')):
        return 'OK'
    else:
        return 'NG'

@app.route('/start')
def start():
    gm.getready()
    return 'Started.'

@app.route('/isready')
def isready():
    return str(gm.is_ready())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
