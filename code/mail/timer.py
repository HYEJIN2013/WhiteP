import time
import sys
import datetime

class Timer(object):
  def __init__(self, label, sleep=None):
    self.label = label
    self.sleep = sleep
  
  def __enter__(self):
    self.starttime = time.time()
  
  def __exit__(self, exc_type, exc_value, traceback):
    duration = time.time() - self.starttime
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    sys.stdout.write("{%s} %s [%.8f]\n" % (timestamp, self.label, duration))
    if self.sleep:
      time.sleep(self.sleep)
