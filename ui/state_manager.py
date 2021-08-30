from setback.events.update_joinable_games import UpdateJoinableGamesEvent
from setback.events.game_update_event import GameUpdateEvent
from kivy.uix.screenmanager import ScreenManager
from setback import Player
from kivy.properties import ObjectProperty, ListProperty

class StateManager(ScreenManager):
    game_id = ""
    games_to_join = ListProperty()
    game = ObjectProperty()
    team_one = ListProperty()
    team_two = ListProperty()
    player = Player("Player",2)
    connection = None
    
    def __init__(self, **kwargs):
        self.register_event("game_update_event",self.handle_game_update_event)
        self.register_event("game_started_event",self.handle_game_start_event)
        self.register_event("update_joinable_games_event",self.handle_update_joinable_games_event)
        self.register_event_type('on_game_update')
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
            self.event_handlers[event] = [handler]
    
    def on_game_update(self):
        pass
    
    def handle_game_update_event(self,event):
        event = GameUpdateEvent.from_json(event)
        self.game = event.game
        self.team_one = event.game.team_one
        self.team_two = event.game.team_two  
        self.dispatch('on_game_update')

    def handle_update_joinable_games_event(self,event):
        event = UpdateJoinableGamesEvent.from_json(event)
        self.games_to_join = event.games

    def handle_game_start_event(self, event):
        self.current = "table"