from setback.events.place_bid_event import PlaceBidEvent
from setback.events.bid_update_event import BidUpdateEvent
from setback.game.bid_manager import BidManager
from setback import Game, Player, GameStartedEvent, GameUpdateEvent, Game

class Lobby():
    def __init__(self,name) -> None:
        self.game = Game(name=name)
        self.bid_manager = None
        self.clients = []

    def is_full(self):
        if len(self.clients) == 4: 
            return True
        else:
            return False
    
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

    def start_game(self,client,args):
        if(self.game.started == True):
            return "success"

        if(self.game.is_full()):
            self.game.started = True
            self.bid_manager = BidManager(self.game)
            event = GameStartedEvent()
            event.current_bidder = self.bid_manager.get_current_bidder()
            self.update(event)
            return "success"
        else:
            return "not enough players"

    def join(self,client,name):
        self.clients.append(client)
        client.lobby = self
        player = Player(name,"team_one",client.id)
        player.team = self.game.add_player(player)
        self.update(GameUpdateEvent(self.game))
    
    def leave_game(self,client,args):
        self.game.remove_player(client.id)
        self.clients.remove(client)
        client.lobby = None
        update_game_event = GameUpdateEvent(self.game)
        self.update(update_game_event)
    
    def send_bid_update(self):
        event = BidUpdateEvent()
        event.current_bidder_id = self.bid_manager.get_current_bidder()
        event.bids = self.bid_manager.get_bids()
        self.update(event)

    def place_bid(self,client,args):
        event = PlaceBidEvent.from_json(args)
        self.bid_manager.place_bid(event.id,event.bid)
        self.send_bid_update()

    def update(self,event):
        for client in self.clients:
            event.player_id = client.id
            client.throw_event(event)