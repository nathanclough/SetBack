import json
from server.protocol import SetbackServer
from twisted.internet import protocol

class SetbackServerFactory(protocol.Factory):
    protocol = SetbackServer
    clients = {}
    
    def __init__(self, app):
        self.app = app

    def register(self,client):
        self.clients[client.id] = client
        print(f"registered {client}: id {client.id}")

    def unregister(self,client):
        self.clients.pop(client.id)

    def sendCommand(self, client_list,cmd):
        for id in client_list:
            client = self.clients[id]
            cmd = json.dumps(cmd, default=lambda o: o.__dict__, sort_keys=True, indent=4).encode("utf-8")
            client.transport.write(cmd)
    
