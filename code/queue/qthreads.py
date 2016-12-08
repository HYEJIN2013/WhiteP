#! /usr/bin/env python

from pika.adapters import BlockingConnection
import threading
import time

class QueueThread(threading.Thread):
  def __init__(self):
    super(QueueThread, self).__init__()
    self.name = self.__class__.__name__
    self.connection = BlockingConnection()
    self._stop = threading.Event()
    self.setDaemon(True)

  def dprint(self, msg):
    print "%s: %s" % (self.name, msg)

class QueueConsumerThread(QueueThread):
  def __init__(self):
    super(QueueConsumerThread, self).__init__()

  def run(self):
    self.setup()
    self.channel.start_consuming()

  def stop(self):
    self.channel.stop_consuming()
    self._stop.set()

class QueueProducerThread(QueueThread):
  def __init__(self, freq=5):
    super(QueueProducerThread, self).__init__()
    self.freq = freq

  def run(self):
    self.setup()
    while True:
      self.produce()
      time.sleep(self.freq)

  def stop(self):
      self.connection.close()
      self._stop.set()
