# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol
from setback import Game, CreateGameResult, GetGamesResult, Player
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
            self.transport.write(f"{e.args[0]}".encode("utf-8"))
    
    def connectionMade(self):
        self.factory.register(self)
        print(f"connected {self}")
    
    def connectionLost(self, reason):
        self.factory.unregister(self)
        print(f"disconnected {self}")

class SetbackServerFactory(protocol.Factory):
    protocol = SetbackServer
    clients = {}
    
    def __init__(self, app):
        self.app = app

    def register(self,client):
        self.clients[client.id] = client
        print(f"registered {client}: id {client.id}")

    def unregister(self,client):
        self.clients.remove(client)

    def sendCommand(self, client_list,cmd):
        for id in client_list:
            client = self.clients[id]
            cmd = json.dumps(cmd, default=lambda o: o.__dict__, sort_keys=True, indent=4).encode("utf-8")
            client.transport.write(cmd)
    
from kivy.app import App
from kivy.uix.label import Label


class SetbackServerApp(App):
    label = None
    games = {}
    # key is game id, value is list of client id's 
    lobies = {}

    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenTCP(8000, SetbackServerFactory(self))
        return self.label

    def create_game(self,args):
        game = Game()
        game.name = args["name"]
        game.team_one.append(Player.from_json(args["player"]))

        self.games[game.id] = game
        self.lobies[game.id] = [ args["client_id"] ]

        result = CreateGameResult(game.name,game.id)
        return result
    
    def get_games(self):
        not_full_games = {k:v for (k,v) in self.games.items() if not v.is_full()}
        result = GetGamesResult(not_full_games)
        return result
    
    def leave_game(self,args):
        game_id = args["game_id"]
        player_id = args["player_id"]
        
        game = self.games[game_id]
        
        for player in game.team_one:
            if(player.id == player_id):
                game.team_one.remove(player)
                return f"removed {player.name} from Game: {game.id}"
        
        for player in game.team_two:
            if(player.id == player_id):
                game.team_two.remove(player)
                return f"removed {player.name} from Game: {game.id}" 

        self.lobies[game.id].remove(args["client_id"])

    def join_game(self,args):
        game = self.games[args["game_id"]]

        if (len(game.team_one) < 2):
            game.team_one.append(Player.from_json(args["player"]))
        elif(len(game.team_two) < 2):
            game.team_two.append(Player.from_json(args["player"]))
        

        self.lobies[game.id].append(args["client_id"])         
        return game

    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.games.append(msg)

        response = json.dumps(self.games)
        return response.encode('utf-8')


if __name__ == '__main__':
    SetbackServerApp().run()