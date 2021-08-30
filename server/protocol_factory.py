import json
from server.protocol import SetbackServer
from twisted.internet import protocol

class SetbackServerFactory(protocol.Factory):
    protocol = SetbackServer
        
    def __init__(self, app):
        self.app = app
        self.clients = []

    def register(self,client):
        self.clients.append(client)
        print(f"registered {client}: id {client.id}")

    def unregister(self,client):
        self.clients.remove(client)
        

    
