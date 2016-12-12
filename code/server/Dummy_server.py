from tornado import web, websocket, ioloop

class Test(websocket.WebSocketHandler):
    clients = set()

    def open(self):
        self.clients.add(self)

    def on_message(self, msg):
        for c in self.clients:
            c.write_message(msg)

    def on_close(self):
        self.clients.remove(self)

if __name__ == '__main__':
    app = web.Application([(r'/', Test)])
    app.listen(8080)

    ioloop.IOLoop.instance().start()
