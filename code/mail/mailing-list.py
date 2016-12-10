from smtproutes import Route, Server
from pymongo import Connection

subscribers = Connection('vmimage').mailing_list.subscribers

class MailingList(Route):
    
    def subscribe(self, route=r'subscribe-(?P<name>[^@]*)@.*'):
        subscribers.update({
            'email': self.mailfrom.email,
        },
        {'$set': {
            'email': self.mailfrom.email,
            'name': self.name
        }}, upsert=True)
        
    def unsubscribe(self, route=r'unsubscribe@.*'):
        subscribers.remove({
            'email': self.mailfrom.email
        })
        
Server(('0.0.0.0', 25), None).add_route(MailingList).start()
