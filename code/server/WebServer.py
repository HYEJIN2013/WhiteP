import socket

server = socket.socket()
server.bind(('localhost', 1001))
server.listen(1)


while True:
    conn, addr = server.accept()
    print "User connected!"
    conn.send("<h1>Lol</h1>")
    conn.close()
