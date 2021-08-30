from setback import Game, Player, CreateGameEvent, GameUpdateEvent

class Lobby():
    def __init__(self,name) -> None:
        self.game = Game(name=name)
        self.clients = []
    
    def handle_event(self,client,request):
        try:
            method = getattr(self,request["method"])
            args = request.get("args",False)
            if args:
                method(client,args)
             
        except AttributeError as e:
            print(f"{e.args[0]}".encode("utf-8"))
            client.transport.write(f"{e.args[0]}".encode("utf-8"))

    def handle_disconnect(self,client):
        self.clients.remove(client)
        self.game.remove_player(client.id)

    def start_game(self):
        if(self.game.started == True):
            return "success"

        if(self.game.is_full()):
            self.game.started = True
            event = { "event": "game_started_event"}
            self.update(event)
            return "success"
        else:
            return "not enough players"

    def join(self,client,name):
        self.clients.append(client)
        client.lobby = self
        player = Player(name,"team_one",client.id)
        self.game.add_player(player)
        self.update(GameUpdateEvent(self.game))
    
    def leave_game(self,client,args):
        self.game.remove_player(client.id)
        self.clients.remove(client)
        client.lobby = None
        update_game_event = GameUpdateEvent(self.game)
        self.update(update_game_event)

    def update(self,event):
        for client in self.clients:
            client.throw_event(event)