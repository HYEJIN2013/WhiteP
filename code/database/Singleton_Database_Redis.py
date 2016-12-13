class Redis(object):
  _Dict = dict()

  def __new__(self):
    if 'Instance' in Redis._Dict:
      return Redis._Dict['Instance']
    else:
      self.Conf = DBConf()['Redis']
      self.Engine = redis.Redis(connection_pool=redis.ConnectionPool(host=self.Conf['Host'],port=self.Conf['Port'],max_connections=10))
      return super(Redis,self).__new__(self)

  def __init__(self):
    Redis._Dict['Instance'] = self
