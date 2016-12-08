import eventlet
from eventlet.hubs import get_hub
from eventlet.queue import _NONE, Empty, Queue, Waiter


class PeekableQueue(Queue):
    def get(self, *args, **kwargs):
        return self.__get_item_when_available(self._get, *args, **kwargs)

    def peek(self, *args, **kwargs):
        return self.__get_item_when_available(self._peek, *args, **kwargs)

    def _peek(self):
        return self.queue[0]

    def __get_item_when_available(self, method, block=True, timeout=None):
        if self.qsize():
            if self.putters:
                self._schedule_unlock()
            return method()
        elif not block and get_hub().greenlet is eventlet.getcurrent():
            while self.putters:
                putter = self.putters.pop()
                if putter:
                    putter.switch(putter)
                    if self.qsize():
                        return method()
        elif block:
            waiter = Waiter()
            timeout = eventlet.Timeout(timeout, Empty)
            try:
                self.getters.add(waiter)
                if self.putters:
                    self._schedule_unlock()
                result = waiter.wait()
                assert result is waiter, 'Invalid switch into Queue.get: %r' % (result,)
                return method()
            finally:
                self.getters.discard(waiter)
                timeout.cancel()
        else:
            raise Empty

    def _unlock(self):
        try:
            while True:
                if self.qsize() and self.getters:
                    getter = self.getters.pop()
                    if getter:
                        getter.switch(getter)
                elif self.putters and self.getters:
                    putter = self.putters.pop()
                    if putter:
                        getter = self.getters.pop()
                        if getter:
                            item = putter.item
                            putter.item = _NONE
                            self._put(item)
                            getter.switch(getter)
                            putter.switch(putter)
                        else:
                            self.putters.add(putter)
                elif self.putters and (self.getters or self.maxsize is None or self.qsize() < self.maxsize):
                    self.putters.pop().switch(putter)
                else:
                    break
        finally:
            self._event_unlock = None
