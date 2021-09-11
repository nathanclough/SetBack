from setback.events.update_joinable_games import UpdateJoinableGamesEvent
from setback.events.game_update_event import GameUpdateEvent
from kivy.uix.screenmanager import ScreenManager
from setback import Player
from kivy.properties import ObjectProperty, ListProperty
import json

class StateManager(ScreenManager):
    game_id = ""
    games_to_join = ListProperty()
    game = ObjectProperty()
    team_one = ListProperty()
    team_two = ListProperty()
    player = ObjectProperty(Player("",1))
    connection = None
    
    def __init__(self, **kwargs):
        self.player = Player("Player",1)
        self.register_event("game_update_event",self.handle_game_update_event)
        self.register_event("game_started_event",self.handle_game_started_event)
        self.register_event("update_joinable_games_event",self.handle_update_joinable_games_event)
        super().__init__(**kwargs)
    
    # key is event name and handler is list of subscribers
    event_handlers = {}
    
    def handle_event(self,event):
        handlers = self.event_handlers[event["event"]]
        for handler in handlers:
            handler(event)

    def set_connection(self, connection):
        self.connection = connection

    def register_event(self,event,handler):
        if(event in self.event_handlers):
           # there is already a subscriber
           # so we can just append the handler
           self.event_handlers[event].append(handler)
        else:
            # no current subscribers 
            # add new list of handlers
            self.register_event_type(f"on_{event}") 
            self.event_handlers[event] = [handler]
    
    def handle_game_update_event(self,event):
        event = GameUpdateEvent.from_json(event)
        self.game = event.game
        self.team_one = event.game.team_one
        self.team_two = event.game.team_two
        self.teams = {1:self.team_one, 2: self.team_two}
        self.player.id = event.player_id
        # Update the current player
        self.player = next((player for player in self.team_one + self.team_two if player.id == self.player.id),None)
        self.dispatch('on_game_update_event')

    def handle_update_joinable_games_event(self,event):
        event = UpdateJoinableGamesEvent.from_json(event)
        self.games_to_join = event.games
        self.dispatch('on_update_joinable_games_event')

    def handle_game_started_event(self, event):
        self.current = "table"
        self.dispatch('on_game_started_event')

    def get_games(self,*args):
        request = {
            "method": "get_games",
        }
        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        if self.connection is not None:
            self.connection.write(request.encode('utf-8'))

    def on_update_joinable_games_event(self):
        pass

    def on_game_started_event(self):
        pass

    def on_game_update_event(self):
        pass