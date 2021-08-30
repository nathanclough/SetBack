from setback.events.game_update_event import GameUpdateEvent
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import json
import uuid

class SelectTeam(Screen):
    game_name = StringProperty("Game Name")
    team_one = StringProperty("Team One")
    team_two = StringProperty("Team Two")

    def __init__(self, **kw):
        self.register_event_type('on_game_update')
        super(SelectTeam,self).__init__(**kw)
    
    def update_state(self,manager,game):
        self.game_name = game.name
        text = "Team One \n"
        for player in game.team_one:
            text += player.name + "\n"
        self.team_one = text
        text = "Team Two \n"
        for player in game.team_two:
            text += player.name +"\n"
        self.team_two = text

    def on_enter(self, *args):
        self.manager.bind(on_game_update=self.on_game_update)
        if not self.manager.game is None:
            self.update_state(None,self.manager.game)
        return super().on_enter(*args)
    
    def on_game_update(self,*largs):
        self.update_state(None,self.manager.game)
    
    def on_leave(self, *args):
        self.get_games()
        return super().on_leave(*args)

    def leave(self):
        request ={
            "method": "leave_game",
            "args" : "nonthing"}
        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.manager.connection.write(request.encode('utf-8'))
        self.manager.current = "homepage"
    
    def start(self):
        id = str(uuid.uuid4())
        request ={ "request_id": id,
            "method": "start_game",
            "args" : { "game_id": self.manager.game.id} }
        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.manager.connection.write(request.encode('utf-8'))

    def get_games(self,*args):
        request = {
            "method": "get_games",
        }
        self.manager.connection
        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.manager.connection.write(request.encode('utf-8'))

