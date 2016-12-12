from twisted.internet import reactor  
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols import amp

class ChangeCurrency(amp.Command):
    arguments = [('newPrice', amp.Integer())]

class MarketProtocol(amp.AMP):
    def __init__(self, price):
        self.price = price
        
    def connectionMade(self):
        self.callRemote(ChangePrice, newPrice=price) 
        print 'connection made'

    def changeCurrency(self):
        self.factory.currency = price 

class Factory(ClientFactory):
    def __init__(self, price):
        self.price = price
        self.currency = 0

    def buildProtocol(self, addr):
        return MarketProtocol(self.price)

def printCurrency():
    print factory.currency

def main(price):
    from twisted.internet import reactor
    print 'installed'
    factory = Factory(price)
    print 'initializing factory'
    reactor.connectTCP("86.85.138.215", 45000, factory) 
    print 'connecting'
    reactor.run()
    print 'reactor done running'

if __name__=="__main__":main(10)
