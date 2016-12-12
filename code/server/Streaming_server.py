from flask import Flask
from flask import Response

import sys
import time
from threading import Condition
from threading import Thread


from deploy import staging

def staging():
    for i in range(0, 8):
        time.sleep(1)
        print >>sys.stderr, 'getting to %s' % i
        print i

class PipeIO(object):

    def __init__(self):
        self.monitor = Condition()
        self.open = True
        self.bytes = ""

    def __iter__(self):
        return self

    def next(self):
        if not self.bytes and not self.open:
            print >>sys.stderr, 'over'
            raise StopIteration()
        self.monitor.acquire()
        self.monitor.wait()
        bytes = self.bytes
        self.bytes = ""
        self.monitor.release()
        return bytes
            

    def write(self, bytes):
        self.monitor.acquire()
        self.bytes += bytes
        self.monitor.notify()
        self.monitor.release()

    def close(self):
        self.monitor.acquire()
        print >>sys.stderr, 'closing'
        self.open = False
        self.monitor.notify()
        self.monitor.release()


class Runner(Thread):
    def __init__(self, func, stdout):
        super(Runner, self).__init__()
        self.func = func
        self.stdout = stdout

    def run(self):
        sys.stdout = self.stdout
        self.func()
        sys.stdout = sys.__stdout__
        self.stdout.close()

app = Flask(__name__)

@app.route('/de/staging/')
def de_staging():
    pipe = PipeIO()
    runner = Runner(staging, stdout=pipe)
    runner.start()

    return Response(pipe, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
