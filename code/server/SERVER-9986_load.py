from pymongo import MongoClient
import random

mc = MongoClient()

batch = []

for i in xrange(10000000):
	doc = {"location": [random.random(), random.random()], "name": {"firstName": random.choice(["tom","david","james","stephen","ian","tia","andre"])},"taxonomy":{"code": str(random.randint(0, 10000))}}
	if i % 10000 == 9999:
		mc.test.docs.insert(batch, w=0)
		batch = []
		print i
	else:
		batch.append(doc)
