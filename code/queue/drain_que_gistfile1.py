#!/usr/bin/env python

import beanstalkc

conn = beanstalkc.Connection(host="mq-aws-us-east-1.iron.io", port=11300)
conn.put("oauth xxxxx-token xxx-project-id")

conn.use("urlpush.dest1.10")
while True:
    job = conn.reserve(1)
    if job:
        print "got job: %s" % job.body
        job.delete()
        print "job deleted"
    else:
        break

print "queue empty"
