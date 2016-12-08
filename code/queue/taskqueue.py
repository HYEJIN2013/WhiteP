import threading
import Queue
import atexit

def _worker():
    while True:
        func, args, kwargs = _queue.get()
        try:
            func(*args, **kwargs)
        except:
            pass # bork or ignore here; ignore for now
        finally:
            _queue.task_done() # so we can join at exit

def postpone(func):
    def decorator(*args, **kwargs):
        _queue.put((func, args, kwargs))
    return decorator

_queue = Queue.Queue()
_thread = threading.Thread(target = _worker) # one is enough; it's postponed after all
_thread.daemon = True # so we can exit
_thread.start()

def _cleanup():
    _queue.join() # so we don't exit too soon

atexit.register(_cleanup)
