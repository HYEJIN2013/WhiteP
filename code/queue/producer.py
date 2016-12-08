from time import sleep


def data_thread(queue):
    counter = 1

    while True:
        sleep(1)
        queue.put(counter)
        counter += 1
