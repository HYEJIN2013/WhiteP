from queue import Queue
from threading import Thread
from time import sleep

from producer import data_thread


def vpython_main(queue: Queue):
    while True:
        sleep(0.2)
        if not queue.empty():
            data = queue.get_nowait()
        else:
            print('empty')
            continue

        print(data)


if __name__ == '__main__':
    q = Queue()

    data_t = Thread(target=data_thread, args=(q,))
    data_t.start()

    vpython_main(q)
