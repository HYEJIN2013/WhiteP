import time
import threading

import sloq


THREADS = 5
RATE = 1
WORK_UNITS = 100
WORK_DELAY = 0.1


def do_stuff(name, q):
    running = True
    while running:
        w = q.get()
        if w is None:
            running = False
            q.task_done()
        else:
            try:
                now = time.time()
                print("%s %s doing work %s" % (now, name, w))
                time.sleep(WORK_DELAY)
                now = time.time()
                print("%s %s finished work %s" % (now, name, w))
            finally:
                q.task_done()


def main():
    q = sloq.SlowQueue(release_tick=RATE)
    for i in range(0, WORK_UNITS):
        q.put(i + 1)
    for i in range(0, THREADS):
        q.put(None)
    for i in range(0, THREADS):
        name = "thread_%s" % (i + 1)
        t = threading.Thread(target=do_stuff, args=(name, q), name=name)
        t.daemon = True
        t.start()
    q.join()


if __name__ == "__main__":
    main()
