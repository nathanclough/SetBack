from twisted.internet import protocol
import json
import uuid

class SetbackServer(protocol.Protocol):
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        super().__init__()

    def dataReceived(self, data):
        data = data.decode('utf-8')
        request = json.loads(data)
        request_id = request["request_id"]
        try:
            method = getattr(self.factory.app,request["method"])
            args = request.get("args",False)
            if args:
                args["client_id"] = self.id
                response = method(args)
            else:
                response = method()
            response = { "request_id":request_id ,
                "response": response }

            # dump the json to string and encode utf-8 
            response = json.dumps(response, default=lambda o: o.__dict__, sort_keys=True, indent=4).encode("utf-8")
            self.transport.write(response)
        except AttributeError as e:
            print(f"{e.args[0]}".encode("utf-8"))
            self.transport.write(f"{e.args[0]}".encode("utf-8"))
    
    def connectionMade(self):
        self.factory.register(self)
        print(f"connected {self}")
    
    def connectionLost(self, reason):
        self.factory.unregister(self)
        print(f"disconnected {self}")