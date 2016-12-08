__author__ = 'szymon'
from multiprocessing import Process
from threading import Thread
from time import sleep
import zmq

class Worker(Thread):
    def __str__(self):
        return "%s-%d"%(self.name, self.id)
    def __init__(self, name, id):
        Thread.__init__(self)
        self.name = name
        self.id = id
    def run(self):
        pass

class ZMQWorker(Worker):
    def __init__(self, zmq_context, zmq_pull_addr, name="zmq_worker", id=1):
        Worker.__init__(self, name, id)
        self.context = zmq_context
        self.pull_socket = zmq_context.socket(zmq.PULL)
        self.pull_socket.connect(zmq_pull_addr)
    def run(self):
        while True:
            print "%s: %s"%(str(self), self.pull_socket.recv_multipart())
            sleep(5)



class ZMQClient(Worker):
    def __init__(self, zmq_context, zmq_sub_addr, zmq_push_addr, name="zmq_client", id=1):
        Worker.__init__(self, name, id)
        self.context = zmq_context
        self.sub_socket = zmq_context.socket(zmq.SUB)
        self.sub_socket.connect(zmq_sub_addr)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, "")

        self.push_socket = zmq_context.socket(zmq.PUSH)
        self.push_socket.bind(zmq_push_addr)

    def run(self):
        while True:
            msg = self.sub_socket.recv_multipart()
            self.push_socket.send_multipart(msg)

class ZMQServer(Worker):
    def __init__(self, zmq_context, zmq_pub_addr, name="zmq_server", id=1):
        Worker.__init__(self, name, id)
        self.context = zmq_context
        self.pub_socket = zmq_context.socket(zmq.PUB)
        self.pub_socket.bind(zmq_pub_addr)
    def publish(self, msg_list):
        self.pub_socket.send_multipart(msg_list)




context = zmq.Context()
server = ZMQServer(context,"tcp://*:5555")
client = ZMQClient(context,"tcp://localhost:5555", "inproc://test")
client.start()
for num in range(0,5):
    worker = ZMQWorker(context,"inproc://test", id=num)
    worker.start()
for msg in range(0,20):
    server.publish(["message","%d"%msg])
