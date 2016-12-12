import optparse
from keyczar.keys import RsaPrivateKey
from twisted.internet import reactor, protocol
from twisted.protocols import basic

class CryptoProtocol(basic.LineReceiver):

	def connectionMade(self):
		self.factory.clients.append(self)
		self.file_handler = None
		self.file_data = ()
		self.key=RsaPrivateKey.Generate()
		self.pubkey=self.key.public_key
		self.transport.write(str(self.pubkey))
		print 'Connection from: %s (%d clients total)' % (self.transport.getPeer().host, len(self.factory.clients))
		
	def connectionLost(self, reason):
		self.factory.clients.remove(self)
		print 'Connection from %s lost (%d clients left)' % (self.transport.getPeer().host, len(self.factory.clients))
			
	def dataReceived(self, data):
		print self.key.Decrypt(data)

class CryptoServerFactory(protocol.ServerFactory):
	
	protocol = CryptoProtocol
	
	def __init__(self):
		
		self.clients = []
	
if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-p', '--port', action = 'store', type = 'int', dest = 'port', default = 1234, help = 'listening port')
	(options, args) = parser.parse_args()
	
	print 'Listening on port %d' % (options.port)

	reactor.listenTCP(options.port, CryptoServerFactory())
	reactor.run()
