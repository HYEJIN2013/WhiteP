import threading
import Queue
import random, time
import os, psutil

import gevent
import gevent.queue

proc = None

class ProducerLocal(threading.Thread):
    def __init__(self):
        super(ProducerLocal, self).__init__()
        self.queue = Queue.Queue()
        self.stopped = False

    def run(self):
        while not self.stopped:
            self.queue.put(1)
            time.sleep(random.random() * 4)

def consumer_remote():
    producers = [ProducerLocal() for _ in xrange(4)]

    print('initial cpu usage: %f' % get_cpu_usage())
    t = time.time()
    c = time.clock()

    for p in producers:
        p.start()

    print('startup took %f seconds, clock: %f, cpu usage: %f' % (time.time() - t, time.clock() - c, get_cpu_usage()))
    t = time.time()
    c = time.clock()

    cnt = 0
    while cnt < 30:
        for p in producers:
            try:
                while cnt < 30:
                    cnt += p.queue.get_nowait()
            except Queue.Empty:
                pass

    print('consuming 30 values took %f seconds, clock: %f, cpu usage: %f' % (time.time() - t, time.clock() - c, get_cpu_usage()))
    t = time.time()
    c = time.clock()

    for p in producers:
        p.stopped = True

    for p in producers:
        p.join()

    print('shutdown took %f seconds, clock: %f, cpu usage: %f' % (time.time() - t, time.clock() - c, get_cpu_usage()))
    

class ProducerRemote(threading.Thread):
    def __init__(self, queue):
        super(ProducerRemote, self).__init__()
        self.queue = queue
        self.stopped = False

    def run(self):
        while not self.stopped:
            self.queue.put(1)
            time.sleep(random.random() * 4)

def consumer_local(block):
    queue = Queue.Queue()
    producers = [ProducerRemote(queue) for _ in xrange(4)]

    if block:
        queue_getter = queue.get
    else:
        queue_getter = queue.get_nowait
    
    print('initial cpu usage: %f' % get_cpu_usage())
    t = time.time()
    c = time.clock()

    for p in producers:
        p.start()

    print('startup took %f seconds, clock: %f, cpu usage: %f' % (time.time() - t, time.clock() - c, get_cpu_usage()))
    t = time.time()
    c = time.clock()

    cnt = 0
    while cnt < 30:
        try:
            cnt += queue_getter()
        except Queue.Empty:
            pass

    print('consuming 30 values took %f seconds, clock: %f, cpu usage: %f' % (time.time() - t, time.clock() - c, get_cpu_usage()))
    t = time.time()
    c = time.clock()

    for p in producers:
        p.stopped = True

    for p in producers:
        p.join()

    print('shutdown took %f seconds, clock: %f, cpu usage: %f' % (time.time() - t, time.clock() - c, get_cpu_usage()))

class ProducerRemoteGevent(gevent.Greenlet):
    def __init__(self, queue):
        super(ProducerRemoteGevent, self).__init__()
        self.queue = queue

    def _run(self):
        while True:
            self.queue.put(1)
            gevent.sleep(random.random() * 4)

def consumer_local_gevent(block):
    queue = gevent.queue.Queue()
    producers = [ProducerRemoteGevent(queue) for _ in xrange(4)]

    if block:
        queue_getter = queue.get
    else:
        queue_getter = queue.get_nowait

    print('initial cpu usage: %f' % get_cpu_usage())
    t = time.time()
    c = time.clock()

    for p in producers:
        p.start()

    gevent.sleep(0)

    print('startup took %f seconds, clock: %f, cpu usage: %f' % (time.time() - t, time.clock() - c, get_cpu_usage()))
    t = time.time()
    c = time.clock()

    cnt = 0
    while cnt < 30:
        gevent.sleep(0)
        try:
            cnt += queue_getter()
        except gevent.queue.Empty:
            pass

    print('consuming 30 values took %f seconds, clock: %f, cpu usage: %f' % (time.time() - t, time.clock() - c, get_cpu_usage()))
    t = time.time()
    c = time.clock()

    gevent.killall(producers)

    # for p in producers:
    #     p.stopped = True

    # gevent.joinall(producers)

    print('shutdown took %f seconds, clock: %f, cpu usage: %f' % (time.time() - t, time.clock() - c, get_cpu_usage()))
    
def get_own_pid():
    for proc in psutil.process_iter():
        cmd = proc.cmdline()
        if cmd and 'python' in cmd[0]:
            for field in cmd[1:]:
                if field == __file__:
                    return proc.pid

def get_cpu_usage():
    return proc.cpu_percent()

if __name__ == '__main__':
    pid = get_own_pid()
    print('pid: %d' % pid)
    proc = psutil.Process(pid)

    print('== Polling multiple queues ==')
    consumer_remote()
    print('== Polling one queue ==')
    consumer_local(block=False)
    print('== Blocking on one queue ==')
    consumer_local(block=True)
    print('== Polling one queue with Gevent ==')
    consumer_local_gevent(block=False)
    print('== Blocking on one queue with Gevent ==')
    consumer_local_gevent(block=True)
