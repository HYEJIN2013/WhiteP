from amqplib import client_0_8 as amqp

conn = amqp.Connection(host="mq.example.com:5672", userid="admin", password="p@ssw0rd!", virtual_host="/", insist=False)
conn = conn.channel()

queues = ['celery']

for q in queues:
    if q:
        #print 'deleting %s' % q
        conn.queue_purge(q.strip())

print 'purged %d items' % len(queues)
