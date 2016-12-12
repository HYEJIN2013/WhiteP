#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import tornado.ioloop
import tornado.web
import tornado.log
import tornado.gen
import tornado.template

is_closing = False

def signal_handler(signum, frame):
    global is_closing
    logging.info('exiting...')
    is_closing = True

def try_exit():
    global is_closing
    if is_closing:
        # clean up here
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('exit success')

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.template = 'data/p.html'

    @tornado.gen.coroutine
    def get(self):
        arg_sleep = float(self.get_argument(name='sleep', default=0))
        if arg_sleep > 0:
            yield tornado.gen.sleep(arg_sleep)
        self.render(self.template)

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(9999)
    tornado.log.enable_pretty_logging()
    tornado.ioloop.PeriodicCallback(try_exit, 100).start()
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
