# install_twisted_rector must be called before importing and using the reactor
from setback.events.game_update_event import GameUpdateEvent
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from kivy.app import App
from kivy.uix.label import Label
from setback import Game, CreateLobbyEvent, UpdateJoinableLobbiesEvent, Player
from server.protocol_factory import SetbackServerFactory
import json 
from server.lobby import Lobby
class SetbackServerApp(App):
    lobbies = []

    def build(self):
        self.label = Label(text="server started\n")
        self.factory = SetbackServerFactory(self)
        reactor.listenTCP(8000, self.factory)
        return self.label

    def handle_request(self,client,request):
        try:
            method = getattr(self,request["method"])
            args = request.get("args",False)
            if args:
                args["client_id"] = client.id
                method(client,args)
             
        except AttributeError as e:
            print(f"{e.args[0]}".encode("utf-8"))
            client.transport.write(f"{e.args[0]}".encode("utf-8"))

    def create_lobby(self,client,args):
        lobby = Lobby(args["name"])
        self.lobbies.append(lobby)
        lobby.join(client,Player.from_json(args["player"]).name)
        self.update_joinable_lobbies()

    def get_games(self,client):
        event = self.get_joinable_games()
        client.throw_event(event)

    def join_game(self,client,args):
        game_id = args["game_id"]

        for lobby in self.lobbies:
            if lobby.game.id == game_id and not lobby.is_full():
                player = Player.from_json(args["player"])
                lobby.join(client,player.name)
            else:
                self.get_games(client)
    
    def get_joinable_games(self):
        not_full_games = []
        for lobby in self.lobbies:
            if len(lobby.clients) == 0:
                self.lobbies.remove(lobby)
            elif not lobby.game.is_full():
                not_full_games.append(lobby.game)

        return UpdateJoinableLobbiesEvent(not_full_games)
    
    def update_joinable_lobbies(self):
        result = self.get_joinable_games()
        
        for client in self.factory.clients:
            if client.lobby is None:
                client.throw_event(result)

if __name__ == '__main__':
    SetbackServerApp().run()