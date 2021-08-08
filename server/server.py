# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol
from setback import Game, CreateGameResult, GetGamesResult, Player
import json

class SetbackServer(protocol.Protocol):
    def dataReceived(self, data):
        data = data.decode('utf-8')
        request = json.loads(data)

        try:
            method = getattr(self.factory.app,request["method"])
            args = request.get("args",False)
            if args:
                response = method(args)
            else:
                response = method()

            # dump the json to string and encode utf-8 
            response = json.dumps(response, default=lambda o: o.__dict__, sort_keys=True, indent=4).encode("utf-8")
            self.transport.write(response)
        except AttributeError as e:
            self.transport.write(f"{e.args[0]}".encode("utf-8"))
        


class SetbackServerFactory(protocol.Factory):
    protocol = SetbackServer

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label


class SetbackServerApp(App):
    label = None
    games = []

    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenTCP(8000, SetbackServerFactory(self))
        return self.label

    def create_game(self,args):
        game = Game()
        game.name = args["name"]
        game.team_one.append(Player.from_json(args["player"]))

        self.games.append(game)

        result = CreateGameResult(game.name,game.id)
        return result
    
    def get_games(self):
        result = GetGamesResult(self.games)
        return result
    
    def leave_game(self,args):
        game_id = args["game_id"]
        player_id = args["player_id"]
        
        game = [game for game in self.games if game.id == game_id][0]
        
        for player in game.team_one:
            if(player.id == args["player_id"]):
                game.team_one.remove(player)
                return f"removed {player_id} from {game_id}"
        for player in game.team_two:
            if(player.id == args["player_id"]):
                game.team_two.remove(player)
                return f"removed {player_id} from {game_id}"
    
    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.games.append(msg)

        response = json.dumps(self.games)
        return response.encode('utf-8')


if __name__ == '__main__':
    SetbackServerApp().run()