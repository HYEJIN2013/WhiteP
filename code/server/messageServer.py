import socket
import sys

PORT = 8000
IP = '197.168.1.67'

serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((IP, PORT))
serversocket.listen(5)


def runServer():
    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(128) # 128 bytes per message
        if len(buf) > 0:
            print ', '.join([buf[0:19], address[0], buf[19:]])

if __name__ == '__main__':
    try:
        print 'Now running server on %s, port %i' % (IP, PORT)
        runServer()
    except KeyboardInterrupt:
        print '\nExiting program'
    sys.exit()
