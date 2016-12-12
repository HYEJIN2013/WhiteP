import socket

server = socket.socket()
server.bind(('localhost', 1001))
server.listen(1)

conn, addr = server.accept()
print "User connected!"

while True:
    data = conn.recv(1024)
    if not data: break
    conn.send("SAY "+data)

conn.close()
