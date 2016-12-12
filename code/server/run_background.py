import subprocess
import sys
import time

try:
    p = subprocess.Popen([sys.executable, '-m', 'Pyro4.naming'],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)
    time.sleep(5)
except Exception, e:
    raise e
finally:
    p.terminate()
