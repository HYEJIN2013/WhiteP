#!/usr/bin/python

import Queue
import threading
import time

exitFlag = 0

portas = { 'ttyUSB1': 'idle', 'ttyUSB2': 'idle'}

fila = ['tarefa 1', 'tarefa 2', 'tarefa 3', 'tarefa 4', 'tarefa 5', 'tarefa 6', 'tarefa 7', 'tarefa 8', 'tarefa 9', 'tarefa 10']



class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    
    def run(self):
        print "Starting " + self.name
        process_data(self.name, self.q)
        print "Exiting " + self.name



def getIdlePort():
   
    while True: 
        for port in portas:
            if portas[port] == 'idle':
                portas[port] = 'busy'

                return port
        time.sleep(5)




def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            port = getIdlePort()
            queueLock.release()
            print "%s processing %s - %s" % (threadName, data, port)
            time.sleep(2)
            portas[port] = 'idle'
        else:
            queueLock.release()
        time.sleep(1)




threadList = ["Thread-1", "Thread-2", "Thread-3"]

queueLock = threading.Lock()
workQueue = Queue.Queue()
threads = []
threadID = 1

# Create new threads
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# Fill the queue
queueLock.acquire()
for word in fila:
    workQueue.put(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"
