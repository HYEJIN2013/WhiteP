# coding=utf-8

import select, socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'

def server(port):
    resp = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
    resp += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
    resp += b'Hello, world!'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
    server_socket.setblocking(0)

    epoll = select.epoll()
    epoll.register(server_socket.fileno(), select.EPOLLIN)

    try:
        conns = {}; reqs = {}; resps = {}
        while True:
            events = epoll.poll(1)
            for fileno, event in events:
                if fileno == server_socket.fileno():
                    conn, address = server_socket.accept()
                    conn.setblocking(0)
                    epoll.register(conn.fileno(), select.EPOLLIN)
                    conns[conn.fileno()] = conn
                    reqs[conn.fileno()] = b''
                    resps[conn.fileno()] = resp
                elif event & select.EPOLLIN:
                    reqs[fileno] += conns[fileno].recv(1024)
                    if EOL1 in reqs[fileno] or EOL2 in reqs[fileno]:
                        epoll.modify(fileno, select.EPOLLOUT)
                        print '-' * 40 + '\n' + reqs[fileno].decode()[:-2]
                elif event & select.EPOLLOUT:
                    bytes_written = conns[fileno].send(resps[fileno])
                    resps[fileno] = resps[fileno][bytes_written:]
                    if len(resps[fileno]) == 0:
                        epoll.modify(fileno, 0)
                        conns[fileno].shutdown(socket.SHUT_RDWR)
                elif event & select.EPOLLHUP:
                    epoll.unregister(fileno)
                    conns[fileno].close()
                    del conns[fileno]
    finally:
        epoll.unregister(server_socket.fileno())
        epoll.close()
        server_socket.close()

server(8098)
