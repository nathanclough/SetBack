from attr import Factory
from twisted.internet.protocol import ServerFactory
from twisted.test import proto_helpers
from server.server import SetbackServerApp, SetbackServerFactory
from setback import CreateGameResult, GetGamesResult, Game, Player
import json
import pytest


class FakeServer():
    def  __init__(self) -> None: 
        self.app = SetbackServerApp()
        self.factory = SetbackServerFactory(self.app)
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

class TestServer:
    def test_create_game(self,server:FakeServer):
        # Arrange 
        # Create the request as dict 
        request = {
            "request_id": 1,
            "method": "create_game",
            "args": {
                "name" : "Game1",
                "player": {
                    "name" : "Nathan",
                    "id" : 123,
                    "team": 1
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
        create_game_result = CreateGameResult.from_json(json.loads(result)["response"])
        
        # Verify that the result is correct
        assert create_game_result.id != None and create_game_result.name == "Game1"

    def test_get_games(self,server:FakeServer):   
        request = {
            "request_id": 1,
            "method": "get_games"
        }
        request = json.dumps(request)

        server.send_request(request)
        result = server.get_result()
        get_games_result = GetGamesResult.from_json(json.loads(result)["response"])
        assert len(get_games_result.games) == 1 

    def test_leave_game_team_one(self,server:FakeServer):
        player = Player("Nathan",1,123)
        team = [player]
        game = Game(team_one=team)
        server.app.games = { game.id: game}

        request = { "request_id": 1,
            "method": "leave_game",
            "args" : { "game_id": game.id, "player_id" : player.id}}

        server.send_request(json.dumps(request))

        result = server.get_result()
        
        assert len(server.app.games[game.id].team_one) == 0

    def test_leave_game_team_two(self,server:FakeServer):
        player = Player("Nathan",2,123)
        team = [player]
        game = Game(team_one=team)
        server.app.games = { game.id: game}

        request ={ "request_id": 1,
            "method": "leave_game",
            "args" : { "game_id": game.id, "player_id" : player.id}}

        server.send_request(json.dumps(request))

        result = server.get_result()
        
        assert len(server.app.games[game.id].team_one) == 0 
    
    def test_join_game(self,server):
        game = Game()
        server.app.games = {game.id: game}
        server.app.lobies[game.id] = []

        player = Player("Nathan",2,123)
        request = { "request_id": 1, 
            "method" : "join_game",
            "args" : { 
                "player" : player, 
                "game_id" : game.id,
                "team": 1
                }
            }
        
        server.send_request(json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4))

        assert len(server.app.games[game.id].team_one) == 2
    
    def test_get_game_with_full_teams_not_in_result(self,server:FakeServer):
        game = Game()
        team_one = [Player("p1",1),Player("p2",1)]
        team_two = [Player("p3",2),Player("p4",2)]
        game.team_two = team_two
        game.team_one = team_one

        server.app.games = {game.id: game}
        request = {
            "request_id": 1,
            "method": "get_games"
        }
        request = json.dumps(request)

        server.send_request(request)
        result = server.get_result()
        get_games_result = GetGamesResult.from_json(json.loads(result)["response"])
        assert len(get_games_result.games) == 0

    def test_join_game_team_is_full_joins_other_team(self, server:FakeServer):
        game = Game()
        team_two = [Player("p3",2),Player("p4",2)]
        game.team_two = team_two
        game.team_one = []

        server.app.games = {game.id: game}
        server.app.lobies[game.id] = []

        player = Player("Nathan",2,123)
        request = { "request_id": 1, 
            "method" : "join_game",
            "args" : { 
                "player" : player, 
                "game_id" : game.id,
                "team": 2
                }
            }
        
        server.send_request(json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4))

        assert len(server.app.games[game.id].team_one) == 1


    def test_unknown_method(self,server:FakeServer):
        request = {
            "request_id": 1,
            "method": "foo",
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

        assert result == "'SetbackServerApp' object has no attribute 'foo'"
