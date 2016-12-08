import traceback as tb, gevent
from concurrent.futures import Future

in_flight = [0]
in_flight_max = 100
Q = []

def spawn_query(fn,future,*a,**kw):
    def wrapper():
        try:
            in_flight[0] += 1
            ret = fn(*a,**kw)
            future.set_result(ret)
        except:
            print '*'*80
            print tb.format_exc()
            print '*'*80
        finally:
            if not Q:
                in_flight[0] -= 1
            else:
                ( fn,future,a,kw ) = Q.pop(0)
                spawn_query( fn,future,*a,**kw )
                pass
            pass
        pass
    if in_flight[0] < in_flight_max:
        gevent.spawn(wrapper)
    else:
        Q.append( ( fn,future,a,kw ) )
        pass
    return future

def spawn_future_query(fn,*a,**kw):
    return spawn_future_query(fn,Future(),*a,**kw)
