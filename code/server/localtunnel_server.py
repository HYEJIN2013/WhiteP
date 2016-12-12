
try:
    from twisted.internet import pollreactor
    pollreactor.install()
except: pass
from twisted.internet import protocol, reactor, defer, task
from twisted.web import http, proxy, resource, server
from twisted.python import log
import sys
import time
import itertools
import urlparse
import random
import socket
import simplejson
import re

SSH_USER = 'localtunnel'
AUTHORIZED_KEYS = '/home/localtunnel/.ssh/authorized_keys'
PORT_RANGE = [32000, 64000]
BANNER = "This localtunnel service is brought to you by XLAB."
SSH_OPTIONS = 'command="/bin/echo Shell access denied",no-agent-forwarding,no-pty,no-user-rc,no-X11-forwarding '
KEY_REGEX = re.compile(r'^ssh-(\w{3}) [^\n]+$')

def port_available(port):
    try:
        socket.create_connection(['127.0.0.1', port]).close()
        return False
    except socket.error:
        return True
    
class LocalTunnelReverseProxy(proxy.ReverseProxyResource):
    isLeaf = True
    
    def __init__(self, user, host='127.0.0.1'):
        self.user = user
        self.tunnels = {}
        proxy.ReverseProxyResource.__init__(self, host, None, None)
    
    def find_tunnel_name(self):
        chars = '23456789abcdefghijkmnpqrstuvwxyz'
        
        def get_name():
            return ''.join([random.choice(chars) for i in range(4)])
        
        name = get_name()
        
        while ((name in self.tunnels
                and not port_available(self.tunnels[name]['port']))
                or name == 'open'):
            name = get_name()
        
        return name
        
    def find_tunnel_port(self):
        port_range = range(*PORT_RANGE)
        random.shuffle(port_range)
        
        for port in self.tunnels:
            if port in port_range:
                port_range.remove(port)
                port_range.append(port)
        
        for port in itertools.cycle(port_range):
            if port_available(port):
                return port
            
            if time.time() - start_time > 3:
                raise Exception('No port available')
    
    def garbage_collect(self):
        for name, data in self.tunnels.items()[:]:
            if time.time() - data['created'] > 10:
                if port_available(data['port']):
                    del self.tunnels[name]
    
    def install_key(self, key):
        if not KEY_REGEX.match(key.strip()):
            return False
        key = ''.join([SSH_OPTIONS, key.strip(), "\n"])
        fr = open(AUTHORIZED_KEYS, 'r')
        if not key in fr.readlines():
            fa = open(AUTHORIZED_KEYS, 'a')
            fa.write(key)
            fa.close()
        fr.close()
        return True
    
    def register_tunnel(self, superhost, key=None):
        if key and not self.install_key(key): return simplejson.dumps(dict(error="Invalid key."))
        name = self.find_tunnel_name()
        port = self.find_tunnel_port()
        self.tunnels[name] = {'port': port, 'created': time.time()}
        return simplejson.dumps(
            dict(through_port=port, user=self.user, host='%s.%s' % (name, superhost), banner=BANNER))
    
    def render(self, request):
        host = request.getHeader('host')
        name, superhost = host.split('.', 1)
        if host.startswith('open.'):
            request.setHeader('Content-Type', 'application/json')
            return self.register_tunnel(superhost, request.args.get('key', [None])[0])
        else:
            if not name in self.tunnels: return "Not found"
        
            request.content.seek(0, 0)
            clientFactory = self.proxyClientFactoryClass(
                request.method, request.uri, request.clientproto,
                request.getAllHeaders(), request.content.read(), request)
            self.reactor.connectTCP(self.host, self.tunnels[name]['port'], clientFactory)
            return server.NOT_DONE_YET

def test_local_tunnel():
    import tempfile
    
    global AUTHORIZED_KEYS
    
    assert port_available('55020') == True
    
    x = LocalTunnelReverseProxy(SSH_USER)
    
    assert x.find_tunnel_name()
    
    assert x.find_tunnel_port()
    
    x.garbage_collect()
    
    AUTHORIZED_KEYS = tempfile.mktemp()
    
    open(AUTHORIZED_KEYS, 'w').close()
    
    assert x.install_key('ssh-rsa a1s2d3ff4g5h7j')
    
    assert not x.install_key('ssh-t a1s2d3ff4g5h7j')
    
    assert x.register_tunnel('myhost.local')
    assert x.register_tunnel('myhost.local', 'ssh-rsa a1s2d3ff4g5h7j')

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    reactor.listenTCP(80, server.Site(LocalTunnelReverseProxy(SSH_USER)))
    reactor.run()
