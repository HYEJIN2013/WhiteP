from dirq.QueueSimple import QueueSimple
from random import randint
import time

path = '/tmp/test'

print("start consuming...")
dirq = QueueSimple(path)
done = 0
while True:
    for name in dirq:
        # print("element: %s %s" % (path, name))
        if not dirq.lock(name):
            #print("couldn't lock: %s" % name)
            # name = dirq.next()
            continue
        element = dirq.get(name)
        #print(element.keys())
        print("Body: \"%s\"" % element)
        if randint(1,2) % 2:
            done += 1
            dirq.remove(name)
            #print('Removed')
        else:
            dirq.unlock(name)
        #name = dirq.next()
    print("consumed %i elements" % done)
    total_left = dirq.count()
    print("elements left in the queue: %d" % total_left)
    time.sleep(0.5)
