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
        super(SelectTeam,self).__init__(**kw)

    def update_state(self):
        self.game_name = self.manager.game.name
        text = "Team One \n"
        for player in self.manager.game.team_one:
            text += player.name + "\n"
        self.team_one = text
        text = "Team Two \n"
        for player in self.manager.game.team_two:
            text += player.name +"\n"
        self.team_two = text

    def on_enter(self, *args):
        self.update_state()
        return super().on_enter(*args)

    def leave(self):
        id = str(uuid.uuid4())
        request ={ "request_id": id,
            "method": "leave_game",
            "args" : { "game_id": self.manager.game.id, "player_id" : self.manager.player.id}}
        request = json.dumps(request, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.manager.response_handlers[id] = self.handle_leave
        self.manager.connection.write(request.encode('utf-8'))       
    
    def handle_leave(self,args):
        self.manager.game.remove_player(self.manager.player.id)
        self.manager.current="homepage"