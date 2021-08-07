from attr import Factory
from twisted.internet.protocol import ServerFactory
from twisted.test import proto_helpers
from server.server import SetbackServerApp, SetbackServerFactory
from setback import CreateGameResult
import json
import pytest

class FakeServer():
    def  __init__(self) -> None:      
        self.factory = SetbackServerFactory(SetbackServerApp())
        self.proto = self.factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)
    
    # Takes in json and sends to server 
    def send_request(self,requestJson):
        self.proto.dataReceived(requestJson.encode("utf-8"))
    
    # Returns Json Response
    def get_result(self):
        return self.tr.value().decode('utf-8')

@pytest.fixture
def server():
    return FakeServer()

def test_create_game(server:FakeServer):
    # Arrange 
    # Create the request as dict 
    request = {
        "method": "create_game",
        "args": {
            "name" : "Game1",
            "player": {
                "id" : 123
            }
        }
    }
    # Convert to json 
    request = json.dumps(request)
    
    # Act 
    # Send the request 
    server.send_request(request)
    
    # Assert 
    # get the result
    result = server.get_result()
    
    # Convert it to result object from json 
    create_game_result = CreateGameResult.from_json(json.loads(result))
    
    # Verify that the result is correct
    assert create_game_result.id != None and create_game_result.name == "Game1"

def test_unknown_method(server:FakeServer):
    request = {
        "method": "foo",
        "args": {
            "name" : "Game1",
            "player": {
                "id" : 123
            }
        }
    }
    # 
    # Convert to json 
    request = json.dumps(request)
    
    # Act 
    # Send the request 
    server.send_request(request)
    
    # Assert 
    # get the result
    result = server.get_result()

    assert result == "AttributeError: 'SetbackServerApp' object has no attribute 'foo'"
