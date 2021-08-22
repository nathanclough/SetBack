# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from kivy.app import App
from kivy.uix.label import Label
from setback import Game, CreateGameResult, GetGamesResult, Player
from server.protocol_factory import SetbackServerFactory
import json 

class SetbackServerApp(App):
    label = None
    games = {}
    # key is game id, value is list of client id's 
    lobbies = {}

    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenTCP(8000, SetbackServerFactory(self))
        return self.label

    def create_game(self,args):
        game = Game()
        game.name = args["name"]
        game.team_one.append(Player.from_json(args["player"]))

        self.games[game.id] = game
        self.lobbies[game.id] = [ args["client_id"] ]

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
        game.remove_player(player_id)

        if( any(x == args["client_id"] for x in self.lobbies[game.id])):
            self.lobbies[game.id].remove(args["client_id"])

        if(not game.has_players()):
            self.games.pop(game.id)
            self.lobbies.pop(game.id)
        return "success"

    def join_game(self,args):
        game = self.games[args["game_id"]]

        game.add_player(Player.from_json(args["player"]))
        self.lobbies[game.id].append(args["client_id"])         
        return game

    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.games.append(msg)

        response = json.dumps(self.games)
        return response.encode('utf-8')

if __name__ == '__main__':
    SetbackServerApp().run()