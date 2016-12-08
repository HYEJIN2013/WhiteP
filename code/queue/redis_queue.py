class RQueue(object):
    """ redis queue wrap """
    KEY = "redis"
    def __init__(self, redis_conn):
        """
        :host: redis host
        :port: redis port
        :redis_conn: redis connection
        """
        self.redis = redis_conn
        #redis.Redis(host=host, port=port, db=db)

    def get(self, timeout=5):
        """Get element from q."""
        value = self.redis.blpop(self.KEY, timeout=timeout)
        return value and value[1] or value

    def put(self, value):
        """Put element into q."""
        self.redis.rpush(self.KEY, value)

    def empty(self):
        """Return True if q is empty."""
        return False if self.redis.llen(self.KEY) else True
        
    def count(self):
        """Return the number of emelments in the q."""
        return self.redis.llen(self.KEY)

    def __str__(self):
        return "Redis Queue: len {}".format(self.redis.llen(self.KEY))

    def __repr__(self):
        return "{0}('{host}', '{port}', '{db}')".format(
                              self.__class__.__name__,
                              **self.redis.connection_pool.connection_kwargs)
