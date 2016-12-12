from functools import wraps




def cached(f):
    cache = f._meta_cache = {}
    @wraps(f)
    def finder(a_):
        if a_ not in cache:
            cache[a_] = f(a_)
        return cache[a_]
    return finder


@cached
def x(a):
    return x(a - 1) + x(a - 2) + 42 if a > 1 else a


print '%r' % x(195)
