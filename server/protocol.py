from twisted.internet import protocol
import json
import uuid

class SetbackServer(protocol.Protocol):
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.lobby = None
        super().__init__()

    def dataReceived(self, data):
        data = data.decode('utf-8')
        request = json.loads(data)
        if self.lobby is None: 
            self.factory.app.handle_request(self,request)
        else: 
            self.lobby.handle_event(self,request)
   
    def throw_event(self, event):
        event_as_json = json.dumps(event, default=lambda o: o.__dict__, sort_keys=True, indent=4).encode("utf-8")
        self.transport.write(event_as_json)

    def connectionMade(self):
        self.factory.register(self)
        print(f"connected {self}")

        # give a list of the current games
        event = self.factory.app.get_joinable_lobbies()
        self.throw_event(event)

    
    def connectionLost(self, reason):
        self.factory.unregister(self)
        if not self.lobby is None:
            self.lobby.handle_disconnect(self)
        print(f"disconnected {self}")